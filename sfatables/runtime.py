#!/usr/bin/python

import sys
import os
import pdb
import libxml2

from optparse import OptionParser
from sfatables import commands
from sfatables.globals import *
from sfatables.commands.List import *
from sfatables.xmlrule import *

class SFATablesRules:
    def __init__(self, chain_name):
        self.active_context = None
        self.contexts = None # placeholder for rspec_manger
        self.sorted_rule_list = []
        chain_dir_path = os.path.join(sfatables_config,chain_name)
        rule_list = List().get_rule_list(chain_dir_path)
        for rule_number in rule_list:
            self.sorted_rule_list = self.sorted_rule_list + [XMLRule(chain_name, rule_number)]
        return


    def set_context(self, request_context):
        self.active_context = request_context
        return

    def apply(self, rspec):
        doc = libxml2.parseDoc(rspec)
        intermediate_rspec = doc

        for rule in self.sorted_rule_list:
            intermediate_rspec  = rule.apply_interpreted(intermediate_rspec)
            if (rule.terminal):
                break

        final_rspec = XMLRule().wrap_up(intermediate_rspec) 
        return final_rspec

def main():
    incoming = SFATablesRules('INCOMING')

    outgoing = SFATablesRules('OUTGOING')
    print "%d rules loaded for INCOMING chain"%len(incoming.sorted_rule_list)
    print incoming.sorted_rule_list[0].processors

    print "%d rules loaded for OUTGOING chain"%len(outgoing.sorted_rule_list)
    print outgoing.sorted_rule_list[0].processors

    rspec = open(sys.argv[1]).read()
    newrspec = incoming.apply(rspec)
    print newrspec
    return

if __name__=="__main__":
    main()
