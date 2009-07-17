#!/usr/bin/python

from sfa.util.rspec import Rspec
import sys
import pdb

SFA_MAX_CONF_FILE = '/etc/sfa/max_allocations'

# Topology 

topology = {'pl23':('planetlab2.dragon.maxgigapop.net','planetlab3.dragon.maxgigapop.net'),
            'pl24':('planetlab2.dragon.maxgigapop.net','planetlab4.dragon.maxgigapop.net'),
            'pl25':('planetlab2.dragon.maxgigapop.net','planetlab5.dragon.maxgigapop.net'),
            'pl34':('planetlab3.dragon.maxgigapop.net','planetlab4.dragon.maxgigapop.net'),
            'pl35':('planetlab3.dragon.maxgigapop.net','planetlab5.dragon.maxgigapop.net'),
            'pl45':('planetlab4.dragon.maxgigapop.net','planetlab5.dragon.maxgigapop.net')
            }

def link_endpoints(links):
    nodes=[]
    for l in links:
        nodes.extend(topology[l])
    return nodes

def lock_state_file():
    # Noop for demo
    return True

def unlock_state_file():
    return True
    # Noop for demo

def read_alloc_dict():
    alloc_dict={}
    rows = open(SFA_MAX_CONF_FILE).read().split('\n')
    for r in rows:
        columns = r.split(' ')
        if (len(columns)>2):
            hrn = columns[0]
            allocs = columns[1].split(',')
            alloc_dict[hrn]=allocs
    return alloc_dict

def commit_alloc_dict(d):
    f = open(SFA_MAX_CONF_FILE, 'w')
    for hrn in d.keys():
        columns = d[hrn]
        row = hrn+' '+','.join(columns)+'\n'
        f.write(row)
    f.close()

def collapse_alloc_dict(d):
    ret = []
    for k in d.keys():
        ret.extend(d[k])
    return ret


def alloc_links(api, links_to_add, links_to_drop, foo):
    return True

def alloc_nodes(api,hrn, requested_links, links_to_delete):
    
    nodes_to_add = link_endpoints(links_to_add)
    nodes_to_delete = link_endpoints(links_to_delete)

    pdb.set_trace()
    create_slice_max_aggregate(api, hrn, nodes_to_add, nodes_to_delete)

# Taken from slices.py

def create_slice_max_aggregate(api, hrn, nodes):
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

    api.plshell.AddSliceToNodes(api.plauth, slicename, added_nodes) 
    api.plshell.DeleteSliceFromNodes(api.plauth, slicename, deleted_nodes)

    return 1


def get_rspec(hrn):
    # Eg. config line:
    # plc.princeton.sapan vlan23,vlan45

    allocations = read_alloc_dict()
    if (hrn):
        current_allocations = allocations[hrn]
    else:
        current_allocations = collapse_alloc_dict(allocations)

    return (allocations_to_rspec_dict(current_allocations))


def create_slice(api, hrn, rspec):
    # Check if everything in rspec is either allocated by hrn
    # or not allocated at all.

    lock_state_file()

    allocations = read_alloc_dict()
    requested_allocations = rspec_to_allocations (rspec)
    current_allocations = collapse_alloc_dict(allocations)
    try:
        current_hrn_allocations=allocations[hrn]
    except KeyError:
        current_hrn_allocations=[]

    # Check request against current allocations
    for a in requested_allocations:
        if (a not in current_hrn_allocations and a in current_allocations):
            return False
    # Request OK

    # Allocations to delete
    allocations_to_delete = []
    for a in current_hrn_allocations:
        if (a not in requested_allocations):
            allocations_to_delete.extend([a])

    # Ok, let's do our thing
    alloc_nodes(api, hrn, requested_allocations, allocations_to_delete)
    alloc_links(api, hrn, requested_allocations, allocations_to_delete)
    allocations[hrn] = requested_allocations
    commit_alloc_dict(allocations)

    unlock_state_file()

    return True

def rspec_to_allocations(rspec):
    links = []
    try:
        linkspecs = rspec['rspec']['request'][0]['netspec'][0]['linkspec']
        for l in linkspecs:
            links.extend([l['name'].replace('tns:','')])
        
    except KeyError:
        # Bad Rspec
        pass
    return links

def main():
    r = Rspec()
    rspec_xml = open(sys.argv[1]).read()
    r.parseString(rspec_xml)
    rspec = r.toDict()
    create_slice(None,'plc',rspec)
    
if __name__ == "__main__":
    main()
