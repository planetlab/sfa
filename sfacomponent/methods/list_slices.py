### $Id: start_slice.py 15428 2009-10-23 15:28:03Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/methods/start_slice.py $

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed

class list_slices(Method):
    """
    List the slices on a component      

    @param cred credential string specifying the rights of the caller
    @return list of slice names  
    """

    interfaces = ['component']
    
    accepts = [
        Parameter(str, "Credential string"),
        ]

    returns = [Parameter(str, "slice name")]
    
    def call(self, cred, hrn, request_hash=None):
        # This cred will be an slice cred, not a user, so we cant use it to
        # authenticate the caller's request_hash. Let just get the caller's gid
        # from the cred and authenticate using that
        client_gid = Credential(string=cred).get_gid_caller()
        client_gid_str = client_gid.save_to_string(save_parents=True)
        self.api.auth.authenticateGid(client_gid_str, [cred, hrn], request_hash)
        self.api.auth.check(cred, 'listslices')
        slice_names = self.nodemanager.GetXIDs().keys()
        
        return slice_names 
