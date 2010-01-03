### $Id: reset_slice.py 15428 2009-10-23 15:28:03Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfacomponent/methods/reset_slice.py $
import xmlrpclib
from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed

class redeem_ticket(Method):
    """
    Reset the specified slice      

    @param cred credential string specifying the rights of the caller
    @param ticket 
    @return 1 is successful, faults otherwise  
    """

    interfaces = ['component']
    
    accepts = [
        Parameter(str, "Credential string representation of SFA credential"),
        Parameter(str, "Ticket  string representation of SFA ticket")
        ]

    returns = [Parameter(int, "1 if successful")]
    
    def call(self, cred, ticket):
        self.api.auth.check(cred, 'redeemticket')
        self.api.auth.check_ticket(ticket)

        # send the call to the right manager
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_CM_TYPE
        manager_module = manager_base + ".component_manager_%s" % mgr_type
        manager = __import__(manager_module, fromlist=[manager_base])
        manager.redeem_ticket(self.api, ticket) 
        return 1 
