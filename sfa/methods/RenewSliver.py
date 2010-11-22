from sfa.util.faults import *
from sfa.util.xrn import urn_to_hrn
from sfa.util.method import Method
from sfa.util.parameter import Parameter
from sfa.trust.credential import Credential
from sfa.util.sfatime import utcparse
import datetime

class RenewSliver(Method):
    """
    Renews the resources in a sliver, extending the lifetime of the slice.    
    @param slice_urn (string) URN of slice to renew
    @param credentials ([string]) of credentials
    @param expiration_time (string) requested time of expiration
    
    """
    interfaces = ['aggregate', 'slicemgr']
    accepts = [
        Parameter(str, "Slice URN"),
        Parameter(type([str]), "List of credentials"),
        Parameter(str, "Expiration time in RFC 3339 format")
        ]
    returns = Parameter(bool, "Success or Failure")

    def call(self, slice_xrn, creds, expiration_time):
        hrn, type = urn_to_hrn(slice_xrn)

        self.api.logger.info("interface: %s\ttarget-hrn: %s\tcaller-creds: %s\tmethod-name: %s"%(self.api.interface, hrn, creds, self.name))

        # Find the valid credentials
        valid_creds = self.api.auth.checkCredentials(creds, 'renewsliver', hrn)

        # Validate that the time does not go beyond the credential's expiration time
        requested_time = utcparse(expiration_time)
        if requested_time > Credential(string=valid_creds[0]).get_expiration():
            raise InsufficientRights('SliverStatus: Credential expires before requested expiration time')
        if requested_time > datetime.datetime.utcnow() + datetime.timedelta(days=60):
            raise Exception('Cannot renew > 60 days from now')
        manager = self.api.get_interface_manager()
        manager.renew_slice(self.api, slice_xrn, valid_creds, expiration_time)    
 
        return 1
    
