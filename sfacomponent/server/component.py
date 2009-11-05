#
# Component is a GeniServer that implements the Component interface
#
### $Id: 
### $URL: 
#

import tempfile
import os
import time
import sys

from sfa.util.geniserver import GeniServer
 
# GeniLight client support is optional
try:
    from egeni.geniLight_client import *
except ImportError:
    GeniClientLight = None            

##
# Component is a GeniServer that serves component operations.

class Component(GeniServer):
    ##
    # Create a new registry object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)

    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)
        self.server.interface = 'component' 
