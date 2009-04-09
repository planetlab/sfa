from geni.util.faults import *
from geni.util.excep import *
from geni.util.method import Method
from geni.util.parameter import Parameter, Mixed
from geni.util.auth import Auth
from geni.util.record import GeniRecord

class list(Method):
    """
    List the records in an authority. 

    @param cred credential string specifying the rights of the caller
    @param hrn human readable name of authority to list
    @return list of record dictionaries         
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Human readable name (hrn)")
        ]

    returns = [GeniRecord]
    
    def call(self, cred, hrn):
        
        self.api.auth.check(cred, 'list')
        # is this a foreign authority
        if not hrn.startswith(self.api.hrn):
            for registry in self.api.registries:
                if hrn.startswith(registry):
                    records = self.api.registries[registry].list(self.api.credential, hrn)
                    return records    

        if not self.api.auth.hierarchy.auth_exists(hrn):
            raise MissingAuthority(hrn)
        table = self.api.auth.get_auth_table(hrn)   
        records = table.list()
        
        return records
