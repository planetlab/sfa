#! /usr/bin/env python

import sys
from sfa.client.sfi_commands import Commands
from sfa.rspecs.rspec_parser import parse_rspec

command = Commands(usage="%prog [options] node1 node2...",
                   description="Add slivers to the RSpec. " +
                   "This command reads in an RSpec and outputs a modified " +
                   "RSpec. Use this to add nodes to your slice.")
command.add_nodefile_option()
command.prep()

if command.opts.infile:
    rspec = parse_rspec(command.opts.infile)
    nodes = []
    if command.opts.nodefile:
        f = open(command.opts.nodefile, "r")
        nodes = f.read().split()
        f.close()

    try:
        rspec.add_slivers(nodes)
    except:
        print >> sys.stderr, "FAILED: %s" % node

    print rspec.toxml()
    

    
