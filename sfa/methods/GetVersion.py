from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.trust.gid import GID
from sfa.trust.certificate import Certificate

class GetVersion(Method):
    """
    Returns this GENI Aggregate Manager's Version Information
    @return version
    """
    interfaces = ['geni_am']
    accepts = []
    returns = Parameter(dict, "Version information")

    def call(self):
        self.api.logger.info("interface: %s" % (self.name))

        manager_base = 'sfa.managers'

        if self.api.interface in ['geni_am']:
            mgr_type = self.api.config.SFA_GENI_AGGREGATE_TYPE
            manager_module = manager_base + ".geni_am_%s" % mgr_type
            manager = __import__(manager_module, fromlist=[manager_base])
            return manager.GetVersion()
        return {}
    
