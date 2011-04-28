#! /usr/bin/env python

import sys
from sfa.client.sfi_commands import Commands
from sfa.rspecs.rspec_parser import parse_rspec 

command = Commands(usage="%prog [options]",
                   description="List all nodes in the RSpec. " + 
                   "Use this to display the list of nodes on which it is " + 
                   "possible to create a slice.")
command.prep()

if command.opts.infile:
    rspec = parse_rspec(command.opts.infile)
    nodes = rspec.get_nodes()
    if command.opts.outfile:
        sys.stdout = open(command.opts.outfile, 'w')
    
    for node in nodes:
        print node



    
