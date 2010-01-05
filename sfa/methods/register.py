### $Id$
### $URL$

from sfa.trust.certificate import Keypair, convert_public_key
from sfa.trust.gid import *
from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.record import SfaRecord
from sfa.util.debug import log
from sfa.trust.auth import Auth
from sfa.trust.gid import create_uuid
from sfa.trust.credential import Credential

class register(Method):
    """
    Register an object with the registry. In addition to being stored in the
    SFA database, the appropriate records will also be created in the
    PLC databases
    
    @param cred credential string
    @param record_dict dictionary containing record fields
    
    @return gid string representation
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(dict, "Record dictionary containing record fields")
        ]

    returns = Parameter(int, "String representation of gid object")
    
    def call(self, cred, record, origin_hrn=None):
        user_cred = Credential(string=cred)

        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        hrn = None
        if 'hrn' in record:
            hrn = record['hrn']
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))
        
        # validate the cred
        self.api.auth.check(cred, "register")

        #send the call to the right manager
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_REGISTRY_TYPE
        manager_module = manager_base + ".registry_manager_%s" % mgr_type
        manager = __import__(manager_module, fromlist=[manager_base])
        return manager.register(self.api, record)
