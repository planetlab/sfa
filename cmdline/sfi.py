#! /usr/bin/env python
from __future__ import with_statement

# sfi -- slice-based facility interface

import sys
import os, os.path
from optparse import OptionParser
from util.cert import Keypair, Certificate
from util.credential import Credential
from util.geniclient import GeniClient

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
      print "Contacting Registry at:", registry_url

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
   registry = GeniClient(registry_url, key_file, cert_file)
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
      user_cred = get_credential(None, "user", user)
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

   file = os.path.join(sfi_dir, "authority.cred")
   if (os.path.isfile(file)):
      auth_cred = Credential(filename=file)
      return auth_cred
   else:
      # bootstrap authority credential from user credential
      user_cred = get_user_cred()
      auth_cred = get_credential(user_cred, "sa", authority)
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
      slice_cred = get_credential(user_cred, "slice", name)
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
      print "No such rspec file"
      sys.exit(1)

def get_record_file(record):
   if (os.path.isabs(record)):
      file = record
   else:
      file = os.path.join(sfi_dir, record)
   if (os.path.isfile(file)):
      return file
   else:
      print "No such registry record file"
      sys.exit(1)

#
# Generate sub-command parser
#
def create_cmd_parser(command):
   cmdargs = {"list": "name",
              "show": "name",
              "remove": "name",
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
   if command not in cmdargs:
      print "Invalid command\n"
      print "Commands:list,show,remove,add,update,nodes,slices,resources,create,delete,start,stop,reset"
      sys.exit(2)

   parser = OptionParser(usage="sfi [sfi_options] %s [options] %s" \
      % (command, cmdargs[command]))
   if command in ("nodes", "resources"):
      parser.add_option("-f", "--format", dest="format",type="choice",
           help="output format (dns|ip|hrn|rspec)",default="rspec",
           choices=("dns","ip","hrn","rspec"))
   elif command in ("list", "show", "remove"):
      parser.add_option("-t", "--type", dest="type",type="choice",
           help="type filter (user|slice|sa|ma|node|aggregate)", 
           choices=("user","slice","sa","ma","node","aggregate", "all"),
           default="all")
   return parser

#
# Main: parse arguments and dispatch to command
#
def main():
   global verbose

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
   (options, args) = parser.parse_args()
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

   # Dispatch to selected command
   try:
      globals()[command](cmd_opts, cmd_args)
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
   result = registry.list(user_cred, args[0])
   display_record(opts.type, results)
   return

# show named registry record
def show(opts, args):
   global registry
   user_cred = get_user_cred() 
   result = reg_chan.resolve(user_cred, args[0])
   display_record(opts.type, results)
   return

# removed named registry record
#   - have to first retrieve the record to be removed
def remove(opts, args):
   global registry
   auth_cred = get_auth_cred() 
   results = registry.resolve(auth_cred, args[0])
   record = filter_record(opts.type, results)
   return registry.remove(auth_cred, record)

# add named registry record
def add(opts, args):
   global registry
   auth_cred = get_auth_cred() 
   rec_file = get_record_file(args[1])
   with open(rec_file) as f:
      record = f.read()
   return registry.register(auth_cred, record)

# update named registry entry
def update(opts, args):
   global registry
   user_cred = get_user_cred() 
   rec_file = get_record_file(args[1])
   with open(rec_file) as f:
      record = f.read()
   return registry.update(user_cred, record)

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
   return

# list instantiated slices
def slices(opts, args):
   global slicemgr
   user_cred = get_user_cred() 
   result = slicemgr.list_slices(user_cred)
   display_rspec(opts.format, results)
   return

# show rspec for named slice
def resources(opts, args):
   global slicemgr
   slice_cred = get_slice_cred(args[0]) 
   result = slicemgr.get_slice_resources(slice_cred, args[0])
   display_rspec(opts.format, result)
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
# Display and Filter RSpecs and Records
#   - to be replace by EMF-generated routines
#
#

def display_rspec(format, rspec):
   print "display rspec"
   return

def display_record(type, record):
   rec = filter_record(type, record)
   print "display record"
   return

def filter_record(type, record):
   print "filter record"
   return


if __name__=="__main__":
   main()
