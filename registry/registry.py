import tempfile
import os

from cert import *
from gid import *
from geniserver import *
from excep import *
from hierarchy import *
from misc import *

def get_pl_object_by_hrn(hrn):
    # find the object in the planetlab database
    pointer = None
    if (type=="sa") or (type=="ma"):
        authname = hrn_to_pl_authname(name):
        pl_res = shell.GetSites(pl_auth, {'name': authname)
        if pl_res:
            site_info = pl_res[0]
            pointer = auth_info['auth_id']
            return (site_info, pointer)
    elif (type=="slice"):
        slicename = hrn_to_pl_slicename(name)
        pl_res = shell.GetSlices(pl_auth, {'name': slicename)
        if pl_res:
            slice_info = pl_res[0]
            pointer = slice_info['slice_id']
            return (slice_info, pointer)
    elif (type=="user"):
        username = hrn_to_pl_username(name)
        pl_res = shell.GetPersons(pl_auth, {'name': slicename)
        if pl_res:
            person_info = pl_res[0]
            pointer = slice_info['person_id']
            return (person_info, pointer)
    elif (type=="component"):
        node_name = hrn_to_pl_nodename(hrn)
        pl_res = shell.GetNodes(pl_auth, {'name': nodename)
        if pl_res:
            node_info = pl_res[0]
            pointer = node_info['node_id']
            return (node_info, pointer)
    else:
        raise UnknownGeniType(type)

    return (None, None)

class Registry(GeniServer):
    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

    def register_functions(self):
        GeniServer.register_functions(self)
        self.server.register_function(self.get_self_credential)
        self.server.register_function(self.get_credential)
        self.server.register_function(self.get_gid)

    def get_auth_info(name):
        return Hierarchy.get_auth_info(name)

    def get_auth_table(self, auth_name):
        auth_info = get_auth_info(name, can_create=False)

        table = GeniTable(hrn = auth_name,
                          auth_info.get_cninfo()
                          auth_info.get_privkey_object()
                          auth_info.get_gid_object())

        # if the table doesn't exist, then it means we haven't put any records
        # into this authority yet.

        if not table.exists():
            table.create()

        return table

    def verify_auth_belongs_to_me(self, name):
        # get_auth_info will throw an exception if the authority does not
        # exist
        self.get_auth_info(name)

    def verify_object_belongs_to_me(self, name):
        auth_name = get_authority(name)
        self.verify_auth_belongs_to_me(auth_name)

    def register(self, cred, name, record_dict):
        self.decode_authentication(cred)

        auth_name = get_authority(name)
        auth_info = self.get_auth_info(auth_name)
        table = self.get_auth_table(auth_name)

        record = GeniRecord(dict = record_dict)
        type = record.get_type()

        pkey = None

        # check if record already exists
        existing_records = table.resolve(name, type)
        if existing_records:
            raise ExistingRecord(name)

        if (type == "sa") or (type=="ma"):
            # update the tree
            if not Hierarchy.auth_exists(name):
                Hierarchy.create_auth(name)

            # get the public key from the newly created authority
            child_auth_info = self.get_auth_info(name)
            pkey = child_auth_info.get_pkey_object()

            site_fields = record.get_pl_info()
            pointer = shell.AddSite(pl_auth, site_fields)
            record.set_pointer(pointer)

        elif (type == "slice"):
            slice_fields = record.get_pl_info()
            pointer = shell.AddSlice(pl_auth, slice_fields)
            record.set_pointer(pointer)

        elif (type == "user"):
            # TODO: extract pkey from user_fields
            user_fields = record.get_pl_info()
            pointer = shell.AddPerson(pl_auth, user_fields)
            record.set_pointer(pointer)

        elif (type == "node"):
            node_fields = record.get_pl_info()
            pointer = shell.AddNode(pl_auth, login_base, node_fields)
            record.set_pointer(pointer)

        else:
            raise UnknownGeniType(type)

        gid = Hierarchy.create_gid(name, create_uuid(), pkey)
        record.set_gid(gid.save_to_string())
        table.insert(record)

    def remove(self, cred, record_dict):
        self.decode_authentication(cred)

        record = GeniRecord(dict = record_dict)
        type = record.get_type()

        auth_name = get_authority(record.get_name())
        table = self.get_auth_table(auth_name)

        # let's not trust that the caller has a well-formed record (a forged
        # pointer field could be a disaster), so look it up ourselves
        record = table.resolve(type, record.get_name(), must_exist=True)[0]

        # TODO: sa, ma
        if type == "user":
            shell.DeletePerson(pl_auth, record.get_pointer())
        elif type == "slice":
            shell.DeleteSlice(pl_auth, record.get_pointer())
        elif type == "node":
            shell.DeleteNode(pl_auth, record.get_pointer())
        else:
            raise UnknownGeniType(type)

        table.remove(record_dict)

    def update(self, cred, record_dict):
        self.decode_authentication(cred)

        record = GeniRecord(dict = record_dict)
        type = record.get_type()

        auth_name = get_authority(record.get_name())
        table = self.get_auth_table(auth_name)

        # make sure the record exists
        existing_record = table.resolve(type, record.get_name(), must_exist=True)[0]
        pointer = existing_record.get_pointer()

        if (type == "sa") or (type == "ma"):
            shell.UpdateSite(pl_auth, pointer, record.get_pl_info())

        elif type == "slice":
            shell.UpdateSlice(pl_auth, pointer, record.get_pl_info())

        elif type == "user":
            shell.UpdatePerson(pl_auth, pointer, record.get_pl_info())

        elif type == "node":
            shell.UpdateNode(pl_auth, pointer, record.get_pl_info())

        else:
            raise UnknownGeniType(type)

    def list(self, cred):
        self.decode_authentication(cred)

        auth_name = self.object_gid.get_hrn()
        table = self.get_auth_table(auth_name)

        dict_list = table.list_dict()

        return dict_list

    def resolve_raw(self, type, name, must_exist=True):
        auth_name = get_authority(name)

        table = get_auth_table(auth_name)

        records = table.resolve(type, name)

        if (not records) and must_exist:
            raise RecordNotFound(name)

        return records

    def resolve(self, name):
        self.decode_authentication(cred)

        records = self.resolve("*", name)
        dicts = []
        for record in records:
            dicts.append(record.as_dict())

        return dicts

    def get_gid(self, name):
        self.verify_object_belongs_to_me(name) # XXX Fixme
        records = self.resolve_raw("*", name)
        gid_string_list = []
        for record in records:
            gid = record.get_gid()
            gid_string_list.append(gid.save_to_string())
        return gid_string_list

    def get_self_credential(self, type, name):
        self.verify_object_belongs_to_me(name)

        # find a record that matches
        records = self.resolve_raw(type, name, must_exist=True)
        record = records[0]

        gid = record.get_gid()
        peer_cert = self.server.peer_cert
        if not peer_cert.is_pubkey(gid.get_pubkey()):
           raise ConnectionKeyGIDMismatch(gid.get_subject())

        # create the credential
        gid = found_record.get_gid()
        cred = Credential(subject = gid.get_subject())
        cred.set_gid_caller(gid)
        cred.set_gid_object(gid)
        cred.set_issuer(key=self.key, subject=auth_hrn)
        cred.set_pubkey(gid.get_pubkey())
        cred.encode()
        cred.sign()

        return cred.save_to_string()

    def get_credential(self, cred, type, name):
        if not cred:
            return get_self_credential(self, type, name)

        self.decode_authentication(cred)

        self.verify_object_belongs_to_me(name)

        records = self.resolve(type, name, must_exist=True)
        record = records[0]

        object_gid = record.get_gid()
        new_cred = Credential(subject = object_gid.get_subject())
        new_cred.set_gid_caller(self.client_gid)
        new_cred.set_gid_object(object_gid)
        new_cred.set_issuer(key=self.key, cert=self.cert)
        new_cred.set_pubkey(object_gid.get_pubkey())
        new_cred.encode()
        new_cred.sign()

        return new_cred.save_to_string()

if __name__ == "__main__":
    key_file = "server.key"
    cert_file = "server.cert"

    # if no key is specified, then make one up
    if (not os.path.exists(key_file)) or (not os.path.exists(cert_file)):
        key = Keypair(create=True)
        key.save_to_file(key_file)

        cert = Certificate(subject="registry")
        cert.set_issuer(key=key, subject="registry")
        cert.set_pubkey(key)
        cert.sign()
        cert.save_to_file(cert_file)

    s = Registry("localhost", 12345, key_file, cert_file)
    s.run()

