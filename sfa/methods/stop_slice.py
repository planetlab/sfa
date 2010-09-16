### $Id: stop_slice.py 18567 2010-08-03 22:25:05Z tmack $
### $URL: http://svn.planet-lab.org/svn/sfa/trunk/sfa/methods/stop_slice.py $

from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.methods.Stop import Stop

class stop_slice(Stop):
    """
    Deprecated. Use Stop instead
    Stop the specified slice      

    @param cred credential string specifying the rights of the caller
    @param xrn human readable name of slice to instantiate (hrn or urn)
    @return 1 is successful, faults otherwise  
    """

    interfaces = ['aggregate', 'slicemgr', 'component']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to instantiate (hrn or urn)"),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, xrn, origin_hrn=None):
 
        return Stop.call(self, xrn, cred) 
