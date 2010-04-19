### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.plc.slices import Slices
from sfa.util.config import Config
from sfa.trust.credential import Credential
from sfatables.runtime import SFATablesRules

class create_slice(Method):
    """
    Instantiate the specified slice according to whats defined in the specified rspec      

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name of slice to instantiate (hrn or xrn)
    @param rspec resource specification
    @return 1 is successful, faults otherwise  
    """

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to instantiate (hrn or xrn)"),
        Parameter(str, "Resource specification"),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = Parameter(int, "1 if successful")

    def __run_sfatables(self, manager, rules, hrn, origin_hrn, rspec):
        if rules.sorted_rule_list:
            contexts = rules.contexts
            request_context = manager.fetch_context(hrn, origin_hrn, contexts)
            rules.set_context(request_context)
            newrspec = rules.apply(rspec)
        else:	
            newrspec = rspec
        return newrspec

        
    def call(self, cred, xrn, requested_rspec, origin_hrn=None):
        hrn, type = urn_to_hrn(xrn) 
        user_cred = Credential(string=cred)
        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))
         
        # validate the credential
        self.api.auth.check(cred, 'createslice', hrn)

        manager_base = 'sfa.managers'
        if self.api.interface in ['aggregate']:
            mgr_type = self.api.config.SFA_AGGREGATE_TYPE
            manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            rspec = self.__run_sfatables(manager, 
                                         SFATablesRules('INCOMING'),
                                         hrn, origin_hrn, requested_rspec)
            manager.create_slice(self.api, xrn, rspec)
        elif self.api.interface in ['slicemgr']:
            mgr_type = self.api.config.SFA_SM_TYPE
            manager_module = manager_base + ".slice_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            rspec = self.__run_sfatables(manager, 
                                         SFATablesRules('FORWARD-INCOMING'),
                                         hrn, origin_hrn, requested_rspec)
            manager.create_slice(self.api, xrn, rspec, origin_hrn)

        return 1 
