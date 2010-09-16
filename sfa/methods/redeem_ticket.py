### $Id: reset_slice.py 15428 2009-10-23 15:28:03Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfacomponent/methods/reset_slice.py $
import xmlrpclib
from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.methods.RedeemTicket import RedeemTicket

class redeem_ticket(RedeemTicket):
    """
    Deprecated. Use RedeemTicket instead.

    Redeem a approved set of resource allocations (ticket).        

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

        return RedeemTicket.call(self, ticket, cred)  
