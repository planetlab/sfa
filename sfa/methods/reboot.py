### $Id: reboot.py 15428 2009-10-23 15:28:03Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfacomponent/methods/reboot.py $
import os
from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed

class reboot(Method):
    """
    Reboot the component       

    @param cred credential string specifying the rights of the caller
    @return None  
    """

    interfaces = ['component']
    
    accepts = [
        Parameter(str, "Credential string"),
        ]

    returns = None
    
    def call(self, cred, request_hash=None):
        client_gid = Credential(string=cred).get_gid_caller()
        client_gid_str = client_gid.save_to_string(save_parents=True)
        self.api.auth.authenticateGid(client_gid_str, [cred], request_hash)
        self.api.auth.check(cred, 'reboot')
        # send the call to the right manager
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_CM_TYPE
        manager_module = manger_base + ".component_manager_%s" % mgr_type
        manager = __import__(manager_module, manager_base)
        manager.reboot()
