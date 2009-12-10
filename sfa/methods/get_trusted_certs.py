
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/methods/reset_slices.py $

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.trust.credential import Credential

class get_trusted_certs(Method):
    """
    @param cred credential string specifying the rights of the caller
    @param request_hash hash of the request
    @return 1 is successful, faults otherwise  
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, request_hash=None):
        # authenticate the cred
        client_gid = Credential(string=cred).get_gid_caller()
        client_gid_str = client_gid.save_to_string(save_parents=True)
        self.api.auth.authenticateGid(client_gid_str, [cred], request_hash) 
        self.api.auth.check(cred, 'gettrustedcerts')

        trusted_cert_strings = [gid.save_to_string(save_parents=True) for \
                                gid in self.api.auth.trusted_cert_list] 
        
        return trusted_cert_strings 
