from sfa.util.rspec import Rspec
import sys
import pdb

SFA_VINI_DEFAULT_RSPEC = '/etc/sfa/vini.rspec'

"""
Copied from create_slice_aggregate() in sfa.plc.slices.  
I could even call that directly.
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
            persons = api.plshell.GetPersons(api.plauth, [person_dict['email']], ['person_id', 'key_ids'])

            # Create the person record 
            if not persons:
                person_id=api.plshell.AddPerson(api.plauth, person_dict)

		# The line below enables the user account on the remote aggregate soon after it is created.
		# without this the user key is not transfered to the slice (as GetSlivers returns key of only enabled users),
		# which prevents the user from login to the slice. We may do additional checks before enabling the user.

		api.plshell.UpdatePerson(api.plauth, person_id, {'enabled' : True})
                key_ids = []
            else:
                key_ids = persons[0]['key_ids']

            api.plshell.AddPersonToSlice(api.plauth, person_dict['email'], slicename)        

            # Get this users local keys
            keylist = api.plshell.GetKeys(api.plauth, key_ids, ['key'])
            keys = [key['key'] for key in keylist]

            # add keys that arent already there 
            for personkey in person_dict['keys']:
                if personkey not in keys:
                    key = {'key_type': 'ssh', 'key': personkey}
                    api.plshell.AddPersonKey(api.plauth, person_dict['email'], key)

        # find out where this slice is currently running
        nodelist = api.plshell.GetNodes(api.plauth, slice['node_ids'], ['hostname'])
        hostnames = [node['hostname'] for node in nodelist]

        # remove nodes not in rspec
        deleted_nodes = list(set(hostnames).difference(nodes))
        # add nodes from rspec
        added_nodes = list(set(nodes).difference(hostnames))

        api.plshell.AddSliceToNodes(api.plauth, slicename, added_nodes) 
        api.plshell.DeleteSliceFromNodes(api.plauth, slicename, deleted_nodes)

        return 1


def get_rspec(hrn):
    rspec = None
    
    if (hrn):
        pass
    else:
        # Return canned response for now...
        r = Rspec()
        r.parseFile(SFA_VINI_DEFAULT_RSPEC)
        rspec = r.toGenDict()

    return rspec


def create_slice(api, hrn, rspec):
    # Check request against current allocations
    # Request OK

    nodes = rspec_to_nodeset(rspec)
    create_slice_vini_aggregate(api, hrn, nodes)

    # Add VINI-specific topology attributes to slice here

    return True

def rspec_to_nodeset(rspec):
    nodedict = {}
    nodes = set()
    try:
        sitespecs = rspec['Rspec'][0]['Capacity'][0]['NetSpec'][0]['SiteSpec']
        for s in sitespecs:
            for node in s['NodeSpec']:
                nodedict[node['name'][0]] = node['hostname'][0]

        linkspecs = rspec['Rspec'][0]['Request'][0]['NetSpec'][0]['LinkSpec']
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
    rspec = r.toGenDict()
    create_slice(None,'plc',rspec)
    
if __name__ == "__main__":
    main()
