from geni.util.faults import *
from geni.util.excep import *
from geni.util.misc import *
from geni.util.method import Method
from geni.util.parameter import Parameter, Mixed
from geni.util.auth import Auth
from geni.aggregate import Aggregates

class slices(Method):
    """
    Get a list of instantiated slices at this authority.      

    @param cred credential string specifying the rights of the caller
    @return list of human readable slice names (hrn).  
    """

    interfaces = ['aggregate', 'slicemgr']
    
    accepts = [
        Parameter(str, "Credential string"),
        ]

    returns = [Parameter(str, "Human readable slice name (hrn)")]
    
    def call(self, cred):
       
        self.api.auth.check(cred, 'listslices')
        slice_hrns = []

        if self.api.interface in ['aggregate']:
            slices = self.api.plshell.GetSlices(self.api.plauth, {}, ['name'])
            slice_hrns = [slicename_to_hrn(self.api.hrn, slice['name']) for slice in slices]
        
        else:
            aggregates = Aggregates()
            credential = self.api.getCredential()
            for aggregate in aggregates:
                slices = aggregates[aggregate].slices(credential)
                slice_hrns.extend(slices)    
            
        return slice_hrns
