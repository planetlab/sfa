### $Id$
### $URL$
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
from sfatables.runtime import SFATablesRules

class get_ticket(Method):
    """
    Retrieve a ticket. This operation is currently implemented on PLC
    only (see SFA, engineering decisions); it is not implemented on
    components.
    
    The ticket is filled in with information from the PLC database. This
    information includes resources, and attributes such as user keys and
    initscripts.
    
    @param cred credential string
    @param name name of the slice to retrieve a ticket for
    @param rspec resource specification dictionary
    
    @return the string representation of a ticket object
    """

    interfaces = ['registry', 'aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to retrive a ticket for (hrn)"),
        Parameter(str, "Resource specification (rspec)"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = Parameter(str, "String represeneation of a ticket object")
    
    def call(self, cred, hrn, rspec, request_hash=None):
        self.api.auth.authenticateCred(cred, [cred, hrn, rspec], request_hash)
        self.api.auth.check(cred, "getticket")
        self.api.auth.verify_object_belongs_to_me(hrn)
        self.api.auth.verify_object_permission(hrn)

        # find record info
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

        # determine aggregate tyep 
        sfa_aggregate_type = Config().get_aggregate_rspec_type()
        rspec_manager = __import__("sfa.rspecs.aggregates.rspec_manager_"+sfa_aggregate_type, fromlist = ["sfa.rspecs.aggregates"])

        # Fukter the incoming rspec using sfatables
        incoming_rules = SFATablesRules('INCOMING')
        #incoming_rules.set_slice(hrn) # This is a temporary kludge. Eventually, we'd like to fetch the context requested by the match/target
        contexts = incoming_rules.contexts
        caller_hrn = Credential(string=cred).get_gid_caller().get_hrn()
        request_context = rspec_manager.fetch_context(hrn, caller_hrn, contexts)
        incoming_rules.set_context(request_context)
        rspec = incoming_rules.apply(rspec)

        # get sliver info    
        slivers = Slices(self.api).get_slivers(hrn)
        if not slivers:
            raise SliverDoesNotExist(hrn)
            
        # get initscripts
        initscripts = None
        data = {
            'timestamp': int(time.time()),
            'initscripts': initscripts,
            'slivers': slivers 
        }

        new_ticket.set_attributes(data)
        new_ticket.set_rspec(rspec)

        new_ticket.set_parent(self.api.auth.hierarchy.get_auth_ticket(auth_hrn))

        new_ticket.encode()
        new_ticket.sign()

        return new_ticket.save_to_string(save_parents=True)
        
