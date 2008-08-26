# command line interface

import getopt
import sys
import os
from cert import *
from geniclient import *

long_opts = ["keyfile=", "help", "outfile=", "credfile=", "username=", "email="]

# default command line options
username = "client"
opname = None
type = None
hrn = None

key_file = None
cred_file = None
cert_file = None
out_file = None

email = None
uuid = None
gid_pkey_fn = None
gid_fn = None

leaf_name = None
server_url = "https://localhost:12345/"

def get_leaf(hrn):
    parts = hrn.split(".")
    return parts[-1]

def showhelp():
   print "syntax: cli <options> command <args>"
   print "options:"
   print "    --username       ... username (or hrn) of user making call"
   print "    --outfile        ... save response to a file"
   print "    --credfile       ... credential of user making call (or 'None')"
   print "    --keyfile        ... private key file of user making call"
   print "    --email          ... email address"
   print "commands:"
   print "    resolve <hrn>"
   print "    dumpCredential"
   print "    getCredential <type> <hrn>"
   print "    start <hrn>"
   print "    createKey <filename>"
   print "    createGid <hrn> <uuid|None> <pubkey_fn>"
   print "    register <type> <hrn> <gid_filename>"
   print "    remove <type> <hrn>"

def process_options():
   global username
   global opname
   global type, hrn
   global cert_file, cred_file
   global key_file, out_file
   global uuid, pkey_fn, gid_fn, email, gid_pkey_fn

   (options, args) = getopt.getopt(sys.argv[1:], '', long_opts)
   for opt in options:
       name = opt[0]
       val = opt[1]

       if name == "--help":
           showhelp()
           sys.exit(0)
       elif name == "--username":
           username = val
       elif name == "--outfile":
           out_file = val
       elif name == "--credfile":
           cred_file = val
       elif name == "--certfile":
           cred_file = val
       elif name == "--keyfile":
           key_file = val
       elif name == "--email":
           email = val

   if not args:
       print "no operation specified"
       sys.exit(-1)

   opname = args[0]

   if opname == "resolve":
       if len(args) < 2:
           print "syntax: resolve <hrn>"
           sys.exit(-1)
       hrn = args[1]

   elif opname == "getCredential":
       if len(args) < 3:
           print "syntax: getcredential <type> <hrn>"
           sys.exit(-1)
       type = args[1]
       hrn = args[2]

   elif opname == "createGid":
       if len(args) < 4:
           print "syntax: createGid <hrn> <uuid|None> <pubkey_fn>"
       hrn = args[1]
       if args[2]=="None":
           uuid=None
       else:
           uuid = int(args[2])
       gid_pkey_fn = args[3]

   elif opname == "register":
       if len(args) < 4:
           print "syntax: register <type> <hrn> <gid_filename>"
       type = args[1]
       hrn = args[2]
       gid_fn = args[3]

   elif opname == "remove":
       if len(args) < 3:
           print "syntax: remove <type> <hrn>"
       type = args[1]
       hrn = args[2]

   leaf_name = get_leaf(username)

   if cert_file == None:
       cert_file = leaf_name + ".cert"

   if key_file == None:
       key_file = leaf_name + ".pkey"

   if cred_file == None:
       cred_file = leaf_name + ".cred"

def show_options():
   print " username:", username
   print "cert_file:", cert_file
   print " key_file:", key_file
   print "cred_file:", cred_file
   print "operation:", opname
   print "     type:", type
   print "      hrn:", hrn
   print " out_file:", out_file

def get_authority(x):
    parts = x.split(".")
    return ".".join(parts[:3])

def dumpCredential():
   pass

# creates a self-signed certificate and private key
def createKey():
   k = Keypair(create=True)

   self_signed = False
   if self_signed:
      ik = k
      iname = username
   else:
      ik = Keypair(create=True)
      iname = "issuer"

   print "writing private key to", key_file
   k.save_to_file(key_file)

   #cert = Certificate(subject=username)
   #cert.set_pubkey(k)
   #cert.set_issuer(ik, iname)
   #cert.sign()
   #print "writing self-signed cert to", cert_file
   #cert.save_to_file(cert_file)

def load_publickey_string(fn):
   f = file(fn,"r")
   key_string = f.read()

   # if the filename is a private key file, then extract the public key
   if "PRIVATE KEY" in key_string:
       outfn = tempfile.mktemp()
       cmd = "openssl rsa -in " + fn + " -pubout -outform PEM -out " + outfn
       os.system(cmd)
       f = file(outfn, "r")
       key_string = f.read()
       os.remove(outfn)

   return key_string

def main():
   process_options()
   show_options()

   result = None

   # if the operation is not a local operation, then create a geniclient to
   # talk to the server
   if (opname != "dumpCredential") and (opname != "help") and (opname != "createKey"):
       if not os.path.exists(key_file):
           print "key file", key_file, "does not exist"
           sys.exit(-1)
       if not os.path.exists(cert_file):
           k = Keypair(filename = key_file)
           cert = Certificate(subject=username)
           cert.set_pubkey(k)
           cert.set_issuer(k, username)
           cert.sign()
           print "writing self-signed cert to", cert_file
           cert.save_to_file(cert_file)
       client = GeniClient(server_url, key_file, cert_file)

   # if a cred_file was specified, then load the credential
   if (cred_file=="None") or (opname == "help") or (opname == "createKey"):
      cred = None
   else:
      cred = Credential(filename = cred_file)

   if opname == "dumpCredential":
      dumpCredential()

   elif opname == "help":
      showhelp()

   elif opname == "createKey":
      createKey()

   elif (opname == "resolve"):
      result = client.resolve(cred, hrn)
      if result:
          for record in result:
              print "RESULT:"
              record.dump()
      else:
          print "NO RESULT"

   elif (opname == "getCredential"):
      result = client.get_credential(cred, type, hrn)
      if result:
          print "RESULT:"
          result.dump()
          if out_file:
              file(out_file, "w").write(result.save_to_string(save_parents=True))
      else:
          print "NO RESULT"

   elif (opname == "list"):
      result = client.list(cred)
      if result:
          for record in result:
              print "RESULT:"
              record.dump()
      else:
          print "NO RESULT"

   elif (opname == "createGid"):
       # try loading it from a private or a public key file
       pkey_string = load_publickey_string(gid_pkey_fn)

       gid = client.create_gid(cred, hrn, uuid, pkey_string)
       if gid:
           print "RESULT:"
           gid.dump()
           if out_file:
               file(out_file,"w").write(gid.save_to_string(save_parents=True))
       else:
           print "NO RESULT"

   elif (opname == "register"):
       geni_info = {}
       if type == "user":
           if not email:
               print "ERROR: must specify --email <addr> when registering users"
           geni_info['email'] = email
       gid = GID(filename=gid_fn)
       record = GeniRecord(name=hrn, gid=gid, type=type, pointer=-1)
       record.set_geni_info(geni_info)

       result = client.register(cred, record)

   elif (opname == "remove"):
       record_list = client.resolve(cred, hrn)
       if not record_list:
           print "no records match hrn"

       matching_records = []
       for record in record_list:
           if record.get_type() == type:
               matching_records.append(record)

       if not matching_records:
           print "records match hrn, but no records match type"

       for record in matching_records:
           client.remove(cred,record)

   else:
      print "unknown operation: " + opname

if __name__=="__main__":
   main()

