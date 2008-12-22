#! /usr/bin/env python

# sfi -- slice-based facility interface

import sys
import os
from cert import Keypair, Certificate
from optparse import OptionParser

def create_cmd_parser(command):
   cmdargs = {"list": "name",
              "show": "name",
              "delete": "name",
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
      print "Commands:list,show,delete,add,update,nodes,slices,resources,create,delete,start,stop,reset"
      sys.exit(2)

   parser = OptionParser(usage="sfi [sfi_options] %s [options] %s" \
      % (command, cmdargs[command]))
   if command in ("nodes", "resources"):
      parser.add_option("-f", "--format", dest="format",type="choice",
           help="output format (dns|ip|hrn|rspec)",default="rspec",
           choices=("dns","ip","hrn","rspec"))
   elif command in ("list", "show", "delete"):
      parser.add_option("-t", "--type", dest="type",type="choice",
           help="type filter (user|slice|sa|ma|node|aggregate)", 
           choices=("user","slice","sa","ma","node","aggregate"))
   return parser

def main():
   parser = OptionParser(usage="sfi [options] command [command_options] [command_args]",
        description="Commands: list,show,delete,add,update,nodes,slices,resources,create,delete,start,stop,reset")
   parser.add_option("-r", "--registry", dest="registry",
        help="root registry", metavar="URL")
   parser.add_option("-s", "--slicemgr", dest="sm",
        help="slice manager", metavar="URL")
   parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose", default=False,
        help="verbose mode")
   parser.disable_interspersed_args()
   (options, args) = parser.parse_args()
   command = args[0]
   (cmd_opts, cmd_args) = create_cmd_parser(command).parse_args(args[1:])
   if options.verbose :
      print options.registry,options.sm,options.verbose
      print command
      if command in ("nodes", "resources"):
         print cmd_opts.format
      elif command in ("list","show","delete"):
         print cmd_opts.type
      print cmd_args
   return

if __name__=="__main__":
   main()
