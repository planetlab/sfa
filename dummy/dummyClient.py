import os

from geniclient import *
from cert import *
from gid import *

key_file = "dummyclient.key"
cert_file = "dummyclient.cert"

if (not os.path.exists(key_file)) or (not os.path.exists(cert_file)):
    key = Keypair(create=True)
    key.save_to_file(key_file)

    cert = Certificate(subject="dummyclient")
    cert.set_pubkey(key)
    cert.set_issuer(key=key, subject="dummyclient")
    cert.sign()
    cert.save_to_file(cert_file)

c = GeniClient("https://localhost:12345/", key_file, cert_file)

gid = c.get_gid("planetlab.smbaker.dummy.client")[0]
gid.save_to_file("dummyclient.gid")

print "gid: ", gid.get_subject(), "saved to dummyclient.gid"

cred = c.get_self_credential("user", "planetlab.smbaker.dummy.client")
cred.save_to_file("dummyclient.cred")

print "cred: ", cred.get_subject(), "saved to dummyclient.cred"

object_cred = c.get_credential(cred, "slice", "planetlab.smbaker.dummy.slice")
object_cred.save_to_file("dummyslice.cred")

print "cred: ", object_cred.get_subject(), "saved to dummyslice.cred"
