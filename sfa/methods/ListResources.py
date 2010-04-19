from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.credential import Credential
from sfatables.runtime import SFATablesRules
import sys


class ListResources(Method):
    """
    Returns information about available resources or resources allocated to this    slice
    @param credential list
    @param options dictionary
    @return string
    """
    interfaces = ['geni_am']
    accepts = [
        Parameter(type([str]), "List of credentials"),
        Parameter(dict, "Options")
        ]
    returns = Parameter(str, "List of resources")

    def call(self, creds, options):
        self.api.logger.info("interface: %s\tmethod-name: %s" % (self.api.interface, self.name))
            
        # Validate that at least one of the credentials is good enough
        found = False
        for cred in creds:
            try:
                self.api.auth.check(cred, 'listnodes')
                found = True
                user_cred = Credential(string=cred)
                break
            except:
                error = sys.exc_info()[:2]
                continue
            
        if not found:
            raise InsufficientRights('ListResources: Access denied: %s -- %s' % (error[0],error[1]))
        
        origin_hrn = user_cred.get_gid_caller().get_hrn()
                    
        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            rspec = manager.ListResources(self.api, creds, options)
            outgoing_rules = SFATablesRules('OUTGOING')
            
        
        filtered_rspec = rspec
        if outgoing_rules.sorted_rule_list:
            context = {'sfa':{'user':{'hrn':origin_hrn}, 'slice':{'hrn':None}}}
            outgoing_rules.set_context(context)
            filtered_rspec = outgoing_rules.apply(rspec)      

        return filtered_rspec  
    
    
