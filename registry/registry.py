import tempfile
import os
import time
import sys

from cert import *
from gid import *
from geniserver import *
from excep import *
from trustedroot import *
from hierarchy import *
from misc import *
from record import *
from genitable import *
from geniticket import *

def geni_fields_to_pl_fields(type, hrn, geni_fields, pl_fields):
    if type == "user":
        if not "email" in pl_fields:
            if not "email" in geni_fields:
                raise MissingGeniInfo("email")
            pl_fields["email"] = geni_fields["email"]

        if not "first_name" in pl_fields:
            pl_fields["first_name"] = "geni"

        if not "last_name" in pl_fields:
            pl_fields["last_name"] = hrn

    elif type == "slice":
        if not "instantiation" in pl_fields:
            pl_fields["instantiation"] = "plc-instantiated"
        if not "name" in pl_fields:
            pl_fields["name"] = hrn_to_pl_slicename(hrn)
        if not "max_nodes" in pl_fields:
            pl_fields["max_nodes"] = 10

    elif type == "node":
        if not "hostname" in pl_fields:
            if not "dns" in geni_fields:
                raise MissingGeniInfo("dns")
            pl_fields["hostname"] = geni_fields["dns"]

        if not "model" in pl_fields:
            pl_fields["model"] = "geni"

    elif type == "sa":
        pl_fields["login_base"] = hrn_to_pl_login_base(hrn)

        if not "name" in pl_fields:
            pl_fields["name"] = hrn

        if not "abbreviated_name" in pl_fields:
            pl_fields["abbreviated_name"] = hrn

        if not "enabled" in pl_fields:
            pl_fields["enabled"] = True

        if not "is_public" in pl_fields:
            pl_fields["is_public"] = True

class Registry(GeniServer):
    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

        # get PL account settings from config module
        self.pl_auth = get_pl_auth()

        # connect to planetlab
        if "Url" in self.pl_auth:
            self.connect_remote_shell()
        else:
            self.connect_local_shell()

    def connect_remote_shell(self):
        import remoteshell
        self.shell = remoteshell.RemoteShell()

    def connect_local_shell(self):
        import PLC.Shell
        self.shell = PLC.Shell.Shell(globals = globals())

    def register_functions(self):
        GeniServer.register_functions(self)
        # registry interface
        self.server.register_function(self.create_gid)
        self.server.register_function(self.get_self_credential)
        self.server.register_function(self.get_credential)
        self.server.register_function(self.get_gid)
        self.server.register_function(self.register)
        self.server.register_function(self.remove)
        self.server.register_function(self.update)
        self.server.register_function(self.list)
        self.server.register_function(self.resolve)
        # component interface
        self.server.register_function(self.get_ticket)

    def get_auth_info(self, name):
        return AuthHierarchy.get_auth_info(name)

    def get_auth_table(self, auth_name):
        auth_info = self.get_auth_info(auth_name)

        table = GeniTable(hrn=auth_name,
                          cninfo=auth_info.get_dbinfo())

        # if the table doesn't exist, then it means we haven't put any records
        # into this authority yet.

        if not table.exists():
            report.trace("Registry: creating table for authority " + auth_name)
            table.create()

        return table

    def verify_auth_belongs_to_me(self, name):
        # get_auth_info will throw an exception if the authority does not
        # exist
        self.get_auth_info(name)

    def verify_object_belongs_to_me(self, name):
        auth_name = get_authority(name)
        if not auth_name:
            # the root authority belongs to the registry by default?
            # TODO: is this true?
            return
        self.verify_auth_belongs_to_me(auth_name)

    def verify_object_permission(self, name):
        object_hrn = self.object_gid.get_hrn()
        if object_hrn == name:
            return
        if name.startswith(object_hrn + "."):
            return
        raise PermissionError(name)

    def fill_record_pl_info(self, record):
        type = record.get_type()
        pointer = record.get_pointer()

        # records with pointer==-1 do not have plc info associated with them.
        # for example, the top level authority records which are
        # authorities, but not PL "sites"
        if pointer == -1:
            return

        if (type == "sa") or (type == "ma"):
            pl_res = self.shell.GetSites(self.pl_auth, [pointer])
        elif (type == "slice"):
            pl_res = self.shell.GetSlices(self.pl_auth, [pointer])
        elif (type == "user"):
            pl_res = self.shell.GetPersons(self.pl_auth, [pointer])
        elif (type == "node"):
            pl_res = self.shell.GetNodes(self.pl_auth, [pointer])
        else:
            raise UnknownGeniType(type)

        if not pl_res:
            # the planetlab record no longer exists
            # TODO: delete the geni record ?
            raise PlanetLabRecordDoesNotExist(record.get_name())

        record.set_pl_info(pl_res[0])

    def fill_record_geni_info(self, record):
        pass

    def fill_record_info(self, record):
        self.fill_record_pl_info(record)
        self.fill_record_geni_info(record)

    def register(self, cred, record_dict):
        self.decode_authentication(cred, "register")

        record = GeniRecord(dict = record_dict)
        type = record.get_type()
        name = record.get_name()

        auth_name = get_authority(name)
        self.verify_object_permission(auth_name)
        auth_info = self.get_auth_info(auth_name)
        table = self.get_auth_table(auth_name)

        pkey = None

        # check if record already exists
        existing_records = table.resolve(type, name)
        if existing_records:
            raise ExistingRecord(name)

        if (type == "sa") or (type=="ma"):
            # update the tree
            if not AuthHierarchy.auth_exists(name):
                AuthHierarchy.create_auth(name)

            # authorities are special since they are managed by the registry
            # rather than by the caller. We create our own GID for the
            # authority rather than relying on the caller to supply one.

            # get the GID from the newly created authority
            child_auth_info = self.get_auth_info(name)
            gid = auth_info.get_gid_object()
            record.set_gid(gid.save_to_string(save_parents=True))

            geni_fields = record.get_geni_info()
            site_fields = record.get_pl_info()

            # if registering a sa, see if a ma already exists
            # if registering a ma, see if a sa already exists
            if (type == "sa"):
                other_rec = table.resolve("ma", record.get_name())
            elif (type == "ma"):
                other_rec = table.resolve("sa", record.get_name())

            if other_rec:
                print "linking ma and sa to the same plc site"
                pointer = other_rec[0].get_pointer()
            else:
                geni_fields_to_pl_fields(type, name, geni_fields, site_fields)
                print "adding site with fields", site_fields
                pointer = self.shell.AddSite(self.pl_auth, site_fields)

            record.set_pointer(pointer)

        elif (type == "slice"):
            geni_fields = record.get_geni_info()
            slice_fields = record.get_pl_info()

            geni_fields_to_pl_fields(type, name, geni_fields, slice_fields)

            pointer = self.shell.AddSlice(self.pl_auth, slice_fields)
            record.set_pointer(pointer)

        elif (type == "user"):
            geni_fields = record.get_geni_info()
            user_fields = record.get_pl_info()

            geni_fields_to_pl_fields(type, name, geni_fields, user_fields)

            pointer = self.shell.AddPerson(self.pl_auth, user_fields)
            record.set_pointer(pointer)

        elif (type == "node"):
            geni_fields = record.get_geni_info()
            node_fields = record.get_pl_info()

            geni_fields_to_pl_fields(type, name, geni_fields, node_fields)

            login_base = hrn_to_pl_login_base(auth_name)

            print "calling addnode with", login_base, node_fields
            pointer = self.shell.AddNode(self.pl_auth, login_base, node_fields)
            record.set_pointer(pointer)

        else:
            raise UnknownGeniType(type)

        table.insert(record)

        return record.get_gid_object().save_to_string(save_parents=True)

    def remove(self, cred, record_dict):
        self.decode_authentication(cred, "remove")

        record = GeniRecord(dict = record_dict)
        type = record.get_type()

        self.verify_object_permission(record.get_name())

        auth_name = get_authority(record.get_name())
        table = self.get_auth_table(auth_name)

        # let's not trust that the caller has a well-formed record (a forged
        # pointer field could be a disaster), so look it up ourselves
        record_list = table.resolve(type, record.get_name())
        if not record_list:
            raise RecordNotFound(name)
        record = record_list[0]

        # TODO: sa, ma
        if type == "user":
            self.shell.DeletePerson(self.pl_auth, record.get_pointer())
        elif type == "slice":
            self.shell.DeleteSlice(self.pl_auth, record.get_pointer())
        elif type == "node":
            self.shell.DeleteNode(self.pl_auth, record.get_pointer())
        elif (type == "sa") or (type == "ma"):
            if (type == "sa"):
                other_rec = table.resolve("ma", record.get_name())
            elif (type == "ma"):
                other_rec = table.resolve("sa", record.get_name())

            if other_rec:
                # sa and ma both map to a site, so if we are deleting one
                # but the other still exists, then do not delete the site
                print "not removing site", record.get_name(), "because either sa or ma still exists"
                pass
            else:
                print "removing site", record.get_name()
                self.shell.DeleteSite(self.pl_auth, record.get_pointer())
        else:
            raise UnknownGeniType(type)

        table.remove(record)

        return True

    def update(self, cred, record_dict):
        self.decode_authentication(cred, "update")

        record = GeniRecord(dict = record_dict)
        type = record.get_type()

        self.verify_object_permission(record.get_name())

        auth_name = get_authority(record.get_name())
        table = self.get_auth_table(auth_name)

        # make sure the record exists
        existing_record_list = table.resolve(type, record.get_name())
        if not existing_record_list:
            raise RecordNotFound(record.get_name())

        existing_record = existing_record_list[0]
        pointer = existing_record.get_pointer()

        if (type == "sa") or (type == "ma"):
            self.shell.UpdateSite(self.pl_auth, pointer, record.get_pl_info())

        elif type == "slice":
            self.shell.UpdateSlice(self.pl_auth, pointer, record.get_pl_info())

        elif type == "user":
            self.shell.UpdatePerson(self.pl_auth, pointer, record.get_pl_info())

        elif type == "node":
            self.shell.UpdateNode(self.pl_auth, pointer, record.get_pl_info())

        else:
            raise UnknownGeniType(type)

    # TODO: List doesn't take an hrn and uses the hrn contained in the
    #    objectGid of the credential. Does this mean the only way to list an
    #    authority is by having a credential for that authority? 
    def list(self, cred):
        self.decode_authentication(cred, "list")

        auth_name = self.object_gid.get_hrn()
        table = self.get_auth_table(auth_name)

        records = table.list()

        good_records = []
        for record in records:
            try:
                self.fill_record_info(record)
                good_records.append(record)
            except PlanetLabRecordDoesNotExist:
                # silently drop the ones that are missing in PL.
                # is this the right thing to do?
                report.error("ignoring geni record " + record.get_name() + " because pl record does not exist")
                table.remove(record)

        dicts = []
        for record in good_records:
            dicts.append(record.as_dict())

        return dicts

        return dict_list

    def resolve_raw(self, type, name, must_exist=True):
        auth_name = get_authority(name)

        table = self.get_auth_table(auth_name)

        records = table.resolve(type, name)

        if (not records) and must_exist:
            raise RecordNotFound(name)

        good_records = []
        for record in records:
            try:
                self.fill_record_info(record)
                good_records.append(record)
            except PlanetLabRecordDoesNotExist:
                # silently drop the ones that are missing in PL.
                # is this the right thing to do?
                report.error("ignoring geni record " + record.get_name() + " because pl record does not exist")
                table.remove(record)

        return good_records

    def resolve(self, cred, name):
        self.decode_authentication(cred, "resolve")

        records = self.resolve_raw("*", name)
        dicts = []
        for record in records:
            dicts.append(record.as_dict())

        return dicts

    def get_gid(self, name):
        self.verify_object_belongs_to_me(name)
        records = self.resolve_raw("*", name)
        gid_string_list = []
        for record in records:
            gid = record.get_gid()
            gid_string_list.append(gid.save_to_string(save_parents=True))
        return gid_string_list

    def determine_rights(self, type, name):
        rl = RightList()

        # rights seem to be somewhat redundant with the type of the credential.
        # For example, a "sa" credential implies the authority right, because
        # a sa credential cannot be issued to a user who is not an owner of
        # the authority

        if type == "user":
            rl.add("refresh")
            rl.add("resolve")
            rl.add("info")
        elif type == "sa":
            rl.add("authority")
        elif type == "ma":
            rl.add("authority")
        elif type == "slice":
            rl.add("embed")
            rl.add("bind")
            rl.add("control")
            rl.add("info")
        elif type == "component":
            rl.add("operator")

        return rl


    def get_self_credential(self, type, name):
        self.verify_object_belongs_to_me(name)

        auth_hrn = get_authority(name)
        auth_info = self.get_auth_info(auth_hrn)

        # find a record that matches
        records = self.resolve_raw(type, name, must_exist=True)
        record = records[0]

        gid = record.get_gid_object()
        peer_cert = self.server.peer_cert
        if not peer_cert.is_pubkey(gid.get_pubkey()):
           raise ConnectionKeyGIDMismatch(gid.get_subject())

        # create the credential
        gid = record.get_gid_object()
        cred = Credential(subject = gid.get_subject())
        cred.set_gid_caller(gid)
        cred.set_gid_object(gid)
        cred.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        cred.set_pubkey(gid.get_pubkey())

        rl = self.determine_rights(type, name)
        cred.set_privileges(rl)

        cred.set_parent(AuthHierarchy.get_auth_cred(auth_hrn))

        cred.encode()
        cred.sign()

        return cred.save_to_string(save_parents=True)

    def get_credential(self, cred, type, name):
        if not cred:
            return get_self_credential(self, type, name)

        self.decode_authentication(cred, "getcredential")

        self.verify_object_belongs_to_me(name)

        auth_hrn = get_authority(name)
        auth_info = self.get_auth_info(auth_hrn)

        records = self.resolve_raw(type, name, must_exist=True)
        record = records[0]

        # TODO: Check permission that self.client_cred can access the object

        object_gid = record.get_gid_object()
        new_cred = Credential(subject = object_gid.get_subject())
        new_cred.set_gid_caller(self.client_gid)
        new_cred.set_gid_object(object_gid)
        new_cred.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        new_cred.set_pubkey(object_gid.get_pubkey())

        rl = self.determine_rights(type, name)
        new_cred.set_privileges(rl)

        new_cred.set_parent(AuthHierarchy.get_auth_cred(auth_hrn))

        new_cred.encode()
        new_cred.sign()

        return new_cred.save_to_string(save_parents=True)

    def create_gid(self, cred, name, uuid, pubkey_str):
        self.decode_authentication(cred, "getcredential")

        self.verify_object_belongs_to_me(name)

        self.verify_object_permission(name)

        if uuid == None:
            uuid = create_uuid()

        pkey = Keypair()
        pkey.load_pubkey_from_string(pubkey_str)
        gid = AuthHierarchy.create_gid(name, uuid, pkey)

        return gid.save_to_string(save_parents=True)

    # ------------------------------------------------------------------------
    # Component Interface

    def record_to_slice_info(self, record):

        # get the user keys from the slice
        keys = []
        persons = self.shell.GetPersons(self.pl_auth, record.pl_info['person_ids'])
        for person in persons:
            person_keys = self.shell.GetKeys(self.pl_auth, person["key_ids"])
            for person_key in person_keys:
                keys = keys + [person_key['key']]

        attributes={}
        attributes['name'] = record.pl_info['name']
        attributes['keys'] = keys
        attributes['instantiation'] = record.pl_info['instantiation']
        attributes['vref'] = 'default'
        attributes['timestamp'] = time.time()

        rspec = {}

        # get the PLC attributes and separate them into slice attributes and
        # rspec attributes
        filter = {}
        filter['slice_id'] = record.pl_info['slice_id']
        plc_attrs = self.shell.GetSliceAttributes(self.pl_auth, filter)
        for attr in plc_attrs:
            name = attr['name']

            # initscripts: lookup the contents of the initscript and store it
            # in the ticket attributes
            if (name == "initscript"):
                filter={'name': attr['value']}
                initscripts = self.shell.GetInitScripts(self.pl_auth, filter)
                if initscripts:
                    attributes['initscript'] = initscripts[0]['script']
            else:
                rspec[name] = attr['value']

        return (attributes, rspec)


    def get_ticket(self, cred, name, rspec):
        self.decode_authentication(cred, "getticket")

        self.verify_object_belongs_to_me(name)

        self.verify_object_permission(name)

        # XXX much of this code looks like get_credential... are they so similar
        # that they should be combined?

        auth_hrn = get_authority(name)
        auth_info = self.get_auth_info(auth_hrn)

        records = self.resolve_raw("slice", name, must_exist=True)
        record = records[0]

        object_gid = record.get_gid_object()
        new_ticket = Ticket(subject = object_gid.get_subject())
        new_ticket.set_gid_caller(self.client_gid)
        new_ticket.set_gid_object(object_gid)
        new_ticket.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        new_ticket.set_pubkey(object_gid.get_pubkey())

        self.fill_record_info(record)

        (attributes, rspec) = self.record_to_slice_info(record)

        new_ticket.set_attributes(attributes)
        new_ticket.set_rspec(rspec)

        new_ticket.set_parent(AuthHierarchy.get_auth_ticket(auth_hrn))

        new_ticket.encode()
        new_ticket.sign()

        return new_ticket.save_to_string(save_parents=True)


if __name__ == "__main__":
    global AuthHierarchy
    global TrustedRoots

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

    AuthHierarchy = Hierarchy()

    TrustedRoots = TrustedRootList()

    s = Registry("", 12345, key_file, cert_file)
    s.trusted_cert_list = TrustedRoots.get_list()
    s.run()

