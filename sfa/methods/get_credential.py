### $Id$
### $URL$

from sfa.trust.credential import *
from sfa.trust.rights import *
from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.debug import log
from sfa.trust.credential import Credential

class get_credential(Method):
    """
    Retrive a credential for an object
    If cred == Nonee then the behavior reverts to get_self_credential

    @param cred credential object specifying rights of the caller
    @param type type of object (user | slice | sa | ma | node)
    @param hrn human readable name of object (hrn or urn)

    @return the string representation of a credential object  
    """

    interfaces = ['registry']
    
    accepts = [
        Mixed(Parameter(str, "credential"),
              Parameter(None, "No credential")),  
        Parameter(str, "Human readable name (hrn or urn)")
        ]

    returns = Parameter(str, "String representation of a credential object")

    def call(self, cred, type, xrn, origin_hrn=None):
        if type:
            hrn = urn_to_hrn(xrn)[0]
        else:
            hrn, type = urn_to_hrn(xrn)

        #log the call
        if not origin_hrn:
            origin_hrn = Credential(string=cred).get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))	
        self.api.auth.check(cred, 'getcredential')
        self.api.auth.verify_object_belongs_to_me(hrn)

        # send the call to the right manager
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_REGISTRY_TYPE
        manager_module = manager_base + ".registry_manager_%s" % mgr_type
        manager = __import__(manager_module, fromlist=[manager_base])
        return manager.get_credential(self.api, xrn, type)
