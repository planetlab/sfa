### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.util.record import GeniRecord
from sfa.util.genitable import GeniTable
from sfa.util.debug import log
from sfa.trust.credential import Credential
from sfa.server.registry import Registries

class remove(Method):
    """
    Remove an object from the registry. If the object represents a PLC object,
    then the PLC records will also be removed.
    
    @param cred credential string
    @param type record type
    @param hrn human readable name of record to remove

    @return 1 if successful, faults otherwise 
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Credential string"),
        Parameter(str, "Record type"),
        Parameter(str, "Human readable name of slice to instantiate"),
        Mixed(Parameter(str, "Human readable name of the original caller"),
              Parameter(None, "Origin hrn not specified"))
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, type, hrn, origin_hrn=None):
        user_cred = Credential(string=cred)

        #log the call
        if not origin_hrn:
            origin_hrn = user_cred.get_gid_caller().get_hrn()
        self.api.logger.info("interface: %s\tcaller-hrn: %s\ttarget-hrn: %s\tmethod-name: %s"%(self.api.interface, origin_hrn, hrn, self.name))

        # validate the cred
        self.api.auth.check(cred, "remove")
        self.api.auth.verify_object_permission(hrn)
        
        table = GeniTable()
        filter = {'hrn': hrn}
        if type not in ['all', '*']:
            filter['type'] = type
        records = table.find(filter)
        if not records:
            raise RecordNotFound(hrn)
        record = records[0]
        type = record['type']

        credential = self.api.getCredential()
       	registries = Registries(self.api) 

        # Try to remove the object from the PLCDB of federated agg.
        # This is attempted before removing the object from the local agg's PLCDB and sfa table
        if hrn.startswith(self.api.hrn) and type in ['user', 'slice', 'authority']:
            for registry in registries:
                if registry not in [self.api.hrn]:
                    result=registries[registry].remove_peer_object(credential, record, origin_hrn)
                    pass
        if type == "user":
            persons = self.api.plshell.GetPersons(self.api.plauth, record['pointer'])
            # only delete this person if he has site ids. if he doesnt, it probably means 
            # he was just removed from a site, not actually deleted
            if persons and persons[0]['site_ids']:
                self.api.plshell.DeletePerson(self.api.plauth, record['pointer'])
        elif type == "slice":
            if self.api.plshell.GetSlices(self.api.plauth, record['pointer']):
                self.api.plshell.DeleteSlice(self.api.plauth, record['pointer'])
        elif type == "node":
            if self.api.plshell.GetNodes(self.api.plauth, record['pointer']):
                self.api.plshell.DeleteNode(self.api.plauth, record['pointer'])
        elif type == "authority":
            if self.api.plshell.GetSites(self.api.plauth, record['pointer']):
                self.api.plshell.DeleteSite(self.api.plauth, record['pointer'])
        else:
            raise UnknownGeniType(type)

        table.remove(record)
           
        return 1
