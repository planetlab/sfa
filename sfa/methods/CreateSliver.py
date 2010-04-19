from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter
from sfatables.runtime import SFATablesRules
import sys
from sfa.trust.credential import Credential

class CreateSliver(Method):
    """
    Allocate resources to a slice.  This operation is expected to
    start the allocated resources asynchornously after the operation
    has successfully completed.  Callers can check on the status of
    the resources using SliverStatus.

    @param slice_urn (string) URN of slice to allocate to
    @param credentials ([string]) of credentials
    @param rspec (string) rspec to allocate
    
    """
    interfaces = ['geni_am']
    accepts = [
        Parameter(str, "Slice URN"),
        Parameter(type([str]), "List of credentials"),
        Parameter(str, "RSpec")
        ]
    returns = Parameter(str, "Allocated RSpec")

    def __run_sfatables(self, manager, rules, hrn, origin_hrn, rspec):
        if rules.sorted_rule_list:
            contexts = rules.contexts
            request_context = manager.fetch_context(hrn, origin_hrn, contexts)
            rules.set_context(request_context)
            newrspec = rules.apply(rspec)
        else:    
            newrspec = rspec
        return newrspec


    def call(self, slice_xrn, creds, rspec):
        hrn, type = urn_to_hrn(slice_xrn)

        self.api.logger.info("interface: %s\ttarget-hrn: %s\tcaller-creds: %s\tmethod-name: %s"%(self.api.interface, hrn, creds, self.name))

        # Validate that at least one of the credentials is good enough
        found = False
        for cred in creds:
            try:
                self.api.auth.check(cred, 'createslice')
                origin_hrn = Credential(string=cred).get_gid_caller().get_hrn()
                found = True
                break
            except:
                error = sys.exc_info()[:2]
                continue
            
        if not found:
            raise InsufficientRights('CreateSliver: Access denied: %s -- %s' % (error[0],error[1]))
             
        
        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            rspec = self.__run_sfatables(manager, SFATablesRules('INCOMING'),
                                         hrn, origin_hrn, rspec)
            return manager.CreateSliver(self.api, slice_xrn, creds, rspec)

        return ''
    
