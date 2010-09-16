#! /usr/bin/env python

import sys
from sfa.util.rspecHelper import RSpec, Commands

command = Commands(usage="%prog [options] [node1 node2...]",
                   description="Delete sliver attributes from the RSpec. " +
                   "This command reads in an RSpec and outputs a modified " +
                   "RSpec. Use this to remove attributes from nodes " +
                   "in your slice.  If no nodes are specified, the " +
                   "attributes will be removed from ALL nodes.",
                   epilog="NOTE: Only admins can actually set these " +
                   "attributes, with the exception of --delegations")
command.add_nodefile_option()
command.add_attribute_options()
command.prep()

attrs = command.get_attribute_dict()
for name in attrs:
    print >> sys.stderr, name, attrs[name]
    for value in attrs[name]:
        if not command.nodes:
            try:
                command.rspec.remove_default_sliver_attribute(name, value)
            except:
                print >> sys.stderr, "FAILED: on all nodes: %s=%s" % (name, value)
            else:
                for node in command.nodes:
                    try:
                        command.rspec.remove_sliver_attribute(node, name, value)
                    except:
                        print >> sys.stderr, "FAILED: on node %s: %s=%s" % (node, name, value)

print command.rspec
    

    
