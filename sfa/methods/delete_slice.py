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
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Paramater(None, "Origin hrn not specified"))
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, hrn, origin_hrn=None):
        user_cred = Credential(string=cred)
        
        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))

        # validate the credential
        self.api.auth.check(cred, 'deleteslice')

        # send the call to the right manager
        manager_base = 'sfa.managers'
        if self.api.interface in ['component']:
            mgr_type = self.api.config.SFA_CM_TYPE
            manager_module = manager_base + ".component_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            manager.delete_slice(self.api, hrn)
        elif self.api.interface in ['aggregate']:
            mgr_type = self.api.config.SFA_AGGREGATE_TYPE
            manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            manager.delete_slice(self.api, hrn)
        elif self.api.interface in ['slicemgr']:        
            mgr_type = self.api.config.SFA_SM_TYPE
            manager_module = manager_base + ".slice_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            manager.delete_slice(self.api, hrn, origin_hrn)

        return 1
