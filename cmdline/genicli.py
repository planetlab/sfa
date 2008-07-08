# command line interface

import getopt
import sys
from clientstub import *

long_opts = ["username=", "usertype=", "help", "outfile=", "credfile="]

# default command line options
username = "planetlab.scott.pl.smbaker"
usertype = "user"
opname = "lookup"
type = None
hrn = None
cred_name = None
id_file = None
key_file = None
acc_file = None
cred_file = None
leaf_name = None
server_host = "127.0.0.1"
server_port = 8002
out_file = None

def showhelp():
   print "syntax: cli <options> command <args>"
   print "options:"
   print "    --username       ... hrn of user performing op"
   print "    --usertype       ... kind of user performing op (user, slice, ...)"
   print "    --outfile        ... write reply to file"
   print "    --credfile       ... credential to pass"
   print "commands:"
   print "    lookup <type> <hrn>"
   print "    dumpCredential"
   print "    getCredential <cred_name>"
   print "    start <hrn>"

def process_options():
   global username, usertype, opname
   global type, hrn, cred_name
   global leaf_name
   global id_file, cred_file
   global acc_file, key_file, out_file

   (options, args) = getopt.getopt(sys.argv[1:], '', long_opts)
   for opt in options:
       name = opt[0]
       val = opt[1]

       if name == "--username":
           username = val
       elif name == "--usertype":
           usertype = val
       elif name == "--help":
           showhelp()
           sys.exit(0)
       elif name == "--outfile":
           out_file = val
       elif name == "--credfile":
           cred_file = val

   if not args:
       report.error("no operation specified")
       sys.exit(-1)

   opname = args[0]

   if opname == "lookup":
       if len(args) < 3:
           report.error("syntax: lookup <type> <hrn>")
           sys.exit(-1)
       type = args[1]
       hrn = args[2]

   elif opname == "getCredential":
       if len(args) < 1:
           report.error("syntax: getcredential <cred_name>")
           sys.exit(-1)
       cred_name = args[1]

   elif opname == "start":
       if len(args) < 1:
           report.error("syntax: start <hrn>")
           sys.exit(-1)
       hrn = args[1]

   if not leaf_name:
       leaf_name = get_leaf(username)

   if id_file == None:
       id_file = leaf_name + ".cert"

   if key_file == None:
       key_file = leaf_name + ".pkey"

   if acc_file == None:
       acc_file = "acc_file"

   if cred_file == None:
       cred_file = "cred_file"

def show_options():
   print " username:", username
   print "     leaf:", leaf_name
   print " usertype:", usertype
   print "  id_file:", id_file
   print " key_file:", key_file
   print " acc_file:", acc_file
   print "cred_file:", cred_file
   print "operation:", opname
   print "     type:", type
   print "      hrn:", hrn
   print "cred_name:", cred_name
   print " out_file:", out_file

def get_authority(x):
    parts = x.split(".")
    return ".".join(parts[:3])

def compose_message():
   g_params = {}
   p_params = {}
   dict = {"opname": opname}

   if opname == "lookup":
      g_params["hrn"] = hrn
      g_params["type"] = type

   elif opname == "getCredential":
      g_params["cred_name"] = cred_name

      parts = cred_name.split(":")
      if len(parts) < 2:
          report.error("bad format for getCredential (slice:hrn.of.slice, ...)")

      # XXX smbaker: this looks redundant
      if parts[0] == "slice":
         g_params["hrn"] = get_authority(parts[1])
         g_params["type"] = "slice"

   elif opname == "start":
      g_params["hrn"] = hrn
      g_params["type"] = "slice"

   dict["g_params"] = g_params
   dict["p_params"] = p_params

   return dict

def do_remote_op():
   message = compose_message()

   client = GENIClient(username, usertype, id_file, key_file, acc_file, cred_file)

   server = client.connect(server_host, server_port)
   if not server:
       report.error("failed to connect to server")
       sys.exit(-1)

   report.trace("message:" + str(message))

   server.write(str(message))

   reply = server.read(MAX_RESULT)
   if not reply:
      report.error("No reply")
      sys.exit(-1)

   if out_file:
      open(out_file, "w").write(reply)
   else:
      print "////// RESULT: //////"
      print reply

def dumpCredential():
    cred_str = open(cred_file).read()
    c_pem = X509.load_cert_string(cred_str)
    subjectAltName = c_pem.get_ext("subjectAltName").get_value()
    info_cert = get_cred_info(subjectAltName)

    print "subject:", c_pem.get_subject().CN
    print "issuer:", c_pem.get_issuer().CN
    print "cred_str:"
    print " ", subjectAltName
    print "rights:"
    op_set = info_cert['operation_set']
    for item in op_set.keys():
       rights = op_set[item]
       print " ", item, ", ".join(rights)

    print "interfaces:"
    interfaces = info_cert['on_interfaces']
    for item in interfaces:
       print " ", item['lbl'], item['type'], item['name']

def main():
   process_options()
   show_options()

   if opname == "dumpCredential":
      dumpCredential()
      sys.exit(0)
      
   elif opname == "help":
      showhelp()
      sys.exit(0)

   elif (opname == "lookup") or \
        (opname == "getCredential") or \
        (opname == "start"):
      do_remote_op()

   else:
      report.error("unknown operation: " + opname)

if __name__=="__main__":
   main()

