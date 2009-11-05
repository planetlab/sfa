#
# Geniwrapper XML-RPC and SOAP interfaces
#
### $Id: api.py 15596 2009-10-31 21:42:05Z anil $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/plc/api.py $
#

import sys
import os
import traceback
import string
import xmlrpclib

from sfa.trust.auth import Auth
from sfa.util.config import *
from sfa.util.faults import *
from sfa.util.debug import *
from sfa.trust.rights import *
from sfa.trust.credential import *
from sfa.trust.certificate import *
from sfa.util.misc import *
from sfa.util.sfalogging import *
from sfa.util.api import *


class ComponentAPI(BaseAPI):

    
    def __init__(self, config = "/etc/sfa/sfa_config", encoding = "utf-8", methods='sfacomponent.methods',
                 peer_cert = None, interface = None, key_file = None, cert_file = None):

        BaseAPI.__init__(self, config=config, encoding=encoding, methods=methods, peer_cert=peer_cert, 
                         interface, key_file, cert_file) 
        self.encoding = encoding

        # Better just be documenting the API
        if config is None:
            return

