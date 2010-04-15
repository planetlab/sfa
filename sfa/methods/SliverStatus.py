from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter

class SliverStatus(Method):
    """
    Get the status of a sliver
    
    @param slice_urn (string) URN of slice to allocate to
    @param credentials ([string]) of credentials
    
    """
    interfaces = ['geni_am']
    accepts = [
        Parameter(str, "Slice URN"),
        Parameter(type([str]), "List of credentials"),
        ]
    returns = Parameter(bool, "Success or Failure")

    def call(self, slice_xrn, creds):
        hrn, type = urn_to_hrn(slice_xrn)

        self.api.logger.info("interface: %s\ttarget-hrn: %s\tcaller-creds: %s\tmethod-name: %s"%(self.api.interface, hrn, creds, self.name))

        # Validate that at least one of the credentials is good enough
        found = False
        for cred in creds:
            try:
                self.api.auth.check(cred, 'sliverstatus')
                found = True
                break
            except:
                continue
            
        if not found:
            raise InsufficientRights('SliverStatus: Credentials either did not verify, were no longer valid, or did not have appropriate privileges')
            
        
        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            return manager.SliverStatus(self.api, slice_xrn, creds)

        return ''
    
