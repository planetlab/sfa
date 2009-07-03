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

from geni.trust.certificate import *
from geni.trust.trustedroot import *
from geni.util.hierarchy import *
from geni.util.record import *
from geni.util.genitable import *
from geni.util.misc import *
from geni.util.config import *

# get PL account settings from config module
pl_auth = get_pl_auth()

def connect_shell():
    global pl_auth, shell

    # get PL account settings from config module
    pl_auth = get_pl_auth()

    # connect to planetlab
    if "Url" in pl_auth:
        from geni.util import remoteshell
        shell = remoteshell.RemoteShell()
    else:
        import PLC.Shell
        shell = PLC.Shell.Shell(globals = globals())

    return shell

# connect to planetlab
shell = connect_shell()

##
# Two authorities are specified: the root authority and the level1 authority.

#root_auth = "plc"
#level1_auth = None

#root_auth = "planetlab"
#level1_auth = "planetlab.us"
config = Config()

root_auth = config.GENI_REGISTRY_ROOT_AUTH
level1_auth = config.GENI_REGISTRY_LEVEL1_AUTH
if not level1_auth or level1_auth in ['']:
    level1_auth = None

def un_unicode(str):
   if isinstance(str, unicode):
       return str.encode("ascii", "ignore")
   else:
       return str

def cleanup_string(str):
    # pgsql has a fit with strings that have high ascii in them, so filter it
    # out when generating the hrns.
    tmp = ""
    for c in str:
        if ord(c) < 128:
            tmp = tmp + c
    str = tmp

    str = un_unicode(str)
    str = str.replace(" ", "_")
    str = str.replace(".", "_")
    str = str.replace("(", "_")
    str = str.replace("'", "_")
    str = str.replace(")", "_")
    str = str.replace('"', "_")
    return str

def process_options():
   global hrn

   (options, args) = getopt.getopt(sys.argv[1:], '', [])
   for opt in options:
       name = opt[0]
       val = opt[1]

def get_auth_table(auth_name):
    AuthHierarchy = Hierarchy()
    auth_info = AuthHierarchy.get_auth_info(auth_name)

    table = GeniTable(hrn=auth_name,
                      cninfo=auth_info.get_dbinfo())

    # if the table doesn't exist, then it means we haven't put any records
    # into this authority yet.

    if not table.exists():
        report.trace("Import: creating table for authority " + auth_name)
        table.create()

    return table

def person_to_hrn(parent_hrn, person):
    # the old way - Lastname_Firstname
    #personname = person['last_name'] + "_" + person['first_name']

    # the new way - use email address up to the "@" 
    personname = person['email'].split("@")[0]

    personname = cleanup_string(personname)

    hrn = parent_hrn + "." + personname
    return hrn

def import_person(parent_hrn, person):
    AuthHierarchy = Hierarchy()
    hrn = person_to_hrn(parent_hrn, person)

    # ASN.1 will have problems with hrn's longer than 64 characters
    if len(hrn) > 64:
        hrn = hrn[:64]

    report.trace("Import: importing person " + hrn)

    table = get_auth_table(parent_hrn)

    key_ids = []
    if 'key_ids' in person:    
        key_ids = person["key_ids"]
        
        # get the user's private key from the SSH keys they have uploaded
        # to planetlab
        keys = shell.GetKeys(pl_auth, key_ids)
        key = keys[0]['key']
        pkey =convert_public_key(key)
    else:
        # the user has no keys
        report.trace("   person " + hrn + " does not have a PL public key")

        # if a key is unavailable, then we still need to put something in the
        # user's GID. So make one up.
        pkey = Keypair(create=True)

    # create the gid 
    person_gid = AuthHierarchy.create_gid(hrn, create_uuid(), pkey)
    person_record = table.resolve("user", hrn)
    if not person_record:
        report.trace("  inserting user record for " + hrn)
        person_record = GeniRecord(name=hrn, gid=person_gid, type="user", pointer=person['person_id'])
        table.insert(person_record)
    else:
        report.trace("  updating user record for " + hrn)
        person_record = GeniRecord(name=hrn, gid=person_gid, type="user", pointer=person['person_id'])
        table.update(person_record)
            
def import_slice(parent_hrn, slice):
    AuthHierarchy = Hierarchy()
    slicename = slice['name'].split("_",1)[-1]
    slicename = cleanup_string(slicename)

    if not slicename:
        report.error("Import_Slice: failed to parse slice name " + slice['name'])
        return

    hrn = parent_hrn + "." + slicename
    report.trace("Import: importing slice " + hrn)

    table = get_auth_table(parent_hrn)

    slice_record = table.resolve("slice", hrn)
    if not slice_record:
        pkey = Keypair(create=True)
        slice_gid = AuthHierarchy.create_gid(hrn, create_uuid(), pkey)
        slice_record = GeniRecord(name=hrn, gid=slice_gid, type="slice", pointer=slice['slice_id'])
        report.trace("  inserting slice record for " + hrn)
        table.insert(slice_record)

def import_node(parent_hrn, node):
    AuthHierarchy = Hierarchy()
    nodename = node['hostname'].split(".")[0]
    nodename = cleanup_string(nodename)

    if not nodename:
        report.error("Import_node: failed to parse node name " + node['hostname'])
        return

    hrn = parent_hrn + "." + nodename

    # ASN.1 will have problems with hrn's longer than 64 characters
    if len(hrn) > 64:
        hrn = hrn[:64]

    report.trace("Import: importing node " + hrn)

    table = get_auth_table(parent_hrn)

    node_record = table.resolve("node", hrn)
    if not node_record:
        pkey = Keypair(create=True)
        node_gid = AuthHierarchy.create_gid(hrn, create_uuid(), pkey)
        node_record = GeniRecord(name=hrn, gid=node_gid, type="node", pointer=node['node_id'])
        report.trace("  inserting node record for " + hrn)
        table.insert(node_record)

def import_site(parent_hrn, site):
    AuthHierarchy = Hierarchy()
    sitename = site['login_base']
    sitename = cleanup_string(sitename)
    
    hrn = parent_hrn + "." + sitename
    
    # Hardcode 'internet2' into the hrn for sites hosting 
    # internet2 nodes. This is a special operation for some vini
    # sites only
    if ".vini" in parent_hrn and parent_hrn.endswith('vini'):
        if sitename.startswith("ii"): 
            sitename = sitename.replace("ii", "")
            hrn = ".".join([parent_hrn, "internet2", sitename]) 
        elif sitename.startswith("nlr"): 
            hrn = ".".join([parent_hrn, "internet2", sitename]) 
            sitename = sitename.replace("nlr", "")
         
    report.trace("Import_Site: importing site " + hrn)

    # create the authority
    if not AuthHierarchy.auth_exists(hrn):
        AuthHierarchy.create_auth(hrn)

    auth_info = AuthHierarchy.get_auth_info(hrn)

    table = get_auth_table(parent_hrn)

    auth_record = table.resolve("authority", hrn)
    if not auth_record:
        auth_record = GeniRecord(name=hrn, gid=auth_info.get_gid_object(), type="authority", pointer=site['site_id'])
        report.trace("  inserting authority record for " + hrn)
        table.insert(auth_record)

    if 'person_ids' in site: 
        for person_id in site['person_ids']:
            persons = shell.GetPersons(pl_auth, [person_id])
            if persons:
                try: 
                    import_person(hrn, persons[0])
                except:
                    report.trace("Failed to import: %s" % persons[0])
    if 'slice_ids' in site:
        for slice_id in site['slice_ids']:
            slices = shell.GetSlices(pl_auth, [slice_id])
            if slices:
                try:
                    import_slice(hrn, slices[0])
                except:
                    report.trace("Failed to import: %s" % slices[0])
    if 'node_ids' in site:
        for node_id in site['node_ids']:
            nodes = shell.GetNodes(pl_auth, [node_id])
            if nodes:
                try:
                    import_node(hrn, nodes[0])
                except:
                    report.trace("Failed to import: %s" % nodes[0])

def create_top_level_auth_records(hrn):
    parent_hrn = get_authority(hrn)
    print hrn, ":", parent_hrn
    if not parent_hrn:
        parent_hrn = hrn    
    auth_info = AuthHierarchy.get_auth_info(parent_hrn)
    table = get_auth_table(parent_hrn)

    auth_record = table.resolve("authority", hrn)
    if not auth_record:
        auth_record = GeniRecord(name=hrn, gid=auth_info.get_gid_object(), type="authority", pointer=-1)
        report.trace("  inserting authority record for " + hrn)
        table.insert(auth_record)

def main():
    global AuthHierarchy
    global TrustedRoots

    process_options()

    AuthHierarchy = Hierarchy()
    TrustedRoots = TrustedRootList()

    print "Import: creating top level authorities"

    if not AuthHierarchy.auth_exists(root_auth):
        AuthHierarchy.create_auth(root_auth)

    create_top_level_auth_records(root_auth)
    if level1_auth:
        if not AuthHierarchy.auth_exists(level1_auth):
            AuthHierarchy.create_auth(level1_auth)
        create_top_level_auth_records(level1_auth)
        import_auth = level1_auth
    else:
        import_auth = root_auth

    print "Import: adding", root_auth, "to trusted list"
    root = AuthHierarchy.get_auth_info(root_auth)
    TrustedRoots.add_gid(root.get_gid_object())

    connect_shell()

    sites = shell.GetSites(pl_auth, {'peer_id': None})
    # create a fake internet2 site first
    i2site = {'name': 'Internet2', 'abbreviated_name': 'I2',
                    'login_base': 'internet2', 'site_id': -1}
    import_site(import_auth, i2site)
    
    for site in sites:
        import_site(import_auth, site)

if __name__ == "__main__":
    main()
