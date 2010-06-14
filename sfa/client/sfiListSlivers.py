#! /usr/bin/env python

import sys
from sfa.util.rspecHelper import RSpec, Commands

command = Commands(usage="%prog [options]",
                   description="List all slivers in the RSpec. " + 
                   "Use this to display the list of nodes belonging to " + 
                   "the slice.")
command.add_show_attributes_option()
command.prep()

nodes = command.rspec.get_sliver_list()
if command.opts.showatt:
    defaults = command.rspec.get_default_sliver_attributes()
    if defaults:
        print "ALL NODES"
        for (name, value) in defaults:
            print "  %s: %s" % (name, value)

for node in nodes:
    print node
    if command.opts.showatt:
        atts = command.rspec.get_sliver_attributes(node)
        for (name, value) in atts:
            print "  %s: %s" % (name, value)

    
