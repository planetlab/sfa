import time
from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.credential import Credential

class Update(Method):
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
        Parameter(dict, "Record dictionary to be updated"),
        Parameter(str, "Credential string"),
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, record_dict, creds):
        # validate the cred
        valid_creds = self.api.auth.checkCredentials(creds, "update")
        
        # verify permissions
        hrn = record_dict.get('hrn', '')  
        self.api.auth.verify_object_permission(hrn)
    
        # log
        origin_hrn = Credential(string=valid_creds[0]).get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))
       
        manager = self.api.get_interface_manager()
 
        return manager.update(self.api, record_dict)

