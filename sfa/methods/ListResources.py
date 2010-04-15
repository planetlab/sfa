from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed

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
                self.api.auth.check(cred, 'ListResources')
                found = True
                break
            except:
                continue
            
        if not found:
            raise InsufficientRights('ListResources: Credentials either did not verify, were no longer valid, or did not have appropriate privileges')
        
        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            return manager.ListResources(self.api, creds, options)

        return ''
    
