#!/usr/bin/python
#
### $Id$
### $URL$
#
##
# Import PLC records into the Geni database. It is indended that this tool be
# run once to create Geni records that reflect the current state of the
# planetlab database.
#
# The import tool assumes that the existing PLC hierarchy should all be part
# of "planetlab.us" (see the root_auth and level1_auth variables below).
#
# Public keys are extracted from the users' SSH keys automatically and used to
# create GIDs. This is relatively experimental as a custom tool had to be
# written to perform conversion from SSH to OpenSSL format. It only supports
# RSA keys at this time, not DSA keys.
##

import getopt
import sys
import tempfile

from sfa.util.record import *
from sfa.util.genitable import GeniTable
from sfa.util.misc import *
from sfa.util.config import Config
from sfa.util.report import trace, error

from sfa.trust.certificate import convert_public_key, Keypair
from sfa.trust.trustedroot import *
from sfa.trust.hierarchy import *
from sfa.trust.gid import create_uuid
from sfa.plc.sfaImport import *



def process_options():
   global hrn

   (options, args) = getopt.getopt(sys.argv[1:], '', [])
   for opt in options:
       name = opt[0]
       val = opt[1]

def main():
    process_options()
    config = Config()
    root_auth = config.SFA_REGISTRY_ROOT_AUTH
    level1_auth = config.SFA_REGISTRY_LEVEL1_AUTH
    sfaImporter = sfaImport()
    shell = sfaImporter.shell
    plc_auth = sfaImporter.plc_auth 
    AuthHierarchy = sfaImporter.AuthHierarchy
    TrustedRoots = sfaImporter.TrustedRoots
    table = GeniTable()
    if not table.exists():
        table.create()

    if not level1_auth or level1_auth in ['']:
        level1_auth = None
    
    print "Import: creating top level authorities"
    if not level1_auth:
        sfaImporter.create_top_level_auth_records(root_auth)
        import_auth = root_auth
    else:
        if not AuthHierarchy.auth_exists(level1_auth):
            AuthHierarchy.create_auth(level1_auth)
        sfaImporter.create_top_level_auth_records(level1_auth)
        import_auth = level1_auth

    print "Import: adding", import_auth, "to trusted list"
    authority = AuthHierarchy.get_auth_info(import_auth)
    TrustedRoots.add_gid(authority.get_gid_object())

    if ".vini" in import_auth and import_auth.endswith('vini'):
        # create a fake internet2 site first
        i2site = {'name': 'Internet2', 'abbreviated_name': 'I2',
                    'login_base': 'internet2', 'site_id': -1}
        sfaImporter.import_site(import_auth, i2site)
   
    # create dict of all existing sfa records
    existing_records = {}
    existing_hrns = []
    results = table.find()
    for result in results:
        existing_records[(result['hrn'], result['type'])] = result
        existing_hrns.append(result['hrn']) 
            
    # Get all plc sites
    sites = shell.GetSites(plc_auth)
    
    # Get all plc users
    persons = shell.GetPersons(plc_auth, {}, ['person_id', 'email', 'key_ids'])
    persons_dict = {}
    for person in persons:
        persons_dict[person['person_id']] = person

    # Get all plc nodes  
    nodes = shell.GetNodes(plc_auth, {}, ['node_id', 'hostname'])
    nodes_dict = {}
    for node in nodes:
        nodes_dict[node['node_id']] = node

    # Get all plc slices
    slices = shell.GetSlices(plc_auth, {}, ['slice_id', 'name'])
    slices_dict = {}
    for slice in slices:
        slices_dict[slice['slice_id']] = slice

    # start importing 
    for site in sites:
        site_hrn = import_auth + "." + site['login_base']
        # import if hrn is not in list of existing hrns or if the hrn exists
        # but its not a site record
        if site_hrn not in existing_hrns or \
           (site_hrn, 'authority') not in existing_records:
            sfaImporter.import_site(import_auth, site)
             
        # import node records
        for node_id in site['node_ids']:
            if node_id not in nodes_dict:
                continue 
            node = nodes_dict[node_id]
            hrn =  hostname_to_hrn(import_auth, site['login_base'], node['hostname'])
            if hrn not in existing_hrns or \
               (hrn, 'node') not in existing_records:
                sfaImporter.import_node(site_hrn, node)

        # import slices
        for slice_id in site['slice_ids']:
            if slice_id not in slices_dict:
                continue 
            slice = slices_dict[slice_id]
            hrn = slicename_to_hrn(import_auth, slice['name'])
            if hrn not in existing_hrns or \
               (hrn, 'slice') not in existing_records:
                sfaImporter.import_slice(site_hrn, slice)      

        # import persons
        for person_id in site['person_ids']:
            if person_id not in persons_dict:
                continue 
            person = persons_dict[person_id]
            hrn = email_to_hrn(site_hrn, person['email'])
            if hrn not in existing_hrns or \
               (hrn, 'user') not in existing_records:
                sfaImporter.import_person(site_hrn, person)

        
        # remove any record in existing_hrns that does not 
        # have a plc record
        site_existing_records_only = lambda (r_hrn, r_type): r_hrn.startswith(site_hrn)
        site_existing_records = filter(site_existing_records_only, existing_records.keys())
        for (record_hrn, type) in site_existing_records:
            found = False
            if type == 'user':
                for person in persons_dict.values():
                    tmp_hrn = email_to_hrn(site_hrn, person['email'])
                    if record_hrn == tmp_hrn:
                        found = True

            elif type == 'node':
                for node in nodes_dict.values():
                    tmp_hrn = hostname_to_hrn(import_auth, site['login_base'], node['hostname'])
                    if record_hrn == tmp_hrn:
                        found = True
            elif type == 'slice':
                for slice in slices_dict.values():
                    tmp_hrn = slicename_to_hrn(import_auth, slice['name'])
                    if record_hrn == tmp_hrn:
                        found = True
            else:
                continue
 
            if not found:
                trace("Import: Removing %s %s" % (type, record_hrn)) 
                record_object = existing_records[(record_hrn, type)]
                sfaImporter.delete_record(record_hrn, type)
    
    # remove stale site_records    
    site_records_only = lambda(r_hrn, r_type): r_type == 'authority' and r_hrn != import_auth
    site_records = filter(site_records_only, existing_records.keys())
    for (record_hrn, type) in site_records:
        found = False
        for site in sites:
            site_hrn = import_auth + "." + site['login_base']
            if site_hrn == record_hrn:
                found = True
        if not found:
            trace("Import: Removing %s %s" % (type,  record_hrn))
            record_object = existing_records[(record_hrn, type)]
            sfaImporter.delete_record(record_hrn, type) 
                                   
                    
        
if __name__ == "__main__":
    main()
