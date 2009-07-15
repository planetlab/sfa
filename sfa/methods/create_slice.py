### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.plc.slices import Slices
# RSpecManager_pl is not used. This is just to resolve issues with the dynamic __import__ that comes later.
import sfa.rspecs.aggregates.rspec_manager_pl


class create_slice(Method):
    """
    Instantiate the specified slice according to whats defined in the specified rspec      

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name of slice to instantiate
    @param rspec resource specification
    @return 1 is successful, faults otherwise  
    """

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to instantiate"),
        Parameter(str, "Resource specification"),
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, hrn, rspec):
        sfa_aggregate_type = Config().get_aggregate_rspec_type()
        if (sfa_aggregate_type == 'pl'):
            self.api.auth.check(cred, 'createslice')
            slices = Slices(self.api)
            slices.create_slice(hrn, rspec)    
        else:
            # To clean up after July 21 - SB    
            rspec_manager = __import__("sfa.rspecs.aggregates.rspec_manager_"+sfa_aggregate_type)
            rspec = rspec_manager.create_slice(hrn, rspec)
        
        return 1 
