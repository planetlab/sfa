#! /usr/bin/env python

import sys
from sfa.util.rspecHelper import RSpec, Commands

command = Commands(usage="%prog [options]",
                   description="List all nodes in the RSpec. " + 
                   "Use this to display the list of nodes on which it is " + 
                   "possible to create a slice.")
command.prep()

nodes = command.rspec.get_node_list()
for node in nodes:
    print node


    
