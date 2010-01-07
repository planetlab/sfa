### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.debug import log
from sfa.trust.credential import Credential

class remove(Method):
    """
    Remove an object from the registry. If the object represents a PLC object,
    then the PLC records will also be removed.
    
    @param cred credential string
    @param type record type
    @param xrn human readable name of record to remove (hrn or urn)

    @return 1 if successful, faults otherwise 
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Record type"),
        Parameter(str, "Human readable name of slice to instantiate (hrn or urn)"),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, type, xrn, origin_hrn=None):
        user_cred = Credential(string=cred)
       
        # convert xrn to hrn     
        if type: 
            hrn = urn_to_hrn(xrn)[0]
        else: 
            hrn, type = urn_to_hrn(xrn)
            
        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))

        # validate the cred
        self.api.auth.check(cred, "remove")
        self.api.auth.verify_object_permission(hrn)
       
        # send the call to the right manager
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_REGISTRY_TYPE
        manager_module = manager_base + ".registry_manager_%s" % mgr_type
        manager = __import__(manager_module, fromlist=[manager_base])
        return manager.remove(self.api, xrn, type, origin_hrn) 
