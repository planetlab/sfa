#
# GeniAPI authentication 
#
#

import time
from geni.util.faults import *
from geni.util.excep import *
from geni.util.credential import Credential
from geni.util.trustedroot import TrustedRootList
from geni.util.hierarchy import Hierarchy
from geni.util.rights import RightList
from geni.util.genitable import *
from geni.util.config import *

class Auth:
    """
    Credential based authentication
    """

    def __init__(self, peer_cert = None, config = None ):
        self.peer_cert = peer_cert
        self.hierarchy = Hierarchy()
        self.trusted_cert_list = TrustedRootList().get_list() 
        if not config:
            self.config = Config() 
    

    def check(self, cred, operation):
        """
        Check the credential against the peer cert (callerGID included 
        in the credential matches the caller that is connected to the 
        HTTPS connection, check if the credential was signed by a 
        trusted cert and check if the credential is allowd to perform 
        the specified operation.    
        """
        self.client_cred = Credential(string = cred)
        self.client_gid = self.client_cred.get_gid_caller()
        self.object_gid = self.client_cred.get_gid_object()
        
        # make sure the client_gid is not blank
        if not self.client_gid:
            raise MissingCallerGID(self.client_cred.get_subject())

        # make sure the client_gid matches client's certificate
        peer_cert = self.peer_cert
        if not peer_cert.is_pubkey(self.client_gid.get_pubkey()):
            raise ConnectionKeyGIDMismatch(self.client_gid.get_subject())

        # make sure the client is allowed to perform the operation
        if operation:
            if not self.client_cred.can_perform(operation):
                raise InsufficientRights(operation)

        if self.trusted_cert_list:
            self.client_cred.verify_chain(self.trusted_cert_list)
            if self.client_gid:
                self.client_gid.verify_chain(self.trusted_cert_list)
            if self.object_gid:
                self.object_gid.verify_chain(self.trusted_cert_list)

        return True

        
    def get_auth_info(self, auth_hrn):
        """
        Given an authority name, return the information for that authority.
        This is basically a stub that calls the hierarchy module.
        
        @param auth_hrn human readable name of authority  
        """

        return self.hierarchy.get_auth_info(auth_hrn)


    def get_auth_table(self, auth_name):
        """
        Given an authority name, return the database table for that authority.
        If the databse table does not exist, then one will be automatically
        created.

        @param auth_name human readable name of authority
        """
        auth_info = self.get_auth_info(auth_name)
        table = GeniTable(hrn=auth_name,
                          cninfo=auth_info.get_dbinfo())
        # if the table doesn't exist, then it means we haven't put any records
        # into this authority yet.

        if not table.exists():
            print >> log, "Registry: creating table for authority", auth_name
            table.create()
    
        return table

    def veriry_auth_belongs_to_me(self, name):
        """
        Verify that an authority belongs to our hierarchy. 
        This is basically left up to the implementation of the hierarchy
        module. If the specified name does not belong, ane exception is 
        thrown indicating the caller should contact someone else.

        @param auth_name human readable name of authority
        """

        self.get_auth_info(name)


    def verify_object_belongs_to_me(self, name):
        """
        Verify that an object belongs to our hierarchy. By extension,
        this implies that the authority that owns the object belongs
        to our hierarchy. If it does not an exception is thrown.
    
        @param name human readable name of object        
        """
        auth_name = self.get_authority(name)
        if not auth_name:
            # the root authority belongs to the registry by default?
            # TODO: is this true?
            return
        self.verify_auth_belongs_to_me(auth_name) 
             
    def verify_auth_belongs_to_me(self, name):
        # get auth info will throw an exception if the authority doesnt exist
        self.get_auth_info(name) 


    def verify_object_permission(self, name):
        """
        Verify that the object gid that was specified in the credential
        allows permission to the object 'name'. This is done by a simple
        prefix test. For example, an object_gid for plc.arizona would 
        match the objects plc.arizona.slice1 and plc.arizona.
    
        @param name human readable name to test  
        """
        object_hrn = self.object_gid.get_hrn()
        if object_hrn == name:
            return
        if name.startswith(object_hrn + "."):
            return
        raise PermissionError(name)

    def determine_user_rights(self, src_cred, record):
        """
        Given a user credential and a record, determine what set of rights the
        user should have to that record.

        Src_cred can be None when obtaining a user credential, but should be
        set to a valid user credential when obtaining a slice or authority
        credential.

        This is intended to replace determine_rights() and
        verify_cancreate_credential()
        """

        type = record.get_type()
        if src_cred:
            cred_object_hrn = src_cred.get_gid_object().get_hrn()
        else:
            # supplying src_cred==None is only valid when obtaining user
            # credentials.
            #assert(type == "user")
            
            cred_object_hrn = None

        rl = RightList()

        if type=="slice":
            researchers = record.get("researcher", [])
            if (cred_object_hrn in researchers):
                rl.add("refresh")
                rl.add("embed")
                rl.add("bind")
                rl.add("control")
                rl.add("info")

        elif type == "authority":
            pis = record.get("pi", [])
            operators = record.get("operator", [])
            rl.add("authority,sa,ma")
            if (cred_object_hrn in pis):
                rl.add("sa")
            if (cred_object_hrn in operators):
                rl.add("ma")

        elif type == "user":
            rl.add("refresh")
            rl.add("resolve")
            rl.add("info")

        return rl

    def verify_cancreate_credential(self, src_cred, record):
        """
        Verify that a user can retrive a particular type of credential.
        For slices, the user must be on the researcher list. For SA and
        MA the user must be on the pi and operator lists respectively
        """

        type = record.get_type()
        cred_object_hrn = src_cred.get_gid_object().get_hrn()
        if cred_object_hrn in [self.config.GENI_REGISTRY_ROOT_AUTH]:
            return
        if type=="slice":
            researchers = record.get("researcher", [])
            if not (cred_object_hrn in researchers):
                raise PermissionError(cred_object_hrn + " is not in researcher list for " + record.get_name())
        elif type == "sa":
            pis = record.get("pi", [])
            if not (cred_object_hrn in pis):
                raise PermissionError(cred_object_hrn + " is not in pi list for " + record.get_name())
        elif type == "ma":
            operators = record.get("operator", [])
            if not (cred_object_hrn in operators):
                raise PermissionError(cred_object_hrn + " is not in operator list for " + record.get_name())

    def get_leaf(self, hrn):
        parts = hrn.split(".")
        return ".".join(parts[-1:])

    def get_authority(self, hrn):
        parts = hrn.split(".")
        return ".".join(parts[:-1])

    def hrn_to_pl_slicename(self, hrn):
        parts = hrn.split(".")
        return parts[-2] + "_" + parts[-1]

    # assuming hrn is the hrn of an authority, return the plc authority name
    def hrn_to_pl_authname(self, hrn):
        parts = hrn.split(".")
        return parts[-1]

    # assuming hrn is the hrn of an authority, return the plc login_base
    def hrn_to_pl_login_base(self, hrn):
        return self.hrn_to_pl_authname(hrn)
      
