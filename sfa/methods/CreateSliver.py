from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.trust.gid import GID
from sfa.trust.certificate import Certificate

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

    def call(self, slice_xrn, creds, rspec):
        hrn, type = urn_to_hrn(slice_xrn)

        self.api.logger.info("interface: %s\ttarget-hrn: %s\tcaller-creds: %s\tmethod-name: %s"%(self.api.interface, hrn, creds, self.name))

        # Validate that at least one of the credentials is good enough
        found = False
        for cred in creds:
            try:
                self.api.auth.check(cred, 'createslice')
                found = True
                break
            except:
                continue
            
        if not found:
            raise InsufficientRights('CreateSliver: Credentials either did not verify, were no longer valid, or did not have appropriate privileges')
            
        
        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            return manager.CreateSlice(self.api, slice_xrn, creds, rspec)

        return ''
    
