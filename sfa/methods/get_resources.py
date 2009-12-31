### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.util.config import Config
from sfa.plc.nodes import Nodes
# RSpecManager_pl is not used. This line is a check that ensures that everything is in place for the import to work.
import sfa.rspecs.aggregates.rspec_manager_pl
from sfa.trust.credential import Credential
from sfatables.runtime import SFATablesRules

class get_resources(Method):
    """
    Get an resource specification (rspec). The rspec may describe the resources
    available at an authority or the resources being used by a slice.      

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name of the slice we are interesed in or None 
           for an authority.  
    """

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        Mixed(Parameter(str, "Human readable name (hrn)"),
              Parameter(None, "hrn not specified")),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = Parameter(str, "String representatin of an rspec")
    
    def call(self, cred, hrn=None, origin_hrn=None):
        user_cred = Credential(string=cred)

        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))

        # validate the cred    
        self.api.auth.check(cred, 'listnodes')

        # send the call to the right manager
        manager_base = 'sfa.managers'
        if self.api.interface in ['aggregate']:
            mgr_type = self.api.config.SFA_AGGREGATE_TYPE
            manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            rspec = manager.get_rspec(self.api, hrn, origin_hrn)
            outgoing_rules = SFATablesRules('OUTGOING')
        elif self.api.interface in ['slicemgr']:
            mgr_type = self.api.config.SFA_SM_TYPE
            manager_module = manager_base + ".slice_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            rspec = manager.get_rspec(self.api, hrn, origin_hrn)
            outgoing_rules = SFATablesRules('FORWARD-OUTGOING')

        filtered_rspec = rspec
        if outgoing_rules.sorted_rule_list:
           request_context = manager.fetch_context(hrn, origin_hrn, outgoing_rules.contexts)
           outgoing_rules.set_context(request_context)
           filtered_rspec = outgoing_rules.apply(rspec)

        return filtered_rspec
