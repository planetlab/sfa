### $Id$
### $URL$

from geni.util.faults import *
from geni.util.misc import *
from geni.util.method import Method
from geni.util.parameter import Parameter, Mixed
from geni.util.auth import Auth

from geni.util.slices import Slices
from geni.aggregate import Aggregates

class delete_slice(Method):
    """
    Remove the slice from all nodes.      

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name specifying the slice to delete
    @return 1 if successful, faults otherwise  
    """

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to delete"),
        ]

    returns = [Parameter(int, "1 if successful")]
    
    def call(self, cred, hrn):
       
        self.api.auth.check(cred, 'deleteslice')
        slices = Slices(self.api)
        slices.delete_slice(hrn)
        return 1
