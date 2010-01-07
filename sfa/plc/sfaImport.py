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
from sfa.util.namespace import *
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

class sfaImport:

    def __init__(self, logger=None):
        self.logger = logger
        self.AuthHierarchy = Hierarchy()
        self.config = Config()
        self.TrustedRoots = TrustedRootList(Config.get_trustedroots_dir(self.config))
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


    def create_top_level_auth_records(self, hrn):
        AuthHierarchy = self.AuthHierarchy
        urn = hrn_to_urn(hrn, 'authority')
        # if auth records for this hrn dont exist, create it
        if not AuthHierarchy.auth_exists(urn):
            trace("Import: creating top level authorites", self.logger)
            AuthHierarchy.create_auth(urn)
        

        # get the auth info of the newly created root auth (parent)
        # or level1_auth if it exists
        if self.level1_auth:
            auth_info = AuthHierarchy.get_auth_info(hrn)
            parent_hrn = hrn
        else:
            parent_hrn = get_authority(hrn)
            if not parent_hrn:
                parent_hrn = hrn
            auth_info = AuthHierarchy.get_auth_info(parent_hrn)
            
        table = SfaTable()
        auth_record = table.find({'type': 'authority', 'hrn': hrn})

        if not auth_record:
            auth_record = SfaRecord(hrn=hrn, gid=auth_info.get_gid_object(), type="authority", pointer=-1)
            auth_record['authority'] = get_authority(auth_record['hrn'])
            trace("Import: inserting authority record for " + hrn, self.logger)
            table.insert(auth_record)


    def import_person(self, parent_hrn, person):
        AuthHierarchy = self.AuthHierarchy
        hrn = email_to_hrn(parent_hrn, person['email'])

        # ASN.1 will have problems with hrn's longer than 64 characters
        if len(hrn) > 64:
            hrn = hrn[:64]

        trace("Import: importing person " + hrn, self.logger)
        key_ids = []
        if 'key_ids' in person and person['key_ids']:
            key_ids = person["key_ids"]
            # get the user's private key from the SSH keys they have uploaded
            # to planetlab
            keys = self.shell.GetKeys(self.plc_auth, key_ids)
            key = keys[0]['key']
            pkey = convert_public_key(key)
            if not pkey:
                pkey = Keypair(create=True)
        else:
            # the user has no keys
            trace("   person " + hrn + " does not have a PL public key", self.logger)
            # if a key is unavailable, then we still need to put something in the
            # user's GID. So make one up.
            pkey = Keypair(create=True)

        # create the gid
        urn = hrn_to_urn(hrn, 'user')
        person_gid = AuthHierarchy.create_gid(urn, create_uuid(), pkey)
        table = SfaTable()
        person_record = SfaRecord(hrn=hrn, gid=person_gid, type="user", pointer=person['person_id'])
        person_record['authority'] = get_authority(person_record['hrn'])
        existing_records = table.find({'hrn': hrn, 'type': 'user', 'pointer': person['person_id']})
        if not existing_records:
            table.insert(person_record)
        else:
            trace("Import: %s exists, updating " % hrn, self.logger)
            existing_record = existing_records[0]
            person_record['record_id'] = existing_record['record_id']
            table.update(person_record)

    def import_slice(self, parent_hrn, slice):
        AuthHierarchy = self.AuthHierarchy
        slicename = slice['name'].split("_",1)[-1]
        slicename = cleanup_string(slicename)

        if not slicename:
            error("Import_Slice: failed to parse slice name " + slice['name'], self.logger)
            return

        hrn = parent_hrn + "." + slicename
        trace("Import: importing slice " + hrn, self.logger)

        pkey = Keypair(create=True)
        urn = hrn_to_urn(hrn, 'slice')
        slice_gid = AuthHierarchy.create_gid(urn, create_uuid(), pkey)
        slice_record = SfaRecord(hrn=hrn, gid=slice_gid, type="slice", pointer=slice['slice_id'])
        slice_record['authority'] = get_authority(slice_record['hrn'])
        table = SfaTable()
        existing_records = table.find({'hrn': hrn, 'type': 'slice', 'pointer': slice['slice_id']})
        if not existing_records:
            table.insert(slice_record)
        else:
            trace("Import: %s exists, updating " % hrn, self.logger)
            existing_record = existing_records[0]
            slice_record['record_id'] = existing_record['record_id']
            table.update(slice_record)

    def import_node(self, parent_hrn, node):
        AuthHierarchy = self.AuthHierarchy
        nodename = node['hostname'].split(".")[0]
        nodename = cleanup_string(nodename)
        
        if not nodename:
            error("Import_node: failed to parse node name " + node['hostname'], self.logger)
            return

        hrn = parent_hrn + "." + nodename
        trace("Import: importing node " + hrn, self.logger)
        # ASN.1 will have problems with hrn's longer than 64 characters
        if len(hrn) > 64:
            hrn = hrn[:64]

        table = SfaTable()
        node_record = table.find({'type': 'node', 'hrn': hrn})
        pkey = Keypair(create=True)
        urn = hrn_to_urn(hrn, 'node')
        node_gid = AuthHierarchy.create_gid(urn, create_uuid(), pkey)
        node_record = SfaRecord(hrn=hrn, gid=node_gid, type="node", pointer=node['node_id'])
        node_record['authority'] = get_authority(node_record['hrn'])
        existing_records = table.find({'hrn': hrn, 'type': 'node', 'pointer': node['node_id']})
        if not existing_records:
            table.insert(node_record)
        else:
            trace("Import: %s exists, updating " % hrn, self.logger)
            existing_record = existing_records[0]
            node_record['record_id'] = existing_record['record_id']
            table.update(node_record)

    
    def import_site(self, parent_hrn, site):
        AuthHierarchy = self.AuthHierarchy
        shell = self.shell
        plc_auth = self.plc_auth
        sitename = site['login_base']
        sitename = cleanup_string(sitename)
        hrn = parent_hrn + "." + sitename
        urn = hrn_to_urn(hrn, 'authority')
        # Hardcode 'internet2' into the hrn for sites hosting
        # internet2 nodes. This is a special operation for some vini
        # sites only
        if ".vini" in parent_hrn and parent_hrn.endswith('vini'):
            if sitename.startswith("i2"):
                #sitename = sitename.replace("ii", "")
                hrn = ".".join([parent_hrn, "internet2", sitename])
            elif sitename.startswith("nlr"):
                #sitename = sitename.replace("nlr", "")
                hrn = ".".join([parent_hrn, "internet2", sitename])

        trace("Import: importing site " + hrn, self.logger)

        # create the authority
        if not AuthHierarchy.auth_exists(urn):
            AuthHierarchy.create_auth(urn)

        auth_info = AuthHierarchy.get_auth_info(urn)

        table = SfaTable()
        auth_record = SfaRecord(hrn=hrn, gid=auth_info.get_gid_object(), type="authority", pointer=site['site_id'])
        auth_record['authority'] = get_authority(auth_record['hrn'])
        existing_records = table.find({'hrn': hrn, 'type': 'authority', 'pointer': site['site_id']})
        if not existing_records:
            table.insert(auth_record)
        else:
            trace("Import: %s exists, updating " % hrn, self.logger)
            existing_record = existing_records[0]
            auth_record['record_id'] = existing_record['record_id']
            table.update(auth_record)

        return hrn


    def delete_record(self, hrn, type):
        # delete the record
        table = SfaTable()
        record_list = table.find({'type': type, 'hrn': hrn})
        for record in record_list:
            trace("Import: Removing record %s %s" % (type, hrn), self.logger)
            table.remove(record)        
