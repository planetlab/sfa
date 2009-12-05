### $Id: get_ticket.py 15823 2009-11-20 19:45:52Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/methods/get_ticket.py $
import time
from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.util.config import Config
from sfa.trust.credential import Credential
from sfa.util.genitable import GeniTable
from sfa.util.sfaticket import SfaTicket
from sfa.plc.slices import Slices

class get_signed_ticket(Method):
    """
    Retrieve a ticket. This operation is currently implemented on PLC
    only (see SFA, engineering decisions); it is not implemented on
    components.
    
    The ticket is filled in with information from the PLC database. This
    information includes resources, and attributes such as user keys and
    initscripts.
    
    @param cred credential string
    @param ticket string representation of a ticket object
    
    @return the string representation of a signed ticket object
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "String representation of a ticket object"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = Parameter(str, "String represeneation of a signed ticket object")
    
    def call(self, cred, hrn, rspec, data, request_hash=None):
        self.api.auth.authenticateCred(cred, [cred, hrn, rspec], request_hash)
        self.api.auth.check(cred, "signticket")
        self.api.auth.verify_object_belongs_to_me(hrn)
        self.api.auth.verify_object_permission(hrn)
  
        # get the record info
        table = GeniTable()
        records = table.findObjects({'hrn': hrn, 'type': 'slice', 'peer_authority': None})
        if not records:
            raise RecordNotFound(hrn)
        record = records[0]
        auth_hrn = record['authority']
        auth_info = self.api.auth.get_auth_info(auth_hrn)
        object_gid = record.get_gid_object()
        new_ticket = SfaTicket(subject = object_gid.get_subject())
        new_ticket.set_gid_caller(self.api.auth.client_gid)
        new_ticket.set_gid_object(object_gid)
        new_ticket.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        new_ticket.set_pubkey(object_gid.get_pubkey())
        newticket.set_attributes(data)
        new_ticket.set_rspec(rspec)
        new_ticket.set_parent(self.api.auth.hierarchy.get_auth_ticket(auth_hrn))
        new_ticket.encode()
        new_ticket.sign()
 
        return new_ticket.save_to_string(save_parents=True)
        
