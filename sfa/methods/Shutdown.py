from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter


class Shutdown(Method):
    """
    Perform an emergency shut down of a sliver. This operation is intended for administrative use. 
    The sliver is shut down but remains available for further forensics.

    @param slice_urn (string) URN of slice to renew
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

        # Find the valid credentials
        ValidCreds = self.api.auth.checkCredentials(creds, 'shutdown', hrn)

        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            return manager.Shutdown(self.api, slice_xrn, ValidCreds)

        return ''
    
