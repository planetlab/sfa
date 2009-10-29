### $Id: get_credential.py 15321 2009-10-15 05:01:21Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/methods/get_credential.py $

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

class get_self_credential(Method):
    """
    Retrive a credential for an object
    @param cert certificate string 
    @param type type of object (user | slice | sa | ma | node)
    @param hrn human readable name of object

    @return the string representation of a credential object  
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "certificate"),
        Parameter(str, "Human readable name (hrn)"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = Parameter(str, "String representation of a credential object")

    def call(self, cert, type, hrn, request_hash=None):
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
         
        # if this is a root or sub authority get_authority will return
        # an empty string
        if not auth_hrn or hrn == self.api.config.SFA_INTERFACE_HRN:
            auth_hrn = hrn

        auth_info = self.api.auth.get_auth_info(auth_hrn)

        # find a record that matches
        record = None
        table = GeniTable()
        records = table.findObjects({'type': type, 'hrn':  hrn})
        if not records:
            raise RecordNotFound(hrn)
        record = records[0]
        
        # authenticate the gid
        gid = record.get_gid_object()
        gid_str = gid.save_to_string(save_parents=True)
        self.api.auth.authenticateGid(gid_str, [cert, type, hrn], request_hash)
        
        # authenticate the certificate against the gid in the db
        certificate = Certificate(string=cert)
        if not certificate.is_pubkey(gid.get_pubkey()):
            raise ConnectionKeyGIDMismatch(gid.get_subject())

        # get the right of this record    
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
