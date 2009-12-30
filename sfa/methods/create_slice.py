### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.plc.slices import Slices
from sfa.util.config import Config
# RSpecManager_pl is not used. It's used to make sure the module is in place.
import sfa.rspecs.aggregates.rspec_manager_pl
from sfa.trust.credential import Credential
from sfatables.runtime import SFATablesRules


class create_slice(Method):
    """
    Instantiate the specified slice according to whats defined in the specified rspec      

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name of slice to instantiate
    @param rspec resource specification
    @return 1 is successful, faults otherwise  
    """

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name of slice to instantiate"),
        Parameter(str, "Resource specification"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, hrn, requested_rspec, request_hash=None):
        
        # This cred will be an slice cred, not a user, so we cant use it to
        # authenticate the caller's request_hash. Let just get the caller's gid
        # from the cred and authenticate using that
        user_cred = Credential(string=cred)
        client_gid = user_cred.get_gid_caller()
        client_gid_str = client_gid.save_to_string(save_parents=True)
        self.api.auth.authenticateGid(client_gid_str, [cred, hrn, requested_rspec], request_hash)
        self.api.auth.check(cred, 'createslice')

        #log the call
        gid_origin_caller = user_cred.get_gid_origin_caller()
        origin_hrn = gid_origin_caller.get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))

        sfa_aggregate_type = Config().get_aggregate_rspec_type()
        rspec_manager = __import__("sfa.rspecs.aggregates.rspec_manager_"+sfa_aggregate_type, fromlist = ["sfa.rspecs.aggregates"])
        #Filter the incoming rspec using sfatables
        if self.api.interface in ['slicemgr']:
            incoming_rules = SFATablesRules('FORWARD-INCOMING')
        elif self.api.interface in ['aggregate']:
            incoming_rules = SFATablesRules('INCOMING')

        if incoming_rules.sorted_rule_list:
            #incoming_rules.set_slice(hrn) # This is a temporary kludge. Eventually, we'd like to fetch the context requested by the match/target

            contexts = incoming_rules.contexts
            request_context = rspec_manager.fetch_context(hrn, origin_hrn, contexts)
            incoming_rules.set_context(request_context)
            rspec = incoming_rules.apply(requested_rspec)
        else:	
            rspec = requested_rspec

        # send the call to the right manager
        if sfa_aggregate_type not in ['pl']:
            # To clean up after July 21 - SB
            rspec = rspec_manager.create_slice(self.api, hrn, rspec)
            return 1

        manager_base = 'sfa.managers'
        if self.api.interface in ['aggregate']:
            mgr_type = self.api.config.SFA_AGGREGATE_TYPE
            manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            manager.create_slice(self.api, hrn, rspec)
        elif self.api.interface in ['slicemgr']:
            mgr_type = self.api.config.SFA_SM_TYPE
            manager_module = manager_base + ".slice_manager_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            manager.create_slice(self.api, hrn, rspec, gid_origin_caller)

        return 1 
