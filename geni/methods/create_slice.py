from geni.util.faults import *
from geni.util.excep import *
from geni.util.misc import *
from geni.util.method import Method
from geni.util.parameter import Parameter, Mixed
from geni.util.auth import Auth
from geni.util.slices import Slices

class create_slices(Method):
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

    returns = [Parameter(int, "1 if successful")]
    
    def call(self, cred, hrn, rspec):
       
        self.api.auth.check(cred, 'createslice')
        slices = Slices(self.api)
        slices.create_slice(hrn, rspec):
        
        return 1 
