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

import accounts


class ComponentManager(GeniServer):
    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

    def register_functions(self):
        GeniServer.register_functions(self)
        self.server.register_function(self.stop_slice)
        self.server.register_function(self.start_slice)
        self.server.register_function(self.reset_slice)
        self.server.register_function(self.delete_slice)

    def stop_slice(self, cred_str):
        self.decode_authentication(cred_str, "stopslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "stopslice:", slicename
        accounts.get(slicename).start()

    def start_slice(self, cred_str):
        self.decode_authentication(cred_str, "startslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "startslice:", slicename
        accounts.get(slicename).start()

    def reset_slice(self, cred_str):
        self.decode_authentication(cred_str, "resetslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "resetslice:", slicename
        accounts.get(slicename).stop()
        accounts.get(slicename).ensure_destroyed()
        accounts.get(slicename).ensure_created()

    def delete_slice(self, cred_str):
        self.decode_authentication(cred_str, "deleteslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "deleteslice:", slicename
        accounts.get(slicename).ensure_destroyed()


if __name__ == "__main__":
    global TrustedRoots

    key_file = "component.key"
    cert_file = "component.cert"

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

    s = ComponentManager("", 12345, key_file, cert_file)
    s.trusted_cert_list = TrustedRoots.get_list()
    s.run()

