##
# Gacks Server
##

import tempfile
import os

import sys

from cert import *
from gid import *
from geniserver import *
from excep import *
from trustedroot import *
from misc import *
from record import *
from geniticket import *

##
# GacksServer is a GeniServer that serves component interface requests.
#

class GacksServer(GeniServer):

    ##
    # Create a new GacksServer object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)

    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

    ##
    # Register the server RPCs for Gacks

    def register_functions(self):
        GeniServer.register_functions(self)
        self.server.register_function(self.get_handle)

    def get_handle(self, rspec):
        pass

    def set_allocator(self, callerGid, Handle, allocatorGid, which, where, reqsig)
        pass

if __name__ == "__main__":
    global TrustedRoots

    key_file = "gacksserver.key"
    cert_file = "gacksserver.cert"

    # if no key is specified, then make one up
    if (not os.path.exists(key_file)) or (not os.path.exists(cert_file)):
        key = Keypair(create=True)
        key.save_to_file(key_file)

        cert = Certificate(subject="component")
        cert.set_issuer(key=key, subject="component")
        cert.set_pubkey(key)
        cert.sign()
        cert.save_to_file(cert_file)

    TrustedRoots = TrustedRootList()

    s = ComponentManager("", 12346, key_file, cert_file)
    s.trusted_cert_list = TrustedRoots.get_list()
    s.run()

