# * require certificate as an argument
# * lookup gid in db
# * get pubkey from gid
# * if certifacate matches pubkey from gid, return gid, else raise exception
#  if not peer.is_pubkey(gid.get_pubkey()):
#            raise ConnectionKeyGIDMismatch(gid.get_subject())

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.trust.gid import GID
from sfa.trust.certificate import Certificate
from sfa.util.genitable import GeniTable

class get_gids(Method):
    """
    Get a list of record information (hrn, gid and type) for 
    the specified hrns.

    @param cred credential string 
    @param cert certificate string 
    @return    
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Certificate string"),
        Mixed(Parameter(str, "Human readable name (hrn)"), 
              Parameter(type([str]), "List of Human readable names (hrn)")) 
        ]

    returns = [Parameter(dict, "Dictionary of gids keyed on hrn")]
    
    def call(self, cred, hrns):
        # validate the credential
        self.api.auth.check(cred, 'getgids')
        table = GeniTable()
        if not isinstance(hrns, list):
            hrns = [hrns]
        records = table.find({'hrn': hrns}, columns=['hrn','type','gid'])
        
        return records 
