### $Id$
### $URL$

from sfa.trust.certificate import Keypair, convert_public_key
from sfa.trust.gid import *

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.record import GeniRecord
from sfa.util.debug import log

from sfa.trust.auth import Auth
from sfa.trust.gid import create_uuid

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
            if 'key' in record and record['key']:
                pkey = convert_public_key(record['key'])
            
            gid_object = self.api.auth.hierarchy.create_gid(name, uuid, pkey)
            gid = gid_object.save_to_string(save_parents=True)
            record['gid'] = gid
            record.set_gid(gid)

        # check if record already exists
        existing_records = table.resolve(type, name)
        if existing_records:
            raise ExistingRecord(name)
        
        if type in ["authority"]:
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

            pl_record = self.api.geni_fields_to_pl_fields(type, name, record)
            sites = self.api.plshell.GetSites(self.api.plauth, [pl_record['login_base']])
            if not sites:    
                pointer = self.api.plshell.AddSite(self.api.plauth, pl_record)
            else:
                pointer = sites[0]['site_id']

            record.set_pointer(pointer)

        elif (type == "slice"):
            pl_record = self.api.geni_fields_to_pl_fields(type, name, record)
            slices = self.api.plshell.GetSlices(self.api.plauth, [pl_record['name']])
            if not slices: 
                pointer = self.api.plshell.AddSlice(self.api.plauth, pl_record)
            else:
                pointer = slices[0]['slice_id']
            record.set_pointer(pointer)

        elif (type == "user"):
            persons = self.api.plshell.GetPersons(self.api.plauth, [record['email']])
            if not persons:
                pointer = self.api.plshell.AddPerson(self.api.plauth, dict(record))
            else:
                pointer = persons[0]['person_id']
 
            if 'enabled' in record and record['enabled']:
                self.api.plshell.UpdatePerson(self.api.plauth, pointer, {'enabled': record['enabled']})
            login_base = get_leaf(auth_info.hrn)
            self.api.plshell.AddPersonToSite(self.api.plauth, pointer, login_base)
            # What roles should this user have?
            self.api.plshell.AddRoleToPerson(self.api.plauth, 'user', pointer) 
            record.set_pointer(pointer)
	    
	    # Add the user's key
            if 'key' in record and record['key']:
                self.api.plshell.AddPersonKey(self.api.plauth, pointer, {'key_type' : 'ssh', 'key' : record['key']})

        elif (type == "node"):
            pl_record = self.api.geni_fields_to_pl_fields(type, name, record)
            login_base = hrn_to_pl_login_base(auth_name)
            nodes = self.api.plshell.GetNodes(self.api.plauth, [pl_record['hostname']])
            if not nodes:
                pointer = self.api.plshell.AddNode(self.api.plauth, login_base, pl_record)
            else:
                pointer = nodes[0]['node_id']
            record.set_pointer(pointer)

        else:
            raise UnknownGeniType(type)

        # SFA upcalls may exist in PLCAPI and they could have already added the
        # record for us. Lets check if the record already exists  
        existing_records = table.resolve(type, name)
        if not existing_records:
            table.insert(record)

        # update membership for researchers, pis, owners, operators
        self.api.update_membership(None, record)

        return record.get_gid_object().save_to_string(save_parents=True)
