#! /usr/bin/env python
from __future__ import with_statement

# sfi -- slice-based facility interface

import sys
import os, os.path
import tempfile
from optparse import OptionParser
from geni.util.cert import Keypair, Certificate
from geni.util.credential import Credential
from geni.util.geniclient import GeniClient
from geni.util.gid import create_uuid
from geni.util.record import GeniRecord

sfi_dir = os.path.expanduser("~/.sfi/")
slicemgr = None
registry = None
user = None
authority = None
verbose = False

#
# Establish Connection to SliceMgr and Registry Servers
#
def set_servers(options):
   global slicemgr
   global registry
   global user
   global authority

   # Set SliceMgr URL
   if (options.sm is not None):
      sm_url = options.sm
   elif ("SFI_SM" in os.environ):
      sm_url = os.environ["SFI_SM"]
   else:
      print "No Known Slice Manager"
      sys.exit(1)

   # Set Registry URL
   if (options.registry is not None):
      reg_url = options.registry
   elif ("SFI_REGISTRY" in os.environ):
      reg_url = os.environ["SFI_REGISTRY"]
   else:
      print "No Known Registry Server"
      sys.exit(1)

   if options.verbose :
      print "Contacting Slice Manager at:", sm_url
      print "Contacting Registry at:", reg_url

   # Set user HRN
   if (options.user is not None):
      user = options.user
   elif ("SFI_USER" in os.environ):
      user = os.environ["SFI_USER"]
   else:
      print "No Known User Name"
      sys.exit(1)

   # Set authority HRN
   if (options.auth is not None):
      authority = options.auth
   elif ("SFI_AUTH" in os.environ):
      authority = os.environ["SFI_AUTH"]
   else:
      authority = None

   # Get key and certificate
   key_file = get_key_file()
   cert_file = get_cert_file(key_file)

   # Establish connection to server(s)
   slicemgr = GeniClient(sm_url, key_file, cert_file)
   registry = GeniClient(reg_url, key_file, cert_file)
   return

#
# Get various credential and spec files
#
# Establishes limiting conventions
#   - conflates MAs and SAs
#   - assumes last token in slice name is unique
#
# Bootstraps credentials
#   - bootstrap user credential from self-signed certificate
#   - bootstrap authority credential from user credential
#   - bootstrap slice credential from user credential
#

def get_leaf(name):
   parts = name.split(".")
   return parts[-1]

def get_key_file():
   file = os.path.join(sfi_dir, get_leaf(user) + ".pkey")
   if (os.path.isfile(file)):
      return file
   else:
      print "Key file", file, "does not exist"
      sys.exit(-1)
   return

def get_cert_file(key_file):
   global verbose

   file = os.path.join(sfi_dir, get_leaf(user) + ".cert")
   if (os.path.isfile(file)):
      return file
   else:
      k = Keypair(filename = key_file)
      cert = Certificate(subject=user)
      cert.set_pubkey(k)
      cert.set_issuer(k, user)
      cert.sign()
      if verbose :
         print "Writing self-signed certificate to", file
      cert.save_to_file(file)
      return file

def get_user_cred():
   global user

   file = os.path.join(sfi_dir, get_leaf(user) + ".cred")
   if (os.path.isfile(file)):
      user_cred = Credential(filename=file)
      return user_cred
   else:
      # bootstrap user credential
      user_cred = registry.get_credential(None, "user", user)
      if user_cred:
         user_cred.save_to_file(file, save_parents=True)
         if verbose:
            print "Writing user credential to", file
         return user_cred
      else:
         print "Failed to get user credential"
         sys.exit(-1)

def get_auth_cred():
   global authority

   if not authority:
      print "no authority specified. Use -a or set SF_AUTH"
      sys.exit(-1)

   file = os.path.join(sfi_dir, get_leaf("authority") +".cred")
   if (os.path.isfile(file)):
      auth_cred = Credential(filename=file)
      return auth_cred
   else:
      # bootstrap authority credential from user credential
      user_cred = get_user_cred()
      auth_cred = registry.get_credential(user_cred, "sa", authority)
      if auth_cred:
         auth_cred.save_to_file(file, save_parents=True)
         if verbose:
            print "Writing authority credential to", file
         return auth_cred
      else:
         print "Failed to get authority credential"
         sys.exit(-1)

def get_slice_cred(name):
   file = os.path.join(sfi_dir, "slice_" + get_leaf(name) + ".cred")
   if (os.path.isfile(file)):
      slice_cred = Credential(filename=file)
      return slice_cred
   else:
      # bootstrap slice credential from user credential
      user_cred = get_user_cred()
      slice_cred = registry.get_credential(user_cred, "slice", name)
      if slice_cred:
         slice_cred.save_to_file(file, save_parents=True)
         if verbose:
            print "Writing slice credential to", file
         return slice_cred
      else:
         print "Failed to get slice credential"
         sys.exit(-1)

def get_rspec_file(rspec):
   if (os.path.isabs(rspec)):
      file = rspec
   else:
      file = os.path.join(sfi_dir, rspec)
   if (os.path.isfile(file)):
      return file
   else:
      print "No such rspec file", rspec
      sys.exit(1)

def get_record_file(record):
   if (os.path.isabs(record)):
      file = record
   else:
      file = os.path.join(sfi_dir, record)
   if (os.path.isfile(file)):
      return file
   else:
      print "No such registry record file", record
      sys.exit(1)

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


#
# Generate sub-command parser
#
def create_cmd_parser(command, additional_cmdargs = None):
   cmdargs = {"list": "name",
              "show": "name",
              "remove": "name",
              "creategid": "hrn publickey_fn",
              "add": "name record",
              "update": "name record",
              "nodes": "[name]",
              "slices": "",
              "resources": "name",
              "create": "name rspec",
              "delete": "name",
              "reset": "name",
              "start": "name",
              "stop": "name"
             }

   if additional_cmdargs:
      cmdargs.update(additional_cmdargs)

   if command not in cmdargs:
      print "Invalid command\n"
      print "Commands: ",
      for key in cmdargs.keys():
          print key+",",
      print ""
      sys.exit(2)

   parser = OptionParser(usage="sfi [sfi_options] %s [options] %s" \
      % (command, cmdargs[command]))
   if command in ("nodes", "resources"):
      parser.add_option("-f", "--format", dest="format",type="choice",
           help="display format (dns|ip|hrn|rspec)",default="rspec",
           choices=("dns","ip","hrn","rspec"))
   if command in ("list", "show", "remove"):
      parser.add_option("-t", "--type", dest="type",type="choice",
           help="type filter (user|slice|sa|ma|node|aggregate)",
           choices=("user","slice","sa","ma","node","aggregate", "all"),
           default="all")
   if command in ("show", "list", "nodes", "resources", "creategid"):
      parser.add_option("-o", "--output", dest="file",
           help="output XML to file", metavar="FILE", default=None)
   return parser

def create_parser():
   # Generate command line parser
   parser = OptionParser(usage="sfi [options] command [command_options] [command_args]",
        description="Commands: list,show,remove,add,update,nodes,slices,resources,create,delete,start,stop,reset")
   parser.add_option("-r", "--registry", dest="registry",
        help="root registry", metavar="URL", default=None)
   parser.add_option("-s", "--slicemgr", dest="sm",
        help="slice manager", metavar="URL", default=None)
   parser.add_option("-d", "--dir", dest="dir",
        help="working directory", metavar="PATH", default = sfi_dir)
   parser.add_option("-u", "--user", dest="user",
        help="user name", metavar="HRN", default=None)
   parser.add_option("-a", "--auth", dest="auth",
        help="authority name", metavar="HRN", default=None)
   parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose", default=False,
        help="verbose mode")
   parser.disable_interspersed_args()

   return parser

def dispatch(command, cmd_opts, cmd_args):
   globals()[command](cmd_opts, cmd_args)

#
# Main: parse arguments and dispatch to command
#
def main():
   global verbose

   parser = create_parser()
   (options, args) = parser.parse_args()

   if len(args) <= 0:
        print "No command given. Use -h for help."
        return -1

   command = args[0]
   (cmd_opts, cmd_args) = create_cmd_parser(command).parse_args(args[1:])
   verbose = options.verbose
   if verbose :
      print options.registry, options.sm, options.dir, options.verbose,\
         options.user, options.auth
      print command
      if command in ("nodes", "resources"):
         print cmd_opts.format
      elif command in ("list","show","remove"):
         print cmd_opts.type
      print cmd_args

   set_servers(options)

   try:
      dispatch(command, cmd_opts, cmd_args)
   except KeyError:
      print "Command not found:", command
      sys.exit(1)

   return

#
# Following functions implement the commands
#
# Registry-related commands
#

# list entires in named authority registry
def list(opts, args):
   global registry
   user_cred = get_user_cred()
   list = registry.list(user_cred, args[0])
   list = filter_records(opts.type, list)
   display_records(list)
   if opts.file:
       save_records_to_file(opts.file, list)
   return

# show named registry record
def show(opts, args):
   global registry
   user_cred = get_user_cred()
   records = registry.resolve(user_cred, args[0])
   records = filter_records(opts.type, records)
   if not records:
      print "No record of type", opts.type
   display_records(records)
   if opts.file:
       save_records_to_file(opts.file, records)
   return

# removed named registry record
#   - have to first retrieve the record to be removed
def remove(opts, args):
   global registry
   auth_cred = get_auth_cred()
   return registry.remove(auth_cred, opts.type, args[0])

def creategid(opts, args):
   global registry
   auth_cred = get_auth_cred()
   hrn = args[0]
   pkey_string = load_publickey_string(args[1])
   gid = registry.create_gid(auth_cred, hrn, create_uuid(), pkey_string)
   if (opts.file is not None):
      gid.save_to_file(opts.file, save_parents=True)
   else:
      print "I created your gid, but you did not ask me to save it"

# add named registry record
def add(opts, args):
   global registry
   auth_cred = get_auth_cred()
   rec_file = get_record_file(args[0])
   record = load_record_from_file(rec_file)
   return registry.register(auth_cred, record)

# update named registry entry
def update(opts, args):
   global registry
   user_cred = get_user_cred()
   rec_file = get_record_file(args[0])
   record = load_record_from_file(rec_file)

   if record.get_type() == "user":
       cred = user_cred
   elif record.get_type() in ["sa", "ma", "slice", "node"]:
       cred = get_auth_cred()
   else:
       raise "unknown record type" + record.get_type()

   return registry.update(cred, record)

#
# Slice-related commands
#

# list available nodes
def nodes(opts, args):
   global slicemgr
   user_cred = get_user_cred() 
   if (len(args) == 0):
      context = None
   else:
      context = args[0]
   result = slicemgr.list_nodes(user_cred, context)
   display_rspec(opts.format, result)
   if (opts.file is not None):
      save_rspec_to_file(opts.file, result)
   return

# list instantiated slices
def slices(opts, args):
   global slicemgr
   user_cred = get_user_cred() 
   result = slicemgr.list_slices(user_cred)
   #display_rspec(opts.format, results)
   print result
   return

# show rspec for named slice
def resources(opts, args):
   global slicemgr
   slice_cred = get_slice_cred(args[0])
   result = slicemgr.list_resources(slice_cred, args[0])
   display_rspec(opts.format, result)
   if (opts.file is not None):
      save_rspec_to_file(opts.file, result)
   return

# created named slice with given rspec
def create(opts, args):
   global slicemgr
   slice_cred = get_slice_cred(args[0])
   rspec_file = get_rspec_file(args[1])
   with open(rspec_file) as f:
      rspec = f.read()
   return slicemgr.create_slice(slice_cred, rspec)

# delete named slice
def delete(opts, args):
   global slicemgr
   slice_cred = get_slice_cred(args[0])
   return slicemgr.delete_slice(slice_cred)

# start named slice
def start(opts, args):
   global slicemgr
   slice_cred = get_slice_cred(args[0])
   return slicemgr.start_slice(slice_cred)

# stop named slice
def stop(opts, args):
   global slicemgr
   slice_cred = get_slice_cred(args[0])
   return slicemgr.stop_slice(slice_cred)

# reset named slice
def reset(opts, args):
   global slicemgr
   slice_cred = get_slice_cred(args[0])
   return slicemgr.reset_slice(slice_cred)

#
#
# Display, Save, and Filter RSpecs and Records
#   - to be replace by EMF-generated routines
#
#

def display_rspec(format, rspec):
   print "display rspec"
   print rspec
   return

def save_rspec_to_file(file, rspec):
   print "save rspec"
   return

def display_records(recordList):
   for record in recordList:
      display_record(record)

def display_record(record):
   record.dump(False)
   return

def filter_records(type, records):
   filtered_records = []
   for record in records:
       if (record.get_type() == type) or (type == "all"):
           filtered_records.append(record)
   return filtered_records

def save_records_to_file(filename, recordList):
   index = 0
   for record in recordList:
       if index>0:
           save_record_to_file(filename + "." + str(index), record)
       else:
           save_record_to_file(filename, record)
       index = index + 1

def save_record_to_file(filename, record):
   print "saving record", record.name, "to file", filename
   str = record.save_to_string()
   file(filename, "w").write(str)
   return

def load_record_from_file(filename):
   str = file(filename, "r").read()
   record = GeniRecord(string=str)
   return record

if __name__=="__main__":
   main()
