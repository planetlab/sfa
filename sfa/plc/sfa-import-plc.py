#!/usr/bin/python
#
##
# Import PLC records into the SFA database. It is indended that this tool be
# run once to create SFA records that reflect the current state of the
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
from sfa.util.table import SfaTable
from sfa.util.xrn import get_leaf, get_authority
from sfa.util.plxrn import hostname_to_hrn, slicename_to_hrn, email_to_hrn, hrn_to_pl_slicename
from sfa.util.config import Config
from sfa.trust.certificate import convert_public_key, Keypair
from sfa.trust.trustedroots import *
from sfa.trust.hierarchy import *
from sfa.util.xrn import Xrn
from sfa.plc.api import *
from sfa.trust.gid import create_uuid
from sfa.plc.sfaImport import sfaImport, _cleanup_string

def process_options():

   (options, args) = getopt.getopt(sys.argv[1:], '', [])
   for opt in options:
       name = opt[0]
       val = opt[1]


def load_keys(filename):
    keys = {}
    tmp_dict = {}
    try:
        execfile(filename, tmp_dict)
        if 'keys' in tmp_dict:
            keys = tmp_dict['keys']
        return keys
    except:
        return keys

def save_keys(filename, keys):
    f = open(filename, 'w')
    f.write("keys = %s" % str(keys))
    f.close()

def _get_site_hrn(interface_hrn, site):
    # Hardcode 'internet2' into the hrn for sites hosting
    # internet2 nodes. This is a special operation for some vini
    # sites only
    hrn = ".".join([interface_hrn, site['login_base']]) 
    if ".vini" in interface_hrn and interface_hrn.endswith('vini'):
        if site['login_base'].startswith("i2") or site['login_base'].startswith("nlr"):
            hrn = ".".join([interface_hrn, "internet2", site['login_base']])
    return hrn

def main():

    process_options()
    config = Config()
    if not config.SFA_REGISTRY_ENABLED:
        sys.exit(0)
    root_auth = config.SFA_REGISTRY_ROOT_AUTH
    interface_hrn = config.SFA_INTERFACE_HRN
    keys_filename = config.config_path + os.sep + 'person_keys.py' 
    sfaImporter = sfaImport()
    if config.SFA_API_DEBUG: sfaImporter.logger.setLevelDebug()
    shell = sfaImporter.shell
    plc_auth = sfaImporter.plc_auth 
    
    # initialize registry db table
    table = SfaTable()
    if not table.exists():
       table.create()

    # create root authority 
    sfaImporter.create_top_level_auth_records(root_auth)
    if not root_auth == interface_hrn:
        sfaImporter.create_top_level_auth_records(interface_hrn)

    # create s user record for the slice manager
    sfaImporter.create_sm_client_record()

    # create interface records
    sfaImporter.logger.info("Import: creating interface records")
    sfaImporter.create_interface_records()

    # add local root authority's cert  to trusted list
    sfaImporter.logger.info("Import: adding " + interface_hrn + " to trusted list")
    authority = sfaImporter.AuthHierarchy.get_auth_info(interface_hrn)
    sfaImporter.TrustedRoots.add_gid(authority.get_gid_object())

    # special case for vini
    if ".vini" in interface_hrn and interface_hrn.endswith('vini'):
        # create a fake internet2 site first
        i2site = {'name': 'Internet2', 'abbreviated_name': 'I2',
                    'login_base': 'internet2', 'site_id': -1}
        sfaImporter.import_site(interface_hrn, i2site)
   
    # create dict of all existing sfa records
    existing_records = {}
    existing_hrns = []
    key_ids = []
    person_keys = {} 
    results = table.find()
    for result in results:
        existing_records[(result['hrn'], result['type'])] = result
        existing_hrns.append(result['hrn']) 
            
    # Get all plc sites
    sites = shell.GetSites(plc_auth, {'peer_id': None})
    sites_dict = {}
    for site in sites:
        sites_dict[site['login_base']] = site 
    
    # Get all plc users
    persons = shell.GetPersons(plc_auth, {'peer_id': None, 'enabled': True}, ['person_id', 'email', 'key_ids', 'site_ids'])
    persons_dict = {}
    for person in persons:
        persons_dict[person['person_id']] = person
        key_ids.extend(person['key_ids'])

    # Get all public keys
    keys = shell.GetKeys(plc_auth, {'peer_id': None, 'key_id': key_ids})
    keys_dict = {}
    for key in keys:
        keys_dict[key['key_id']] = key['key']

    # create a dict of person keys keyed on key_id 
    old_person_keys = load_keys(keys_filename)
    for person in persons:
        pubkeys = []
        for key_id in person['key_ids']:
            pubkeys.append(keys_dict[key_id])
        person_keys[person['person_id']] = pubkeys

    # Get all plc nodes  
    nodes = shell.GetNodes(plc_auth, {'peer_id': None}, ['node_id', 'hostname', 'site_id'])
    nodes_dict = {}
    for node in nodes:
        nodes_dict[node['node_id']] = node

    # Get all plc slices
    slices = shell.GetSlices(plc_auth, {'peer_id': None}, ['slice_id', 'name'])
    slices_dict = {}
    for slice in slices:
        slices_dict[slice['slice_id']] = slice
    # start importing 
    for site in sites:
        site_hrn = _get_site_hrn(interface_hrn, site)
        sfaImporter.logger.info("Importing site: %s" % site_hrn)

        # import if hrn is not in list of existing hrns or if the hrn exists
        # but its not a site record
        if site_hrn not in existing_hrns or \
           (site_hrn, 'authority') not in existing_records:
            sfaImporter.import_site(site_hrn, site)
             
        # import node records
        for node_id in site['node_ids']:
            if node_id not in nodes_dict:
                continue 
            node = nodes_dict[node_id]
            site_auth = get_authority(site_hrn)
            site_name = get_leaf(site_hrn)
            hrn =  hostname_to_hrn(site_auth, site_name, node['hostname'])
            if hrn not in existing_hrns or \
               (hrn, 'node') not in existing_records:
                sfaImporter.import_node(hrn, node)

        # import slices
        for slice_id in site['slice_ids']:
            if slice_id not in slices_dict:
                continue 
            slice = slices_dict[slice_id]
            hrn = slicename_to_hrn(interface_hrn, slice['name'])
            if hrn not in existing_hrns or \
               (hrn, 'slice') not in existing_records:
                sfaImporter.import_slice(site_hrn, slice)      

        # import persons
        for person_id in site['person_ids']:
            if person_id not in persons_dict:
                continue 
            person = persons_dict[person_id]
            hrn = email_to_hrn(site_hrn, person['email'])
            old_keys = []
            new_keys = []
            if person_id in old_person_keys:
                old_keys = old_person_keys[person_id]
            if person_id in person_keys:
                new_keys = person_keys[person_id]
            update_record = False
            for key in new_keys:
                if key not in old_keys:
                    update_record = True 

            if hrn not in existing_hrns or \
               (hrn, 'user') not in existing_records or update_record:
                sfaImporter.import_person(site_hrn, person)

    
    # remove stale records    
    system_records = [interface_hrn, root_auth, interface_hrn + '.slicemanager']
    for (record_hrn, type) in existing_records.keys():
        if record_hrn in system_records:
            continue
        
        record = existing_records[(record_hrn, type)]
        if record['peer_authority']:
            continue

        # dont delete vini's internet2 placeholdder record
        # normally this would be deleted becuase it does not have a plc record 
        if ".vini" in interface_hrn and interface_hrn.endswith('vini') and \
           record_hrn.endswith("internet2"):     
            continue

        found = False
        
        if type == 'authority':    
            for site in sites:
                site_hrn = interface_hrn + "." + site['login_base']
                if site_hrn == record_hrn and site['site_id'] == record['pointer']:
                    found = True
                    break

        elif type == 'user':
            login_base = get_leaf(get_authority(record_hrn))
            username = get_leaf(record_hrn)
            if login_base in sites_dict:
                site = sites_dict[login_base]
                for person in persons:
                    tmp_username = person['email'].split("@")[0]
                    alt_username = person['email'].split("@")[0].replace(".", "_").replace("+", "_")
                    if username in [tmp_username, alt_username] and \
                       site['site_id'] in person['site_ids'] and \
                       person['person_id'] == record['pointer']:
                        found = True
                        break
        
        elif type == 'slice':
            slicename = hrn_to_pl_slicename(record_hrn)
            for slice in slices:
                if slicename == slice['name'] and \
                   slice['slice_id'] == record['pointer']:
                    found = True
                    break    
 
        elif type == 'node':
            login_base = get_leaf(get_authority(record_hrn))
            nodename = Xrn.unescape(get_leaf(record_hrn))
            if login_base in sites_dict:
                site = sites_dict[login_base]
                for node in nodes:
                    tmp_nodename = node['hostname']
                    if tmp_nodename == nodename and \
                       node['site_id'] == site['site_id'] and \
                       node['node_id'] == record['pointer']:
                        found = True
                        break  
        else:
            continue 
        
        if not found:
            record_object = existing_records[(record_hrn, type)]
            sfaImporter.delete_record(record_hrn, type) 
                                   
    # save pub keys
    sfaImporter.logger.info('Import: saving current pub keys')
    save_keys(keys_filename, person_keys)                
        
if __name__ == "__main__":
    main()
