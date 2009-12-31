### $Id$
### $URL$

from sfa.trust.credential import *
from sfa.trust.rights import *
from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.trust.gid import GID
from sfa.util.record import GeniRecord
from sfa.util.genitable import *
from sfa.util.debug import log

class get_credential(Method):
    """
    Retrive a credential for an object
    If cred == Nonee then the behavior reverts to get_self_credential

    @param cred credential object specifying rights of the caller
    @param type type of object (user | slice | sa | ma | node)
    @param hrn human readable name of object
    @param origin_hrn human readable name of calls origin 

    @return the string representation of a credential object  
    """

    interfaces = ['registry']
    
    accepts = [
        Mixed(Parameter(str, "credential"),
              Parameter(None, "No credential")),  
        Parameter(str, "Human readable name (hrn)"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified")),
        Parameter(str, "Human readable name (hrn)"),
        ]

    returns = Parameter(str, "String representation of a credential object")

    def call(self, cred, type, hrn, origin_hrn=None, request_hash=None):

        self.api.auth.authenticateCred(cred, [cred, type, hrn], request_hash)
        self.api.auth.check(cred, 'getcredential')
        self.api.auth.verify_object_belongs_to_me(hrn)
        auth_hrn = self.api.auth.get_authority(hrn)

        # Is this a root or sub authority 
        if not auth_hrn or hrn == self.api.config.SFA_INTERFACE_HRN:
            auth_hrn = hrn

        # get record info
        auth_info = self.api.auth.get_auth_info(auth_hrn)
        table = GeniTable()
        records = table.find({'type': type, 'hrn': hrn})
        if not records:
            raise RecordNotFound(hrn)
        record = records[0]
        
        # get the origin caller's gid (this is the caller's gid by default)    
        if origin_hrn:
            orgin_records = table.find({'hrn': origin_hrn})
            if not origin_records:
                raise RecordNotFound(origin_hrn)
            origin_record = origin_records[0]
            origin_caller_gid_object = GID(string = record['gid'])
        else:
            origin_caller_gid_object = self.api.auth.client_gid

        
        # verify_cancreate_credential requires that the member lists
        # (researchers, pis, etc) be filled in
        self.api.fill_record_info(record)

        caller_hrn = self.api.auth.client_cred.get_gid_caller().get_hrn()
        rights = self.api.auth.determine_user_rights(caller_hrn, record)
        if rights.is_empty():
            raise PermissionError(self.api.auth.client_cred.get_gid_object().get_hrn() + " has no rights to " + record['name'])

        # TODO: Check permission that self.client_cred can access the object

        gid = record['gid']
        gid_object = GID(string=gid)

        new_cred = Credential(subject = gid_object.get_subject())
        new_cred.set_gid_caller(self.api.auth.client_gid)
        new_cred.set_gid_origin_caller(origin_caller_gid_object)
        new_cred.set_gid_object(gid_object)
        new_cred.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        new_cred.set_pubkey(gid_object.get_pubkey())
        new_cred.set_privileges(rights)
        new_cred.set_delegate(True)

        auth_kind = "authority,ma,sa"
        new_cred.set_parent(self.api.auth.hierarchy.get_auth_cred(auth_hrn, kind=auth_kind))

        new_cred.encode()
        new_cred.sign()

        return new_cred.save_to_string(save_parents=True)

