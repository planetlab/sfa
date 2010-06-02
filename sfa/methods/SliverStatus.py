from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter

class SliverStatus(Method):
    """
    Get the status of a sliver
    
    @param slice_urn (string) URN of slice to allocate to
    
    """
    interfaces = ['geni_am']
    accepts = [
        Parameter(str, "Slice URN"),
        ]
    returns = Parameter(bool, "Success or Failure")

    def call(self, slice_xrn, creds):
        hrn, type = urn_to_hrn(slice_xrn)
        
        ValidCreds = self.api.auth.checkCredentials(creds, 'sliverstatus', hrn)

        self.api.logger.info("interface: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, hrn, self.name))

        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            return manager.SliverStatus(self.api, slice_xrn, ValidCreds)

        return ''
    
