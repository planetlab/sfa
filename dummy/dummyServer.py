import tempfile
import os

from cert import *
from gid import *
from geniserver import *

# DummyRegistry implements the security layer for a registry. It creates GIDs
#   by using the public key contained in client's certificate. 


class DummyRegistry(GeniServer):
    gid_dict = {}

    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

    def register_functions(self):
        GeniServer.register_functions(self)
        self.server.register_function(self.get_self_credential)
        self.server.register_function(self.get_credential)
        self.server.register_function(self.get_gid)

    def resolve_gid(self, name):
        gid = self.gid_dict.get(name, None)
        if gid:
            return [gid]

        # assume the user is who he says he is, and create a GID for him
        peer_cert = self.server.peer_cert
        gid = GID(subject=name, uuid=create_uuid(), hrn=name)
        gid.set_pubkey(peer_cert.get_pubkey())
        gid.set_issuer(key=self.key, cert=self.cert)
        gid.encode()
        gid.sign()

        self.gid_dict[name] = gid

        return [gid]

    def get_gid(self, name):
        gid_list = self.resolve_gid(name)
        gid_string_list = []
        for gid in gid_list:
            gid_string_list.append(gid.save_to_string())
        return gid_string_list

    def get_self_credential(self, type, name):
        client_gid = self.resolve_gid(name)[0]
        cred = Credential(subject = client_gid.get_subject())
        cred.set_gid_caller(client_gid)
        cred.set_issuer(key=self.key, cert=self.cert)
        cred.set_pubkey(client_gid.get_pubkey())
        cred.encode()
        cred.sign()
        return cred.save_to_string()

    def get_credential(self, cred, type, name):
        if not cred:
            return get_self_credential(self, type, name)

        self.decode_authentication(cred)

        object_gid = self.resolve_gid(name)[0]
        new_cred = Credential(subject = object_gid.get_subject())
        new_cred.set_gid_caller(self.client_gid)
        new_cred.set_gid_object(object_gid)
        new_cred.set_issuer(key=self.key, cert=self.cert)
        new_cred.set_pubkey(object_gid.get_pubkey())
        new_cred.encode()
        new_cred.sign()

        return new_cred.save_to_string()

if __name__ == "__main__":
    key_file = "dummyserver.key"
    cert_file = "dummyserver.cert"

    # if no key is specified, then make one up
    if (not os.path.exists(key_file)) or (not os.path.exists(cert_file)):
        key = Keypair(create=True)
        key_file = "dummyserver.key"
        key.save_to_file(key_file)

        cert = Certificate(subject="dummy")
        cert.set_issuer(key=key, subject="dummy")
        cert.set_pubkey(key)
        cert.sign()
        cert.save_to_file(cert_file)

    s = DummyRegistry("localhost", 12345, key_file, cert_file)
    s.run()

