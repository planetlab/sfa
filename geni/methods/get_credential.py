from geni.util.faults import *
from geni.util.excep import *
from geni.util.method import Method
from geni.util.parameter import Parameter, Mixed
from geni.util.auth import Auth
from geni.util.record import GeniRecord
from geni.util.credential import *
from geni.util.rights import *
from geni.util.debug import log

class get_credential(Method):
    """
    Retrive a credential for an object
    If cred == Nonee then the behavior reverts to get_self_credential

    @param cred credential object specifying rights of the caller
    @param type type of object (user | slice | sa | ma | node)
    @param hrn human readable name of object

    @return the string representation of a credential object  
    """

    interfaces = ['registry']
    
    accepts = [
        Mixed(Parameter(str, "credential"),
              Parameter(None, "No credential")),  
        Parameter(str, "Human readable name (hrn)")
        ]

    returns = Parameter(str, "String representation of a credential object")

    def call(self, cred, type, hrn):
        if not cred:
            return self.get_self_credential(type, hrn)

        self.api.auth.check(cred, 'getcredential')
        self.api.auth.verify_object_belongs_to_me(hrn)
        auth_hrn = self.api.auth.get_authority(hrn)
        if not auth_hrn:
            auth_hrn = hrn
        auth_info = self.api.auth.get_auth_info(auth_hrn)
        table = self.api.auth.get_auth_table(auth_hrn)
        records = table.resolve('*', hrn)
        if not records:
            raise RecordNotFound(hrn)
        record = records[0]
        # verify_cancreate_credential requires that the member lists
        # (researchers, pis, etc) be filled in
        self.api.fill_record_info(record)

        rights = self.api.auth.determine_user_rights(self.api.auth.client_cred, record)
        if rights.is_empty():
            raise PermissionError(self.api.auth.client_cred.get_gid_object().get_hrn() + " has no rights to " + record.get_name())

        # TODO: Check permission that self.client_cred can access the object

        object_gid = record.get_gid_object()
        new_cred = Credential(subject = object_gid.get_subject())
        new_cred.set_gid_caller(self.api.auth.client_gid)
        new_cred.set_gid_object(object_gid)
        new_cred.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        new_cred.set_pubkey(object_gid.get_pubkey())
        new_cred.set_privileges(rights)
        new_cred.set_delegate(True)

        auth_kind = "authority,ma,sa"
        new_cred.set_parent(self.api.auth.hierarchy.get_auth_cred(auth_hrn, kind=auth_kind))

        new_cred.encode()
        new_cred.sign()

        return new_cred.save_to_string(save_parents=True)

    def get_self_credential(self, type, hrn):
        """
        get_self_credential a degenerate version of get_credential used by a client
        to get his initial credential when de doesnt have one. This is the same as
        get_credetial(..., cred = None, ...)

        The registry ensures that the client is the principal that is named by
        (type, name) by comparing the public key in the record's  GID to the
        private key used to encrypt the client side of the HTTPS connection. Thus
        it is impossible for one principal to retrive another principal's
        credential without having the appropriate private key.

        @param type type of object (user | slice | sa | ma | node)
        @param hrn human readable name of authority to list
        @return string representation of a credential object
        """
        self.api.auth.verify_object_belongs_to_me(hrn)

        auth_hrn = self.api.auth.get_authority(hrn)
        if not auth_hrn:
            auth_hrn = hrn
        auth_info = self.api.auth.get_auth_info(auth_hrn)

        # find a record that matches
        record = None
        table = self.api.auth.get_auth_table(auth_hrn)
        records = table.resolve('*', hrn)
        for rec in records:
            if type in ['*'] or rec.get_type() in [type]:
                record = rec
        if not record:
            raise RecordNotFound(hrn)
        gid = record.get_gid_object()
        peer_cert = self.api.auth.peer_cert
        if not peer_cert.is_pubkey(gid.get_pubkey()):
           raise ConnectionKeyGIDMismatch(gid.get_subject())

        rights = self.api.auth.determine_user_rights(None, record)
        if rights.is_empty():
            raise PermissionError(gid.get_hrn() + " has no rights to " + record.get_name())

        # create the credential
        gid = record.get_gid_object()
        cred = Credential(subject = gid.get_subject())
        cred.set_gid_caller(gid)
        cred.set_gid_object(gid)
        cred.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        cred.set_pubkey(gid.get_pubkey())
        cred.set_privileges(rights)
        cred.set_delegate(True)

        auth_kind = "authority,sa,ma"
        cred.set_parent(self.api.auth.hierarchy.get_auth_cred(auth_hrn, kind=auth_kind))

        cred.encode()
        cred.sign()

        return cred.save_to_string(save_parents=True)
