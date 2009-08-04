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

def person_to_hrn(parent_hrn, person):
    # the old way - Lastname_Firstname
    #personname = person['last_name'] + "_" + person['first_name']

    # the new way - use email address up to the "@"
    personname = person['email'].split("@")[0]

    personname = cleanup_string(personname)

    hrn = parent_hrn + "." + personname
    return hrn


class sfaImport:

    def __init__(self):
        self.AuthHierarchy = Hierarchy()
        self.TrustedRoots = TrustedRootList()

        self.config = Config()
        self.plc_auth = self.config.get_plc_auth()
        self.root_auth = self.config.SFA_REGISTRY_ROOT_AUTH
        self.level1_auth = self.config.SFA_REGISTRY_LEVEL1_AUTH
        if not self.level1_auth or self.level1_auth in ['']:
            self.level1_auth = None
        
        # connect to planetlab
        self.shell = None
        if "Url" in self.plc_auth:
            from sfa.plc.remoteshell import RemoteShell
            self.shell = RemoteShell()
        else:
            import PLC.Shell
            self.shell = PLC.Shell.Shell(globals = globals())        

    def get_auth_table(self, auth_name):
        AuthHierarchy = self.AuthHierarchy
        auth_info = AuthHierarchy.get_auth_info(auth_name)

        table = GeniTable(hrn=auth_name,
                          cninfo=auth_info.get_dbinfo())

        # if the table doesn't exist, then it means we haven't put any records
        # into this authority yet.

        if not table.exists():
            trace("Import: creating table for authority " + auth_name)
            table.create()

        return table


    def create_top_level_auth_records(self, hrn):
        AuthHierarchy = self.AuthHierarchy
        
        # if root doesnt exist, create it
        if not AuthHierarchy.auth_exists(hrn):
            AuthHierarchy.create_auth(hrn)
        
        # get the parent hrn
        parent_hrn = get_authority(hrn)
        if not parent_hrn:
            parent_hrn = hrn

        # get the auth info of the newly created root auth (parent)
        # or level1_auth if it exists
        auth_info = AuthHierarchy.get_auth_info(parent_hrn)
        if self.level1_auth:
            auth_info = AuthHierarchy.get_auth_info(hrn)
        table = self.get_auth_table(parent_hrn)

        auth_record = table.resolve("authority", hrn)
        if not auth_record:
            auth_record = GeniRecord(hrn=hrn, gid=auth_info.get_gid_object(), type="authority", pointer=-1)
            trace("  inserting authority record for " + hrn)
            table.insert(auth_record)


    def import_person(self, parent_hrn, person):
        AuthHierarchy = self.AuthHierarchy
        hrn = person_to_hrn(parent_hrn, person)

        # ASN.1 will have problems with hrn's longer than 64 characters
        if len(hrn) > 64:
            hrn = hrn[:64]

        trace("Import: importing person " + hrn)

        table = self.get_auth_table(parent_hrn)

        key_ids = []
        if 'key_ids' in person and person['key_ids']:
            key_ids = person["key_ids"]

            # get the user's private key from the SSH keys they have uploaded
            # to planetlab
            keys = self.shell.GetKeys(self.plc_auth, key_ids)
            key = keys[0]['key']
            pkey = convert_public_key(key)
        else:
            # the user has no keys
            trace("   person " + hrn + " does not have a PL public key")

            # if a key is unavailable, then we still need to put something in the
            # user's GID. So make one up.
            pkey = Keypair(create=True)

        # create the gid
        person_gid = AuthHierarchy.create_gid(hrn, create_uuid(), pkey)
        person_record = table.resolve("user", hrn)
        if not person_record:
            trace("  inserting user record for " + hrn)
            person_record = GeniRecord(hrn=hrn, gid=person_gid, type="user", pointer=person['person_id'])
            table.insert(person_record)
        else:
            trace("  updating user record for " + hrn)
            person_record = GeniRecord(hrn=hrn, gid=person_gid, type="user", pointer=person['person_id'])
            table.update(person_record)

    def import_slice(self, parent_hrn, slice):
        AuthHierarchy = self.AuthHierarchy
        slicename = slice['name'].split("_",1)[-1]
        slicename = cleanup_string(slicename)

        if not slicename:
            error("Import_Slice: failed to parse slice name " + slice['name'])
            return

        hrn = parent_hrn + "." + slicename
        trace("Import: importing slice " + hrn)

        table = self.get_auth_table(parent_hrn)

        slice_record = table.resolve("slice", hrn)
        if not slice_record:
            pkey = Keypair(create=True)
            slice_gid = AuthHierarchy.create_gid(hrn, create_uuid(), pkey)
            slice_record = GeniRecord(hrn=hrn, gid=slice_gid, type="slice", pointer=slice['slice_id'])
            trace("  inserting slice record for " + hrn)
            table.insert(slice_record)

    def import_node(self, parent_hrn, node):
        AuthHierarchy = self.AuthHierarchy
        nodename = node['hostname'].replace(".", "_")
        nodename = cleanup_string(nodename)

        if not nodename:
            error("Import_node: failed to parse node name " + node['hostname'])
            return

        hrn = parent_hrn + "." + nodename

        # ASN.1 will have problems with hrn's longer than 64 characters
        if len(hrn) > 64:
            hrn = hrn[:64]

        trace("Import: importing node " + hrn)

        table = self.get_auth_table(parent_hrn)

        node_record = table.resolve("node", hrn)
        if not node_record:
            pkey = Keypair(create=True)
            node_gid = AuthHierarchy.create_gid(hrn, create_uuid(), pkey)
            node_record = GeniRecord(hrn=hrn, gid=node_gid, type="node", pointer=node['node_id'])
            trace("  inserting node record for " + hrn)
            table.insert(node_record)


    
    def import_site(self, parent_hrn, site):
        AuthHierarchy = self.AuthHierarchy
        shell = self.shell
        plc_auth = self.plc_auth
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

        trace("Import_Site: importing site " + hrn)

        # create the authority
        if not AuthHierarchy.auth_exists(hrn):
            AuthHierarchy.create_auth(hrn)

        auth_info = AuthHierarchy.get_auth_info(hrn)

        table = self.get_auth_table(parent_hrn)

        auth_record = table.resolve("authority", hrn)
        if not auth_record:
            auth_record = GeniRecord(hrn=hrn, gid=auth_info.get_gid_object(), type="authority", pointer=site['site_id'])
            trace("  inserting authority record for " + hrn)
            table.insert(auth_record)

        if 'person_ids' in site:
            for person_id in site['person_ids']:
                persons = shell.GetPersons(plc_auth, [person_id])
                if persons:
                    try:
                        self.import_person(hrn, persons[0])
                    except Exception, e:
                        trace("Failed to import: %s (%s)" % (persons[0], e))
        if 'slice_ids' in site:
            for slice_id in site['slice_ids']:
                slices = shell.GetSlices(plc_auth, [slice_id])
                if slices:
                    try:
                        self.import_slice(hrn, slices[0])
                    except Exception, e:
                        trace("Failed to import: %s (%s)" % (slices[0], e))
        if 'node_ids' in site:
            for node_id in site['node_ids']:
                nodes = shell.GetNodes(plc_auth, [node_id])
                if nodes:
                    try:
                        self.import_node(hrn, nodes[0])
                    except Exception, e:
                        trace("Failed to import: %s (%s)" % (nodes[0], e))     

    def delete_record(self, parent_hrn, object, type):
        # get the hrn
        hrn = None
        if type in ['slice'] and 'name' in object and object['name']:
            slice_name = object['name'].split("_")[0]
            hrn = parent_hrn + "." + slice_name
        elif type in ['user', 'person'] and 'email' in object and object['email']:
            person_name = object['email'].split('@')[0]
            hrn = parent_hrn + "." + person_name
        elif type in ['node'] and 'hostname' in object and object['hostname']:
            node_name =  object['hostname'].replace('.','_')  
            hrn = parent_hrn + "." + node_name
        elif type in ['site'] and 'login_base' in object and object['login_base']:
            site_name = object['login_base']
            hrn = parent_hrn + "." + site_name         
        else:
            return

        table = self.get_auth_table(parent_hrn)
        record_list = table.resolve(type, hrn)
        if not record_list:
            return
        record = record_list[0]
        table.remove(record)        