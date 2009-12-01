### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.trust.credential import Credential

class delete_slice(Method):
    """
    Remove the slice from all nodes.      

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name specifying the slice to delete
    @return 1 if successful, faults otherwise  
    """

    interfaces = ['aggregate', 'slicemgr', 'component']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to delete"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, hrn, request_hash=None, caller_cred=None):
       
        if caller_cred==None:
            caller_cred=cred
        #log the call
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, Credential(string=caller_cred).get_gid_caller().get_hrn(), hrn, self.name))

        # This cred will be an slice cred, not a user, so we cant use it to
        # authenticate the caller's request_hash. Let just get the caller's gid
        # from the cred and authenticate using that
        client_gid = Credential(string=cred).get_gid_caller()
        client_gid_str = client_gid.save_to_string(save_parents=True)
        self.api.auth.authenticateGid(client_gid_str, [cred, hrn], request_hash)
        self.api.auth.check(cred, 'deleteslice')

        
        # send the call to the right manager
        manager_base = 'sfa.managers'
        if self.api.interface in ['component']:
            mgr_type = self.api.config.SFA_CM_TYPE
            manager_module = manger_base+= ".component_manager_%s" % mgr_type
            manager = __import__(manager_module, manager_base)
            manager.delete_slice(self.api, hrn)
        elif self.api.interface in ['aggregate']:
            mgr_type = self.api.config.SFA_AGGREGATE_TYPE
            manager_module = manger_base+= ".agregate_manager_%s" % mgr_type
            manager = __import__(manager_module, manager_base)
            manager.delete_slice(self.api, hrn)
        elif self.api.interface in ['slicemngr']:        
            mgr_type = self.api.config.SFA_SM_TYPE
            manager_module = manger_base+= ".slice_manager_%s" % mgr_type
            manager = __import__(manager_module, manager_base)
            manager.delete_slice(self.api, hrn)

        return 1
