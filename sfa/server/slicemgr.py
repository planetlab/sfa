### $Id: slicemgr.py 16477 2010-01-05 16:31:37Z thierry $
### $URL: http://svn.planet-lab.org/svn/sfa/trunk/sfa/server/slicemgr.py $

import os
import sys
import datetime
import time
from sfa.util.server import *

class SliceMgr(SfaServer):

  
    ##
    # Create a new slice manager object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)     

    def __init__(self, ip, port, key_file, cert_file, config = "/etc/sfa/sfa_config"):
        SfaServer.__init__(self, ip, port, key_file, cert_file)
        self.server.interface = 'slicemgr'      
