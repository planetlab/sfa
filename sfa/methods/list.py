### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.auth import Auth
from sfa.util.record import GeniRecord

from sfa.server.registry import Registries

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
        records = []
        try:
            if not self.api.auth.hierarchy.auth_exists(hrn):
                raise MissingAuthority(hrn)
            table = self.api.auth.get_auth_table(hrn)   
            records = table.list()
        except MissingAuthority:
            # is this a foreign authority
            registries = Registries(self.api)
            credential = self.api.getCredential()
            for registry in registries:
                if hrn.startswith(registry) and registry not in [self.api.hrn]:
                    record_list = registries[registry].list(credential, hrn)
                    for record in record_list:
                        records.append(record.as_dict()) 
                    return records
        
        return records
