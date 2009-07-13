### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.util.config import Config
from sfa.plc.nodes import Nodes
# RSpecManager_pl is not used. This is just to resolve issues with the dynamic __import__ that comes later.
import sfa.rspecs.aggregates.rspec_manager_pl

class get_resources(Method):
    """
    Get an resource specification (rspec). The rspec may describe the resources
    available at an authority or the resources being used by a slice.      

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name of the slice we are interesed in or None 
           for an authority.  
    """

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        Mixed(Parameter(str, "Human readable name (hrn)"),
              Parameter(None, "hrn not specified"))
        ]

    returns = Parameter(str, "String representatin of an rspec")
    
    def call(self, cred, hrn=None):
        sfa_aggregate_type = Config().get_aggregate_rspec_type()
        if (sfa_aggregate_type == 'pl'):
            self.api.auth.check(cred, 'listnodes')
            nodes = Nodes(self.api)
            if hrn:
                rspec = nodes.get_rspec(hrn)
            else:
                nodes.refresh()
                rspec = nodes['rspec']
        else:
            # To clean up after July 21 - SB    
            rspec_manager = __import__("sfa.rspecs.aggregates.rspec_manager_"+sfa_aggregate_type)
            rspec = rspec_manager.get_rspec(hrn)
        
        return rspec
