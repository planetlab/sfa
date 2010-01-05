# * require certificate as an argument
# * lookup gid in db
# * get pubkey from gid
# * if certifacate matches pubkey from gid, return gid, else raise exception
#  if not peer.is_pubkey(gid.get_pubkey()):
#            raise ConnectionKeyGIDMismatch(gid.get_subject())

from sfa.util.faults import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.trust.gid import GID
from sfa.trust.certificate import Certificate
from sfa.trust.credential import Credential

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
        user_cred = Credential(string=cred)
        origin_hrn = user_cred.get_gid_caller().get_hrn()

        # resolve the record
        manager_base = 'sfa.managers'
        mgr_type = self.api.config.SFA_REGISTRY_TYPE
        manager_module = manager_base + ".registry_manager_%s" % mgr_type
        manager = __import__(manager_module, fromlist=[manager_base])
        records = manager.resolve(self.api, hrns, None, origin_hrn=origin_hrn)
        if not records:
            raise RecordNotFound(hrns)

        gids = []
        allowed_fields =  ['hrn', 'type', 'gid']
        for record in records:
            for key in record.keys():
                if key not in allowed_fields:
                    del(record[key])
        return records    
