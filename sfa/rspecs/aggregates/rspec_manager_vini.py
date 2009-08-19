from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.rspec import Rspec
from sfa.server.registry import Registries
from sfa.plc.nodes import *
from sfa.rspecs.aggregates.vini.utils import *
from sfa.rspecs.aggregates.vini.rspec import *
import sys

SFA_VINI_WHITELIST = '/etc/sfa/vini.whitelist'

"""
Copied from create_slice_aggregate() in sfa.plc.slices
"""
def create_slice_vini_aggregate(api, hrn, nodes):
    # Get the slice record from geni
    slice = {}
    registries = Registries(api)
    registry = registries[api.hrn]
    credential = api.getCredential()
    records = registry.resolve(credential, hrn)
    for record in records:
        if record.get_type() in ['slice']:
            slice = record.as_dict()
    if not slice:
        raise RecordNotFound(hrn)   

    # Make sure slice exists at plc, if it doesnt add it
    slicename = hrn_to_pl_slicename(hrn)
    slices = api.plshell.GetSlices(api.plauth, [slicename], ['node_ids'])
    if not slices:
        parts = slicename.split("_")
        login_base = parts[0]
        # if site doesnt exist add it
        sites = api.plshell.GetSites(api.plauth, [login_base])
        if not sites:
            authority = get_authority(hrn)
            site_records = registry.resolve(credential, authority)
            site_record = {}
            if not site_records:
                raise RecordNotFound(authority)
            site_record = site_records[0]
            site = site_record.as_dict()
                
            # add the site
            site.pop('site_id')
            site_id = api.plshell.AddSite(api.plauth, site)
        else:
            site = sites[0]
            
        slice_fields = {}
        slice_keys = ['name', 'url', 'description']
        for key in slice_keys:
            if key in slice and slice[key]:
                slice_fields[key] = slice[key]  
        api.plshell.AddSlice(api.plauth, slice_fields)
        slice = slice_fields
        slice['node_ids'] = 0
    else:
        slice = slices[0]    

    # get the list of valid slice users from the registry and make 
    # they are added to the slice 
    researchers = record.get('researcher', [])
    for researcher in researchers:
        person_record = {}
        person_records = registry.resolve(credential, researcher)
        for record in person_records:
            if record.get_type() in ['user']:
                person_record = record
        if not person_record:
            pass
        person_dict = person_record.as_dict()
        persons = api.plshell.GetPersons(api.plauth, [person_dict['email']],
                                         ['person_id', 'key_ids'])

        # Create the person record 
        if not persons:
            person_id=api.plshell.AddPerson(api.plauth, person_dict)

            # The line below enables the user account on the remote aggregate
            # soon after it is created.
            # without this the user key is not transfered to the slice
            # (as GetSlivers returns key of only enabled users),
            # which prevents the user from login to the slice.
            # We may do additional checks before enabling the user.

            api.plshell.UpdatePerson(api.plauth, person_id, {'enabled' : True})
            key_ids = []
        else:
            key_ids = persons[0]['key_ids']

        api.plshell.AddPersonToSlice(api.plauth, person_dict['email'],
                                     slicename)        

        # Get this users local keys
        keylist = api.plshell.GetKeys(api.plauth, key_ids, ['key'])
        keys = [key['key'] for key in keylist]

        # add keys that arent already there 
        for personkey in person_dict['keys']:
            if personkey not in keys:
                key = {'key_type': 'ssh', 'key': personkey}
                api.plshell.AddPersonKey(api.plauth, person_dict['email'], key)

    # find out where this slice is currently running
    nodelist = api.plshell.GetNodes(api.plauth, slice['node_ids'],
                                    ['hostname'])
    hostnames = [node['hostname'] for node in nodelist]

    # remove nodes not in rspec
    deleted_nodes = list(set(hostnames).difference(nodes))
    # add nodes from rspec
    added_nodes = list(set(nodes).difference(hostnames))

    """
    print >> sys.stderr, "Slice on nodes:"
    for n in hostnames:
        print >> sys.stderr, n
    print >> sys.stderr, "Wants nodes:"
    for n in nodes:
        print >> sys.stderr, n
    print >> sys.stderr, "Deleting nodes:"
    for n in deleted_nodes:
        print >> sys.stderr, n
    print >> sys.stderr, "Adding nodes:"
    for n in added_nodes:
        print >> sys.stderr, n
    """

    api.plshell.AddSliceToNodes(api.plauth, slicename, added_nodes) 
    api.plshell.DeleteSliceFromNodes(api.plauth, slicename, deleted_nodes)

    return 1

def get_rspec(api, hrn):
    rspec = ViniRspec()  
    (sites, nodes, tags) = get_topology(api)  

    rspec.updateCapacity(sites, nodes)
    
    if (hrn):
        slicename = hrn_to_pl_slicename(hrn)
        slice = get_slice(api, slicename)
        if slice:
            slice.hrn = hrn
            rspec.updateRequest(slice, nodes, tags)
        else:
            # call the default sfa.plc.nodes.get_rspec() method
            return Nodes(api).get_rspec(hrn)     

    return rspec.toxml()


"""
Check the requested topology against the available topology and capacity
"""
def check_request(hrn, rspec, nodes, sites, sitelinks, maxbw):
    linkspecs = rspec['Rspec']['Request'][0]['NetSpec'][0]['LinkSpec']
    if linkspecs:
        for l in linkspecs:
            n1 = Node.lookup(l['endpoint'][0])
            n2 = Node.lookup(l['endpoint'][1])
            bw = l['bw'][0]
            reqbps = get_tc_rate(bw)
            maxbps = get_tc_rate(maxbw)

            if reqbps <= 0:
                raise GeniInvalidArgument(bw, "BW")
            if reqbps > maxbps:
                raise PermissionError(" %s requested %s but max BW is %s" % 
                                      (hrn, bw, maxbw))

            if adjacent_nodes(n1, n2, sites, sitelinks):
                availbps = get_avail_bps(n1, n2, sites, sitelinks)
                if availbps < reqbps:
                    raise PermissionError("%s: capacity exceeded" % hrn)
            else:
                raise PermissionError("%s: nodes %s and %s not adjacent" 
                                      % (hrn, n1.tag, n2.tag))

"""
Hook called via 'sfi.py create'
"""
def create_slice(api, hrn, xml):
    r = Rspec(xml)
    rspec = r.toDict()

    ### Check the whitelist
    ### It consists of lines of the form: <slice hrn> <bw>
    whitelist = {}
    f = open(SFA_VINI_WHITELIST)
    for line in f.readlines():
        (slice, maxbw) = line.split()
        whitelist[slice] = maxbw
        
    if hrn in whitelist:
        maxbw = whitelist[hrn]
    else:
        raise PermissionError("%s not in VINI whitelist" % hrn)
        
    # Construct picture of global topology
    (sites, nodes, tags) = get_topology(api)

    # Check request against current allocations
    #check_request(hrn, rspec, nodes, sites, sitelinks, maxbw)

    nodes = rspec_to_nodeset(rspec)
    create_slice_vini_aggregate(api, hrn, nodes)

    # Add VINI-specific topology attributes to slice here
    try:
        linkspecs = rspec['Rspec']['Request'][0]['NetSpec'][0]['LinkSpec']
        if linkspecs:
            slicename = hrn_to_pl_slicename(hrn)
            slice = get_slice(api, slicename)
            if slice:
                slice.update_tag('vini_topo', 'manual', tags)
                slice.assign_egre_key(tags)
                slice.turn_on_netns(tags)
                slice.add_cap_net_admin(tags)

                nodedict = {}
                for (k, v) in get_nodedict(rspec).iteritems():
                    for id in nodes:
                        if v == nodes[id].hostname:
                            nodedict[k] = nodes[id]

                for l in linkspecs:
                    n1 = nodedict[l['endpoint'][0]]
                    n2 = nodedict[l['endpoint'][1]]
                    bw = l['bw'][0]
                    n1.add_link(n2, bw)
                    n2.add_link(n1, bw)

                for node in slice.get_nodes(nodes):
                    if node.links:
                        topo_str = "%s" % node.links
                        slice.update_tag('topo_rspec', topo_str, tags, node)

                # Update slice tags in database
                for i in tags:
                    tag = tags[i]
                    if tag.slice_id == slice.id:
                        if tag.tagname == 'topo_rspec' and not tag.updated:
                            tag.delete()
                        tag.write(api)
    except KeyError:
        # Bad Rspec
        pass
    

    return True

def get_nodedict(rspec):
    nodedict = {}
    try:    
        sitespecs = rspec['Rspec']['Capacity'][0]['NetSpec'][0]['SiteSpec']
        for s in sitespecs:
            for node in s['NodeSpec']:
                nodedict[node['name']] = node['hostname'][0]
    except KeyError:
        pass

    return nodedict

	
def rspec_to_nodeset(rspec):
    nodes = set()
    try:
        nodedict = get_nodedict(rspec)
        linkspecs = rspec['Rspec']['Request'][0]['NetSpec'][0]['LinkSpec']
        for l in linkspecs:
            for e in l['endpoint']:
                nodes.add(nodedict[e])
    except KeyError:
        # Bad Rspec
        pass
    
    return nodes

def main():
    r = Rspec()
    r.parseFile(sys.argv[1])
    rspec = r.toDict()
    create_slice(None,'plc',rspec)
    
if __name__ == "__main__":
    main()
