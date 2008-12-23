#! /usr/bin/env python
from __future__ import with_statement

# sfi -- slice-based facility interface

import sys
import os, os.path
#from cert import Keypair, Certificate
from optparse import OptionParser
#from util.geniclient import GeniClient

sfi_dir = os.path.expanduser("~/.sfi/")
sm_chan = None
reg_chan = None

#
# Establish Connection to SliceMgr and Registry Servers
#
def set_servers(options):
   global sm_chan
   global reg_chan

   # Set SliceMgr and Registry URLs
   if (options.sm is not None):
      sm = options.sm
   elif ("SM" in os.environ):
      sm = os.environ["SM"]
   else:
      print "No Known Slice Manager"
      sys.exit(1)
   if (options.registry is not None):
      registry = options.registry
   elif ("REGISTRY" in os.environ):
      registry = os.environ["REGISTRY"]
   else:
      print "No Known Registry"
      sys.exit(1)
   if options.verbose:
      print "Contacting Slice Manager at:", sm
      print "Contacting Registry at:", registry

   # SliceMgr and Registry may be available on the same server
#   if (sm == registry):
#      sm_chan = GeniClient(sm, key_file, cert_file)
#      reg_chan = sm_chan
#   else:
#      sm_chan = GeniClient(sm, key_file, cert_file)
#      reg_chan = GeniClient(registry, key_file, cert_file)
   return

#
# Get file names for various credentials and specs
#
# Establishes limiting conventions
#   - conflates MAs and SAs
#   - assumes a single user per working directory
#   - assumes last token in slice name is unique
#
# Bootstraps credentials (not done yet)
#

def get_leaf(name):
   parts = name.split(".")
   return parts[-1]

def get_user_cred_fn():
   file = os.path.join(sfi_dir, os.environ["USER"] + ".cred")
   if (os.path.isfile(file)):
      return file
   else:
      print "bootstrap user credential here"

def get_auth_cred_fn():
   file = os.path.join(sfi_dir, "auth.cred")
   if (os.path.isfile(file)):
      return file
   else:
      print "bootstrap authority credential here"

def get_slice_cred_fn(name):
   file = os.path.join(sfi_dir, "slice_" + get_leaf(name) + ".cred")
   if (os.path.isfile(file)):
      return file
   else:
      print "bootstrap slice credential here"

def get_rspec_fn(rspec):
   if (os.path.isabs(rspec)):
      file = rspec
   else:
      file = os.path.join(sfi_dir, rspec)
   if (os.path.isfile(file)):
      return file
   else:
      print "No such rspec file"
      sys.exit(1)

def get_record_fn(record):
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
   global sm_chan
   global reg_chan

   # Generate command line parser
   parser = OptionParser(usage="sfi [options] command [command_options] [command_args]",
        description="Commands: list,show,remove,add,update,nodes,slices,resources,create,delete,start,stop,reset")
   parser.add_option("-r", "--registry", dest="registry",
        help="root registry", metavar="URL", default=None)
   parser.add_option("-s", "--slicemgr", dest="sm",
        help="slice manager", metavar="URL", default=None)
   parser.add_option("-d", "--dir", dest="dir",
        help="working directory", metavar="PATH", default = sfi_dir)
   parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose", default=False,
        help="verbose mode")
   parser.disable_interspersed_args()
   (options, args) = parser.parse_args()
   command = args[0]
   (cmd_opts, cmd_args) = create_cmd_parser(command).parse_args(args[1:])
   if options.verbose :
      print options.registry,options.sm,options.dir,options.verbose
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
#   todo: make sure args exist
#
# First, the Registry-related commands
#

# list entires in named authority registry
def list(opts, args):
   global reg_chan
   cred_file = get_user_cred_fn() 
   with open(cred_file) as f:
      credential = f.read()
   print "list:", opts.type, args[0], reg_chan, credential
#   result = reg_chan.list(credential, args[0])
#   ...filter output based on opts.type...
   return

# show named registry record
def show(opts, args):
# pretty print or return record xml?
   global reg_chan
   cred_file = get_user_cred_fn() 
   with open(cred_file) as f:
      credential = f.read()
   print "show:", opts.type, args[0], reg_chan, credential
#   result = reg_chan.resolve(credential, args[0])
#   ...filter output based on opts.type...
   return

# removed named registry record
def remove(opts, args):
   global reg_chan
   cred_file = get_auth_cred_fn() 
   with open(cred_file) as f:
      credential = f.read()
   print "remove:", opts.type, args[0], reg_chan, credential
#   ...first retrieve named record...
#   results = reg_chan.resolve(credential, args[0])
#   ...filter desired record from result using opts.type
#   ...use that record to call remove...
#   result = reg_chan.remove(credential, record)
   return

# add named registry record
def add(opts, args):
   global reg_chan
   cred_file = get_auth_cred_fn() 
   with open(cred_file) as f:
      credential = f.read()
   rec_file = get_record_fn(args[1])
   with open(rec_file) as g:
      record = g.read()
   print "add:", record, reg_chan, credential
#   result = reg_chan.register(credential, record)
   return

# update named registry entry
def update(opts, args):
   global reg_chan
   cred_file = get_auth_cred_fn() 
   with open(cred_file) as f:
      credential = f.read()
   rec_file = get_record_fn(args[1])
   with open(rec_file) as g:
      record = g.read()
   print "update:", record, reg_chan, credential
#   result = reg_chan.update(credential, record)
   return

#
# Second, the Slice-related commands
#

# list available nodes
def nodes(opts, args):
   global sm_chan
   cred_file = get_user_cred_fn() 
   with open(cred_file) as f:
      credential = f.read()
   if (args[0] is None):
      context = "root"
   else:
      context = args[0]
   print "nodes:", opts.format, context, sm_chan, credential
#   result = sm_chan.list_nodes(credential, context)
#   ...format output based on opts.format...
   return

# list instantiated slices
def slices(opts, args):
   global sm_chan
   cred_file = get_user_cred_fn() 
   with open(cred_file) as f:
      credential = f.read()
   print "slices:", sm_chan, credential
#   result = sm_chan.list_slices(credential)
   return

# show rspec for named slice
def resources(opts, args):
   global sm_chan
   cred_file = get_slice_cred_fn(args[0]) 
   with open(cred_file) as f:
      credential = f.read()
   print "resources:", opts.format, args[0], sm_chan, credential
#   result = sm_chan.get_resources(credential, args[0])
#   ...format output based on opts.format...
   return

# created named slice with given rspec
def create(opts, args):
   global sm_chan
   cred_file = get_slice_cred_fn(args[0]) 
   with open(cred_file) as f:
      credential = f.read()
   rspec_file = get_rspec_fn(args[1])
   with open(rspec_file) as g:
      rspec = g.read()
   print "create:", args[0], rspec, sm_chan, credential
#   result = sm_chan.instantiate(credential, rspec)
   return

# delete named slice
def delete(opts, args):
   global sm_chan
   cred_file = get_slice_cred_fn(args[0]) 
   with open(cred_file) as f:
      credential = f.read()
   print "delete:", args[0], sm_chan, credential
#   result = sm_chan.delete_slice(credential)
   return

# start named slice
def start(opts, args):
   global sm_chan
   cred_file = get_slice_cred_fn(args[0]) 
   with open(cred_file) as f:
      credential = f.read()
   print "start:", args[0], sm_chan, credential
#   result = sm_chan.start_slice(credential)
   return

# stop named slice
def stop(opts, args):
   global sm_chan
   cred_file = get_slice_cred_fn(args[0]) 
   with open(cred_file) as f:
      credential = f.read()
   print "stop:", args[0], sm_chan, credential
#   result = sm_chan.stop_slice(credential)
   return

# reset named slice
def reset(opts, args):
   global sm_chan
   cred_file = get_slice_cred_fn(args[0]) 
   with open(cred_file) as f:
      credential = f.read()
   print "reset:", args[0], sm_chan, credential
#   result = sm_chan.reset_slice(credential)
   return


if __name__=="__main__":
   main()
