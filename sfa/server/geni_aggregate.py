### $Id: aggregate.py 16477 2010-01-05 16:31:37Z thierry $
### $URL: svn+ssh://svn.planet-lab.org/svn/sfa/branches/geni-api/sfa/server/aggregate.py $

import os
import sys
import datetime
import time
import xmlrpclib
from types import StringTypes, ListType

from sfa.util.server import SfaServer
from sfa.util.storage import *
from sfa.util.faults import *
import sfa.util.xmlrpcprotocol as xmlrpcprotocol
import sfa.util.soapprotocol as soapprotocol

# GeniLight client support is optional
try:
    from egeni.geniLight_client import *
except ImportError:
    GeniClientLight = None


class GENIAggregate(SfaServer):

    ##
    # Create a new aggregate object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)     
    def __init__(self, ip, port, key_file, cert_file):
        SfaServer.__init__(self, ip, port, key_file, cert_file)
        self.server.interface = 'geni_am'

