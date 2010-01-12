### $Id$
### $URL$
import traceback
from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.debug import log
from sfa.trust.credential import Credential
from sfa.util.record import SfaRecord

class resolve(Method):
    """
    Resolve a record.

    @param cred credential string authorizing the caller
    @param hrn human readable name to resolve (hrn or urn) 
    @return a list of record dictionaries or empty list     
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Mixed(Parameter(str, "Human readable name (hrn or urn)"),
              Parameter(list, "List of Human readable names ([hrn])"))  
        ]

    returns = [SfaRecord]
    
    def call(self, cred, xrn, origin_hrn=None):
        user_cred = Credential(string=cred)
        hrn = urn_to_hrn(xrn)[0]

        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))
 
        # validate the cred
        self.api.auth.check(cred, 'resolve')
        # send the call to the right manager
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_REGISTRY_TYPE
        manager_module = manager_base + ".registry_manager_%s" % mgr_type
        manager = __import__(manager_module, fromlist=[manager_base])
        return manager.resolve(self.api, xrn, origin_hrn=origin_hrn)


            
