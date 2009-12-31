### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.plc.slices import Slices
from sfa.trust.credential import Credential

class get_slices(Method):
    """
    Get a list of instantiated slices at this authority.      

    @param cred credential string specifying the rights of the caller
    @return list of human readable slice names (hrn).  
    """

    interfaces = ['aggregate', 'slicemgr', 'component']
    
    accepts = [
        Parameter(str, "Credential string"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = [Parameter(str, "Human readable slice name (hrn)")]
    
    def call(self, cred, request_hash=None):
        user_cred = Credential(string=cred)
        #log the call
        gid_origin_caller = user_cred.get_gid_origin_caller()
        origin_hrn = gid_origin_caller.get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn(), None, self.name))

        self.api.auth.authenticateCred(cred, [cred], request_hash) 
        self.api.auth.check(cred, 'listslices')

        slices = []
        # send the call to the right manager 
        manager_base = 'sfa.managers'
        if self.api.interface in ['component']:
            mgr_type = self.api.config.SFA_CM_TYPE
            manager_module = manager_base + ".component_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            slices = manager.get_slices(self.api)
        elif self.api.interface in ['aggregate']:
            mgr_type = self.api.config.SFA_AGGREGATE_TYPE
            manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            slices = manager.get_slices(self.api)
        elif self.api.interface in ['slicemgr']:
            mgr_type = self.api.config.SFA_SM_TYPE
            manager_module = manager_base + ".slice_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            slices = manager.get_slices(self.api)

        return slices
