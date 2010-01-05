### $Id$
### $URL$

import time
from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.debug import log
from sfa.trust.credential import Credential

class update(Method):
    """
    Update an object in the registry. Currently, this only updates the
    PLC information associated with the record. The SFA fields (name, type,
    GID) are fixed.
    
    @param cred credential string specifying rights of the caller
    @param record a record dictionary to be updated

    @return 1 if successful, faults otherwise 
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(dict, "Record dictionary to be updated"),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, record_dict, origin_hrn=None):
        user_cred = Credential(string=cred)
    
	    #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, None, self.name))
        
        # validate the cred
        self.api.auth.check(cred, "update")
        
        # send the call to the right manager
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_REGISTRY_TYPE
        manager_module = manager_base + ".registry_manager_%s" % mgr_type
        manager = __import__(manager_module, fromlist=[manager_base])
        return manager.update(self.api, record_dict)

