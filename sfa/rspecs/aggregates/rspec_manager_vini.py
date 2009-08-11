from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.rspec import Rspec
from sfa.server.registry import Registries
from sfa.plc.nodes import *
import sys
import socket

SFA_VINI_DEFAULT_RSPEC = '/etc/sfa/vini.rspec'

class Node:
    def __init__(self, node):
        self.id = node['node_id']
        self.hostname = node['hostname']
        self.shortname = self.hostname.replace('.vini-veritas.net', '')
        self.site_id = node['site_id']
        self.ipaddr = socket.gethostbyname(self.hostname)
        self.links = []

    def get_link_id(self, remote):
        if self.id < remote.id:
            link = (self.id<<7) + remote.id
        else:
            link = (remote.id<<7) + self.id
        return link
        
    def get_iface_id(self, remote):
        if self.id < remote.id:
            iface = 1
        else:
            iface = 2
        return iface
    
    def get_virt_ip(self, remote):
        link = self.get_link_id(remote)
        iface = self.get_iface_id(remote)
        first = link >> 6
        second = ((link & 0x3f)<<2) + iface
        return "192.168.%d.%d" % (first, second)

    def get_virt_net(self, remote):
        link = self.get_link_id(remote)
        first = link >> 6
        second = (link & 0x3f)<<2
        return "192.168.%d.%d/30" % (first, second)
        
    def get_site(self, sites):
        return sites[self.site_id]
            
    def adjacent_nodes(self, sites, nodes, node_ids):
        mysite = self.get_site(sites)
        adj_ids = mysite.adj_node_ids.intersection(node_ids)
        adj_nodes = []
        for id in adj_ids:
            adj_nodes.append(nodes[id])
        return adj_nodes
    
    def init_links(self):
        self.links = []
        
    def add_link(self, remote, bw):
        my_ip = self.get_virt_ip(remote)
        remote_ip = remote.get_virt_ip(self)
        net = self.get_virt_net(remote)
        link = remote.id, remote.ipaddr, bw, my_ip, remote_ip, net
        self.links.append(link)

        
class Site:
    def __init__(self, site):
        self.id = site['site_id']
        self.node_ids = site['node_ids']
        self.adj_site_ids = set()
        self.adj_node_ids = set()

    def get_sitenodes(self, nodes):
        n = []
        for i in self.node_ids:
            n.append(nodes[i])
        return n
    
    def add_adjacency(self, site):
        self.adj_site_ids.add(site.id)
        for n in site.node_ids:
            self.adj_node_ids.add(n)
        
    
class Slice:
    def __init__(self, slice):
        self.id = slice['slice_id']
        self.name = slice['name']
        self.node_ids = set(slice['node_ids'])
        self.slice_tag_ids = slice['slice_tag_ids']
    
    def get_tag(self, tagname, slicetags, node = None):
        for i in self.slice_tag_ids:
            tag = slicetags[i]
            if tag.tagname == tagname:
                if (not node) or (node.id == tag.node_id):
                    return tag
        else:
            return None
        
    def get_nodes(self, nodes):
        n = []
        for id in self.node_ids:
            n.append(nodes[id])
        return n
             
    
    # Add a new slice tag   
    def add_tag(self, tagname, value, slicetags, node = None):
        record = {'slice_tag_id':None, 'slice_id':self.id, 'tagname':tagname, 'value':value}
        if node:
            record['node_id'] = node.id
        else:
            record['node_id'] = None
        tag = Slicetag(record)
        slicetags[tag.id] = tag
        self.slice_tag_ids.append(tag.id)
        tag.changed = True       
        tag.updated = True
        return tag
    
    # Update a slice tag if it exists, else add it             
    def update_tag(self, tagname, value, slicetags, node = None):
        tag = self.get_tag(tagname, slicetags, node)
        if tag and tag.value == value:
            value = "no change"
        elif tag:
            tag.value = value
            tag.changed = True
        else:
            tag = self.add_tag(tagname, value, slicetags, node)
        tag.updated = True
            
    def assign_egre_key(self, slicetags):
        if not self.get_tag('egre_key', slicetags):
            try:
                key = free_egre_key(slicetags)
                self.update_tag('egre_key', key, slicetags)
            except:
                # Should handle this case...
                pass
        return
            
    def turn_on_netns(self, slicetags):
        tag = self.get_tag('netns', slicetags)
        if (not tag) or (tag.value != '1'):
            self.update_tag('netns', '1', slicetags)
        return
   
    def turn_off_netns(self, slicetags):
        tag = self.get_tag('netns', slicetags)
        if tag and (tag.value != '0'):
            tag.delete()
        return
    
    def add_cap_net_admin(self, slicetags):
        tag = self.get_tag('capabilities', slicetags)
        if tag:
            caps = tag.value.split(',')
            for cap in caps:
                if cap == "CAP_NET_ADMIN":
                    return
            else:
                newcaps = "CAP_NET_ADMIN," + tag.value
                self.update_tag('capabilities', newcaps, slicetags)
        else:
            self.add_tag('capabilities', 'CAP_NET_ADMIN', slicetags)
        return
    
    def remove_cap_net_admin(self, slicetags):
        tag = self.get_tag('capabilities', slicetags)
        if tag:
            caps = tag.value.split(',')
            newcaps = []
            for cap in caps:
                if cap != "CAP_NET_ADMIN":
                    newcaps.append(cap)
            if newcaps:
                value = ','.join(newcaps)
                self.update_tag('capabilities', value, slicetags)
            else:
                tag.delete()
        return

    # Update the vsys/setup-link and vsys/setup-nat slice tags.
    def add_vsys_tags(self, slicetags):
        link = nat = False
        for i in self.slice_tag_ids:
            tag = slicetags[i]
            if tag.tagname == 'vsys':
                if tag.value == 'setup-link':
                    link = True
                elif tag.value == 'setup-nat':
                    nat = True
        if not link:
            self.add_tag('vsys', 'setup-link', slicetags)
        if not nat:
            self.add_tag('vsys', 'setup-nat', slicetags)
        return


class Slicetag:
    newid = -1 
    def __init__(self, tag):
        self.id = tag['slice_tag_id']
        if not self.id:
            # Make one up for the time being...
            self.id = Slicetag.newid
            Slicetag.newid -= 1
        self.slice_id = tag['slice_id']
        self.tagname = tag['tagname']
        self.value = tag['value']
        self.node_id = tag['node_id']
        self.updated = False
        self.changed = False
        self.deleted = False
    
    # Mark a tag as deleted
    def delete(self):
        self.deleted = True
        self.updated = True
    
    def write(self, api):
        if self.changed:
            if int(self.id) > 0:
                api.plshell.UpdateSliceTag(api.plauth, self.id, self.value)
            else:
                api.plshell.AddSliceTag(api.plauth, self.slice_id, 
                                        self.tagname, self.value, self.node_id)
        elif self.deleted and int(self.id) > 0:
            api.plshell.DeleteSliceTag(api.plauth, self.id)


"""
Create a dictionary of site objects keyed by site ID
"""
def get_sites():
    tmp = []
    for site in GetSites():
        t = site['site_id'], Site(site)
        tmp.append(t)
    return dict(tmp)


"""
Create a dictionary of node objects keyed by node ID
"""
def get_nodes(api):
    tmp = []
    for node in api.plshell.GetNodes(api.plauth):
        t = node['node_id'], Node(node)
        tmp.append(t)
    return dict(tmp)

"""
Create a dictionary of slice objects keyed by slice ID
"""
def get_slice(api, slicename):
    slice = api.plshell.GetSlices(api.plauth, [slicename])
    if slice:
        return Slice(slice[0])
    else:
        return None

"""
Create a dictionary of slicetag objects keyed by slice tag ID
"""
def get_slice_tags(api):
    tmp = []
    for tag in api.plshell.GetSliceTags(api.plauth):
        t = tag['slice_tag_id'], Slicetag(tag)
        tmp.append(t)
    return dict(tmp)
    
"""
Find a free EGRE key
"""
def free_egre_key(slicetags):
    used = set()
    for i in slicetags:
        tag = slicetags[i]
        if tag.tagname == 'egre_key':
            used.add(int(tag.value))
                
    for i in range(1, 256):
        if i not in used:
            key = i
            break
    else:
        raise KeyError("No more EGRE keys available")
        
    return "%s" % key
   

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
    # Get default rspec
    default = Rspec()
    default.parseFile(SFA_VINI_DEFAULT_RSPEC)
    
    if (hrn):
        slicename = hrn_to_pl_slicename(hrn)
        defaultrspec = default.toDict()
        nodedict = get_nodedict(defaultrspec)

        # call the default sfa.plc.nodes.get_rspec() method
        nodes = Nodes(api)	
        rspec = nodes.get_rspec(hrn)     

        # Grab all the PLC info we'll need at once
        slice = get_slice(api, slicename)
        if slice:
            nodes = get_nodes(api)
            tags = get_slice_tags(api)

            # Add the node tags from the Capacity statement to Node objects
            for (k, v) in nodedict.iteritems():
                for id in nodes:
                    if v == nodes[id].hostname:
                        nodes[id].tag = k

            endpoints = []
            for node in slice.get_nodes(nodes):
                linktag = slice.get_tag('topo_rspec', tags, node)
                if linktag:
                    l = eval(linktag.value)
                    for (id, realip, bw, lvip, rvip, vnet) in l:
                        endpoints.append((node.id, id, bw))
            
            if endpoints:
                linkspecs = []
                for (l, r, bw) in endpoints:
                    if (r, l, bw) in endpoints:
                        if l < r:
                            edict = {}
                            edict['endpoint'] = [nodes[l].tag, nodes[r].tag]
                            edict['bw'] = [bw]
                            linkspecs.append(edict)

                d = default.toDict()
                d['Rspec']['Request'][0]['NetSpec'][0]['LinkSpec'] = linkspecs
                d['Rspec']['Request'][0]['NetSpec'][0]['name'] = hrn
                new = Rspec()
                new.parseDict(d)
                rspec = new.toxml()
    else:
        # Return canned response for now...
        rspec = default.toxml()

    return rspec


def create_slice(api, hrn, xml):
    r = Rspec(xml)
    rspec = r.toDict()

    # Check request against current allocations
    # Request OK

    nodes = rspec_to_nodeset(rspec)
    create_slice_vini_aggregate(api, hrn, nodes)

    # Add VINI-specific topology attributes to slice here
    try:
        linkspecs = rspec['Rspec']['Request'][0]['NetSpec'][0]['LinkSpec']
        if linkspecs:
            slicename = hrn_to_pl_slicename(hrn)

            # Grab all the PLC info we'll need at once
            slice = get_slice(api, slicename)
            if slice:
                nodes = get_nodes(api)
                tags = get_slice_tags(api)

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
