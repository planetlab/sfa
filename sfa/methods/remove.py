### $Id$
### $URL$

from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.util.record import GeniRecord
from sfa.util.genitable import GeniTable
from sfa.util.debug import log

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
        Parameter(str, "Human readable name (hrn) of record to be removed")
        ]

    returns = Parameter(int, "1 if successful")
    
    def call(self, cred, type, hrn):
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
