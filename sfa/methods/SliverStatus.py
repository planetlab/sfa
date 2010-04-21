from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter
from sfa.server.aggregate import Aggregates

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
        
        # Make sure that this is a geni_aggregate talking to us
        geni_aggs = Aggregates(self.api, '/etc/sfa/geni_aggregates.xml')
        if not hrn in [agg['hrn'] for agg in geni_aggs]:
            raise SfaPermissionDenied("Only GENI Aggregates may make this call")

        self.api.logger.info("interface: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, hrn, self.name))

        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            return manager.SliverStatus(self.api, slice_xrn)

        return ''
    
