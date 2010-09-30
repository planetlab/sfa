### $Id: get_credential.py 15321 2009-10-15 05:01:21Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/methods/get_credential.py $

from sfa.trust.credential import *
from sfa.trust.rights import *
from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.util.record import SfaRecord
from sfa.methods.GetSelfCredential import GetSelfCredential

class get_self_credential(GetSelfCredential):
    """
    Deprecated. Use GetSelfCredential instead.

    Retrive a credential for an object
    @param cert certificate string 
    @param type type of object (user | slice | sa | ma | node)
    @param hrn human readable name of object (hrn or urn)

    @return the string representation of a credential object  
    """

    interfaces = ['registry']
    
    accepts = [
        Parameter(str, "Human readable name (hrn or urn)"),
        Parameter(str, "certificate"),
        Mixed(Parameter(str, "Request hash"),
              Parameter(None, "Request hash not specified"))
        ]

    returns = Parameter(str, "String representation of a credential object")

    def call(self, cert, type, xrn, origin_hrn=None):
        """
        get_self_credential a degenerate version of get_credential used by a client
        to get his initial credential when de doesnt have one. This is the same as
        get_credetial(..., cred = None, ...)

        The registry ensures that the client is the principal that is named by
        (type, name) by comparing the public key in the record's  GID to the
        private key used to encrypt the client side of the HTTPS connection. Thus
        it is impossible for one principal to retrive another principal's
        credential without having the appropriate private key.

        @param type type of object (user | slice | sa | ma | node)
        @param hrn human readable name of authority to list
        @return string representation of a credential object
        """
        return GetSelfCredential.call(self, cert, xrn, type)
