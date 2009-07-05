### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.util.nodes import Nodes

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
        
        self.api.auth.check(cred, 'listnodes')
        nodes = Nodes(self.api)
        if hrn:
            rspec = nodes.get_rspec(hrn)
        else:
            nodes.refresh()
            rspec = nodes['rspec']
        
        return rspec
