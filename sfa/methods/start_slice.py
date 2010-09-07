### $Id: start_slice.py 18566 2010-08-03 22:24:42Z tmack $
### $URL: http://svn.planet-lab.org/svn/sfa/trunk/sfa/methods/start_slice.py $

from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.methods.Start import Start

class start_slice(Start):
    """
    Deprecated. Use Start instead

    Start the specified slice      

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name of slice to instantiate (urn or hrn)
    @return 1 is successful, faults otherwise  
    """

    interfaces = ['aggregate', 'slicemgr', 'component']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to instantiate (urn or hrn)"),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = [Parameter(int, "1 if successful")]
    
    def call(self, cred, xrn, origin_hrn=None):
 
        return Start.call(self, xrn, cred) 
