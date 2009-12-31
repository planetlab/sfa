### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.util.record import GeniRecord
from sfa.util.genitable import GeniTable
from sfa.server.registry import Registries
from sfa.util.prefixTree import prefixTree
from sfa.trust.credential import Credential

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
        Parameter(str, "Human readable name (hrn)"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = [GeniRecord]
    
    def call(self, cred, hrn, request_hash=None):
        #log the call
        origin_hrn=Credential(string=cred).get_gid_origin_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))
        
        self.api.auth.authenticateCred(cred, [cred, hrn], request_hash)
        self.api.auth.check(cred, 'list')
            
        # load all know registry names into a prefix tree and attempt to find
        # the longest matching prefix  
        records = []
        registries = Registries(self.api)
        hrns = registries.keys()
        tree = prefixTree()
        tree.load(hrns)
        registry_hrn = tree.best_match(hrn)

        #if there was no match then this record belongs to an unknow registry
        if not registry_hrn:
            raise MissingAuthority(hrn)
        
        # if the best match (longest matching hrn) is not the local registry,
        # forward the request
        if registry_hrn != self.api.hrn:
            credential = self.api.getCredential()
            try:
                request_hash=None
                record_list = registries[registry_hrn].list(credential, hrn, request_hash)
                records = [GeniRecord(dict=record).as_dict() for record in record_list]
            except:
                arg_list = [credential, hrn]
                request_hash = self.api.key.compute_hash(arg_list)
                record_list = registries[registry_hrn].list(credential, hrn, request_hash)
                records = [GeniRecord(dict=record).as_dict() for record in record_list] 
                
        if records:
            return records

        # if we still havnt found the record yet, try the local registry
        if not self.api.auth.hierarchy.auth_exists(hrn):
            raise MissingAuthority(hrn)
        
        table = GeniTable()
        records = table.find({'authority': hrn})
        
        return records
