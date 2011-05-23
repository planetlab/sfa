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

if not command.opts.nodefile:
    print "Missing node list -- exiting"
    command.parser.print_help()
    sys.exit(1)
    
if command.opts.infile:
    infile=file(command.opts.infile)
else:
    infile=sys.stdin
if command.opts.outfile:
    outfile=file(command.opts.outfile,"w")
else:
    outfile=sys.stdout

rspec = parse_rspec(infile)
nodes = file(command.opts.nodefile).read().split()
try:
    if rspec.version['type'].lower() == 'protogeni':
        rspec.xml.set('type', 'request')
        rspec.remove_element('available')    
    slivers = [{'hostname': node} for node in nodes]
    rspec.add_slivers(slivers)
except:
    print >> sys.stderr, "FAILED: %s" % nodes
    sys.exit(1)
print >>outfile, rspec.toxml()
sys.exit(0)
