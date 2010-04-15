from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter
from sfa.trust.credential import Credential
from dateutil.parser import parse

class RenewSliver(Method):
    """
    Renews the resources in a sliver, extending the lifetime of the slice.    
    @param slice_urn (string) URN of slice to renew
    @param credentials ([string]) of credentials
    @param expiration_time (string) requested time of expiration
    
    """
    interfaces = ['geni_am']
    accepts = [
        Parameter(str, "Slice URN"),
        Parameter(type([str]), "List of credentials"),
        Parameter(str, "Expiration time in RFC 3339 format")
        ]
    returns = Parameter(bool, "Success or Failure")

    def call(self, slice_xrn, creds, expiration_time):
        hrn, type = urn_to_hrn(slice_xrn)

        self.api.logger.info("interface: %s\ttarget-hrn: %s\tcaller-creds: %s\tmethod-name: %s"%(self.api.interface, hrn, creds, self.name))

        # Validate that at least one of the credentials is good enough
        found = False
        validCred = None
        for cred in creds:
            try:
                self.api.auth.check(cred, 'renewsliver')
                validCred = cred
                found = True
                break
            except:
                continue
            
        if not found:
            raise InsufficientRights('SliverStatus: Credentials either did not verify, were no longer valid, or did not have appropriate privileges')
            
        # Validate that the time does not go beyond the credential's expiration time
        requested_time = parse(expiration_time)
        if requested_time > Credential(string=validCred).get_lifetime():
            raise InsufficientRights('SliverStatus: Credential expires before requested expiration time')
        
        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            return manager.RenewSliver(self.api, slice_xrn, creds, expiration_time)

        return ''
    
