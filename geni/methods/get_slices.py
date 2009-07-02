### $Id$
### $URL$

from geni.util.faults import *
from geni.util.misc import *
from geni.util.method import Method
from geni.util.parameter import Parameter, Mixed
from geni.util.auth import Auth
from geni.util.slices import Slices

class get_slices(Method):
    """
    Get a list of instantiated slices at this authority.      

    @param cred credential string specifying the rights of the caller
    @return list of human readable slice names (hrn).  
    """

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        ]

    returns = [Parameter(str, "Human readable slice name (hrn)")]
    
    def call(self, cred):
       
        self.api.auth.check(cred, 'listslices')
        slices = Slices(self.api)
        slices.refresh()    
        return slices['hrn']
