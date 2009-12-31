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
from sfa.util.rspec import *

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

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to retrive a ticket for (hrn)"),
        Parameter(str, "Resource specification (rspec)"),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = Parameter(str, "String represeneation of a ticket object")
    
    def call(self, cred, hrn, rspec, origin_hrn=None):
        user_cred = Credential(string=cred)

        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))

        # validate the cred
        self.api.auth.check(cred, "getticket")
	
        # set the right outgoing rules
        manager_base = 'sfa.managers'
        if self.api.interface in ['aggregate']:
            outgoing_rules = SFATablesRules('OUTGOING')
            mgr_type = self.api.config.SFA_AGGREGATE_TYPE
            manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
        elif self.api.interface in ['slicemgr']:
            outgoing_rules = SFATablesRules('FORWARD-OUTGOING')
            mgr_type = self.api.config.SFA_SM_TYPE
            manager_module = manager_base + ".slice_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])

        # Filter the incoming rspec using sfatables
        incoming_rules = SFATablesRules('INCOMING')
        #incoming_rules.set_slice(hrn) # This is a temporary kludge. Eventually, we'd like to fetch the context requested by the match/target
        contexts = incoming_rules.contexts
        caller_hrn = Credential(string=cred).get_gid_caller().get_hrn()
        request_context = manager.fetch_context(hrn, caller_hrn, contexts)
        incoming_rules.set_context(request_context)
        rspec = incoming_rules.apply(rspec)
        # remove nodes that are not available at this interface from the rspec
        valid_rspec = RSpec(xml=manager.get_rspec(self.api, None, origin_hrn))
        valid_nodes = valid_rspec.getDictsByTagName('NodeSpec')
        valid_hostnames = [node['name'] for node in valid_nodes]
        rspec_object = RSpec(xml=rspec)
        rspec_object.filter(tagname='NodeSpec', attribute='name', whitelist=valid_hostnames)
        rspec = rspec_object.toxml() 
        ticket = manager.get_ticket(self.api, hrn, rspec, origin_hrn)
        
        return ticket
        
