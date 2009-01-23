# command line interface

import getopt
import sys
import os
from cert import *
from geniclient import *
from geniticket import *

long_opts = ["keyfile=", "help", "outfile=", "credfile=", "ticketfile=",
             "username=", "email=", "ip=", "dns=", "dump_parents", "server=",
             "filter=", "short"]

# default command line options
username = "client"
opname = None
type = None
hrn = None

key_file = None
cred_file = None
cert_file = None
out_file = None
ticket_file = None

short = False
ip = None
dns = None
email = None
uuid = None
gid_pkey_fn = None
gid_fn = None
filter = None

dump_fn = None

dump_parents = False

leaf_name = None
server_url = "https://localhost:12345/"

def get_leaf(hrn):
    parts = hrn.split(".")
    return parts[-1]

def showhelp():
   print "syntax: cli <options> command <args>"
   print "options:"
   print "    --username       ... username (or hrn) of user making call"
   print "    --outfile       ... save response to a file"
   print "    --credfile       ... credential of user making call (or 'None')"
   print "    --keyfile        ... private key file of user making call"
   print "    --ticketfile     ... filename of ticket (for redeemticket)"
   print "    --email          ... email address (for registering users)"
   print "    --ip             ... IP address (for registering nodes)"
   print "    --dns            ... DNS address (for registering nodes)"
   print "    --dump_parents   ... dump parents"
   print "    --server         ... geni server (registry/component) to connect to"
   print "    --filter <type>  ... filter the results of a list operation (user | slice | node ...)"
   print "    --short          ... list records in short format (name only)"
   print "commands:"
   print "    resolve <hrn>"
   print "    dumpCredential <filename>"
   print "    dumpGid <filename>"
   print "    getCredential <type> <hrn>"
   print "    list <hrn>"
   print "    start <hrn>"
   print "    createKey <filename>"
   print "    createGid <hrn> <uuid|None> <pubkey_fn>"
   print "    register <type> <hrn> <gid_filename>"
   print "    remove <type> <hrn>"
   print "    update <type> <hrn>"
   print "    startSlice"
   print "    stopSlice"
   print "    listSlices"

def process_options():
   global username
   global opname
   global type, hrn
   global cert_file, cred_file
   global key_file, out_file, ticket_file
   global uuid, pkey_fn, gid_fn, email, gid_pkey_fn, ip, dns
   global dump_parents
   global server_url
   global filter
   global short
   global dump_fn

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
       elif name == "--ticketfile":
           ticket_file = val
       elif name == "--email":
           email = val
       elif name == "--ip":
           ip = val
       elif name == "--dns":
           dns = val
       elif name == "--dump_parents":
           dump_parents = True
       elif name == "--server":
           server_url = val
       elif name == "--filter":
           filter = val
       elif name == "--short":
           short = True

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

   elif opname == "list":
       if len(args) < 2:
           print "syntax: list <hrn>"
           sys.exit(-1)
       hrn = args[1]


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

   elif opname == "update":
       if len(args) < 3:
           print "syntax: update <type> <hrn>"
       type = args[1]
       hrn = args[2]

   elif opname == "getTicket":
       if len(args) < 2:
           print "syntax: getTicket <hrn>"
           sys.exit(-1)
       hrn = args[1]

   elif opname == "dumpGid":
       if len(args) < 2:
           print "syntax: dumpGid <filename>"
           sys.exit(-1)
       dump_fn = args[1]

   leaf_name = get_leaf(username)

   if cert_file == None:
       cert_file = leaf_name + ".cert"

   if key_file == None:
       key_file = leaf_name + ".pkey"

   if cred_file == None:
       cred_file = leaf_name + ".cred"

def show_options():
   print "   server:", server_url
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

def dumpGid():
   gid = GID(filename = dump_fn)
   gid.dump()

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
   if (opname != "dumpCredential") and (opname != "help") and (opname != "createKey") and (opname != "dumpGid"):
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
   if (cred_file=="None") or (opname == "help") or (opname == "createKey") or \
      (opname == "redeemTicket") or (opname == "dumpCredential") or (opname == "dumpGid"):
      cred = None
   else:
      cred = Credential(filename = cred_file)

   if opname == "dumpCredential":
      dumpCredential()

   elif opname == "dumpGid":
      dumpGid()

   elif opname == "help":
      showhelp()

   elif opname == "createKey":
      createKey()

   elif (opname == "resolve"):
      result = client.resolve(cred, hrn)
      if result:
          for record in result:
              print "RESULT:"
              record.dump(dump_parents=dump_parents)
      else:
          print "NO RESULT"

   elif (opname == "getCredential"):
      result = client.get_credential(cred, type, hrn)
      if result:
          print "RESULT:"
          result.dump(dump_parents=dump_parents)
          if out_file:
              file(out_file, "w").write(result.save_to_string(save_parents=True))
      else:
          print "NO RESULT"

   elif (opname == "list"):
      result = client.list(cred, hrn)
      if result:
          if filter:
              result = [r for r in result if r.type==filter]
          print "RESULT:"
          for record in result:
              if short:
                  print "  ", record.get_name()
              else:
                  record.dump(dump_parents=dump_parents)
      else:
          print "NO RESULT"

   elif (opname == "createGid"):
       # try loading it from a private or a public key file
       pkey_string = load_publickey_string(gid_pkey_fn)

       gid = client.create_gid(cred, hrn, uuid, pkey_string)
       if gid:
           print "RESULT:"
           gid.dump(dump_parents=dump_parents)
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

       if type == "node":
           if not ip:
               print "ERROR: must specify --ip <addr> when registering nodes"
           geni_info['ip'] = ip
           if not dns:
               print "ERROR: must specify --dns <addr> when registering nodes"
           geni_info['dns'] = dns

       gid = GID(filename=gid_fn)
       record = GeniRecord(name=hrn, gid=gid, type=type, pointer=-1)
       record.set_geni_info(geni_info)

       result = client.register(cred, record)

   elif (opname == "remove"):
       client.remove(cred, type, hrn)

   elif (opname == "update"):
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
           geni_info = record.get_geni_info()

           if email:
               geni_info['email'] = email
           if ip:
               geni_info['ip'] = ip
           if dns:
               geni_info['dns'] = dns

           client.update(cred, record)

   elif (opname == "stopSlice"):
       client.stop_slice(cred)

   elif (opname == "startSlice"):
       client.start_slice(cred)

   elif (opname == "resetSlice"):
       client.reset_slice(cred)

   elif (opname == "deleteSlice"):
       client.delete_slice(cred)

   elif (opname == "listSlices"):
       result = client.list_slices(cred)
       print "RESULT:"
       print "\n".join(result)
       if out_file:
           file(out_file,"w").write("\n".join(result))

   elif (opname == "getTicket"):
      result = client.get_ticket(cred, hrn, {})
      if result:
          print "RESULT:"
          result.dump(dump_parents=dump_parents)
          if out_file:
              file(out_file,"w").write(result.save_to_string(save_parents=True))
      else:
          print "NO RESULT"

   elif (opname == "redeemTicket"):
       ticket = Ticket(filename = ticket_file)
       result = client.redeem_ticket(ticket)

   else:
      print "unknown operation: " + opname

if __name__=="__main__":
   main()

