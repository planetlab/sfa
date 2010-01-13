### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.record import SfaRecord
from sfa.trust.credential import Credential

class list(Method):
    """
    List the records in an authority. 

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name of authority to list (hrn or urn)
    @return list of record dictionaries         
    """
    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name (hrn or urn)"),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = [SfaRecord]
    
    def call(self, cred, xrn, origin_hrn=None):
        hrn, type = urn_to_hrn(xrn)
        user_cred = Credential(string=cred)
        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))
       
        # validate the cred 
        self.api.auth.check(cred, 'list')
        
        # send the call to the right manager    
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_REGISTRY_TYPE
        manager_module = manager_base + ".registry_manager_%s" % mgr_type
        manager = __import__(manager_module, fromlist=[manager_base])
        return manager.list(self.api, xrn, origin_hrn) 
