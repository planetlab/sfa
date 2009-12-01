### $Id: reset_slice.py 15428 2009-10-23 15:28:03Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfacomponent/methods/reset_slice.py $
import xmlrpclib
from sfa.util.faults import *
from sfa.util.misc import *
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
        Parameter(str, "Ticket  string representation of SFA ticket"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = [Parameter(int, "1 if successful")]
    
    def call(self, cred, ticket, request_hash=None):
        # This cred will be an slice cred, not a user, so we cant use it to
        # authenticate the caller's request_hash. Let just get the caller's gid
        # from the cred and authenticate using that
        client_gid = Credential(string=cred).get_gid_caller()
        client_gid_str = client_gid.save_to_string(save_parents=True)
        self.api.auth.authenticateGid(client_gid_str, [cred, hrn], request_hash)
        self.api.auth.check(cred, 'redeemticket')
        
        ticket = SfaTicket(string=ticket)
        # XX we should verify the ticket, but we need the privste keys to do that
        # maybe we should just pass the ticket to the authoriative registry to it 
        # verify the ticket for us
        #ticket.verify(pkey)
        # or 
        #self.api.registry.verify_ticket(ticket.save_to_string(save_parents=True))

        ticket.decode()
        hrn = ticket.attributes['slivers'][0]['hrn']
        slicename = hrn_to_pl_slicename(hrn)
        if not self.api.sliver_exists(slicename):
            raise SliverDoesNotExist(slicename)

        # convert ticket to format nm is used to
        nm_ticket = xmlrpclib.dumps((ticket.attributes,), methodresponse=True)
        self.api.nodemanager.AdminTicket(nm_ticket)
        
        return 1 
