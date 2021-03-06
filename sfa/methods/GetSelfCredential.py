
from sfa.util.faults import *
from sfa.util.xrn import urn_to_hrn
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.record import SfaRecord
from sfa.trust.credential import Credential
from sfa.trust.certificate import Certificate
from sfa.trust.rights import Right, Rights

class GetSelfCredential(Method):
    """
    Retrive a credential for an object
    @param cert certificate string 
    @param type type of object (user | slice | sa | ma | node)
    @param hrn human readable name of object (hrn or urn)

    @return the string representation of a credential object  
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "certificate"),
        Parameter(str, "Human readable name (hrn or urn)"),
        Mixed(Parameter(str, "Record type"),
              Parameter(None, "Type not specified")),
        ]

    returns = Parameter(str, "String representation of a credential object")

    def call(self, cert, xrn, type):
        """
        GetSelfCredential a degenerate version of GetCredential used by a client
        to get his initial credential when de doesnt have one. This is the same as
        GetCredential(..., cred = None, ...)

        The registry ensures that the client is the principal that is named by
        (type, name) by comparing the public key in the record's  GID to the
        private key used to encrypt the client side of the HTTPS connection. Thus
        it is impossible for one principal to retrieve another principal's
        credential without having the appropriate private key.

        @param type type of object (user | slice | sa | ma | node)
        @param hrn human readable name of authority to list
        @return string representation of a credential object
        """
        if type:
            hrn = urn_to_hrn(xrn)[0]
        else:
            hrn, type = urn_to_hrn(xrn) 
        self.api.auth.verify_object_belongs_to_me(hrn)

        origin_hrn = Certificate(string=cert).get_subject()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))
        
        manager = self.api.get_interface_manager()
 
        # authenticate the gid
        records = manager.resolve(self.api, xrn, type)
        if not records:
            raise RecordNotFound(hrn)
        record = SfaRecord(dict=records[0])
        gid = record.get_gid_object()
        gid_str = gid.save_to_string(save_parents=True)
        self.api.auth.authenticateGid(gid_str, [cert, type, hrn])
        # authenticate the certificate against the gid in the db
        certificate = Certificate(string=cert)
        if not certificate.is_pubkey(gid.get_pubkey()):
            for (obj,name) in [ (certificate,"CERT"), (gid,"GID"), ]:
                self.api.logger.debug("ConnectionKeyGIDMismatch, %s pubkey: %s"%(name,obj.get_pubkey().get_pubkey_string()))
                self.api.logger.debug("ConnectionKeyGIDMismatch, %s dump: %s"%(name,obj.dump_string()))
                if hasattr (obj,'filename'): 
                    self.api.logger.debug("ConnectionKeyGIDMismatch, %s filename: %s"%(name,obj.filename))
            raise ConnectionKeyGIDMismatch(gid.get_subject())
        
        return manager.get_credential(self.api, xrn, type, is_self=True)
