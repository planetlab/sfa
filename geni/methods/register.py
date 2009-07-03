### $Id$
### $URL$

from geni.util.faults import *
from geni.util.method import Method
from geni.util.parameter import Parameter, Mixed
from geni.util.auth import Auth
from geni.util.record import GeniRecord
from geni.trust.certificate import Keypair, convert_public_key
from geni.trust.gid import *
from geni.util.debug import log
from geni.util.misc import *

class register(Method):
    """
    Register an object with the registry. In addition to being stored in the
    Geni database, the appropriate records will also be created in the
    PLC databases
    
    @param cred credential string
    @param record_dict dictionary containing record fields
    
    @return gid string representation
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(dict, "Record dictionary containing record fields")
        ]

    returns = Parameter(int, "String representation of gid object")
    
    def call(self, cred, record_dict):
        self.api.auth.check(cred, "register")
        record = GeniRecord(dict = record_dict)
        type = record.get_type()
        name = record.get_name()
        self.api.auth.verify_object_permission(name)
        auth_name = self.api.auth.get_authority(name)
        auth_info = self.api.auth.get_auth_info(auth_name)
        table = self.api.auth.get_auth_table(auth_name)
        
        # make sure record has a gid
        if 'gid' not in record:
            uuid = create_uuid()
            pkey = Keypair(create=True)
            if 'keys' in record and record['keys']:
                pkey = convert_public_key(record['keys'][0])
            
            gid_object = self.api.auth.hierarchy.create_gid(name, uuid, pkey)
            gid = gid_object.save_to_string(save_parents=True)
            record['gid'] = gid
            record.set_gid(gid)

        # check if record already exists
        existing_records = table.resolve(type, name)
        if existing_records:
            raise ExistingRecord(name)
        
        if (type == "sa") or (type=="ma"):
            # update the tree
            if not self.api.auth.hierarchy.auth_exists(name):
                self.api.auth.hierarchy.create_auth(name)

            # authorities are special since they are managed by the registry
            # rather than by the caller. We create our own GID for the
            # authority rather than relying on the caller to supply one.

            # get the GID from the newly created authority
            child_auth_info = self.api.auth.get_auth_info(name)
            gid = auth_info.get_gid_object()
            record.set_gid(gid.save_to_string(save_parents=True))

            # if registering a sa, see if a ma already exists
            # if registering a ma, see if a sa already exists
            if (type == "sa"):
                other_rec = table.resolve("ma", record.get_name())
            elif (type == "ma"):
                other_rec = table.resolve("sa", record.get_name())

            if other_rec:
                print >> log, "linking ma and sa to the same plc site"
                pointer = other_rec[0].get_pointer()
            else:
                pl_record = self.api.geni_fields_to_pl_fields(type, name, record)
                print >> log, "adding site with fields", pl_record
                pointer = self.api.plshell.AddSite(self.api.plauth, pl_record)

            record.set_pointer(pointer)

        elif (type == "slice"):
            pl_record = self.api.geni_fields_to_pl_fields(type, name, record)
            pointer = self.api.plshell.AddSlice(self.api.plauth, pl_record)
            record.set_pointer(pointer)

        elif (type == "user"):
            pointer = self.api.plshell.AddPerson(self.api.plauth, dict(record))
            if 'enabled' in record and record['enabled']:
                self.api.plshell.UpdatePerson(self.api.plauth, pointer, {'enabled': record['enabled']})
            login_base = get_leaf(auth_info.hrn)
            self.api.plshell.AddPersonToSite(self.api.plauth, pointer, login_base)
            # What roles should this user have?
            self.api.plshell.AddRoleToPerson(self.api.plauth, 'user', pointer) 
            record.set_pointer(pointer)
	    
	    # Add the user's key
            if record['keys']:
		self.api.plshell.AddPersonKey(self.api.plauth, pointer, {'key_type' : 'ssh', 'key' : record['keys'][0]})

        elif (type == "node"):
            pl_record = self.api.geni_fields_to_pl_fields(type, name, record)
            login_base = hrn_to_pl_login_base(auth_name)
            pointer = self.api.plshell.AddNode(self.api.plauth, login_base, pl_record)
            record.set_pointer(pointer)

        else:
            raise UnknownGeniType(type)

        table.insert(record)

        # update membership for researchers, pis, owners, operators
        self.api.update_membership(None, record)

        return record.get_gid_object().save_to_string(save_parents=True)
