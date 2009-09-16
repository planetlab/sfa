#!/usr/bin/python

import sys
import os
import pdb
import libxml2

from optparse import OptionParser
from sfatables import commands, matches, targets
from sfatables.xmlextension import Xmlextension
from sfatables.globals import *
from sfatables.commands.List import *
from sfatables.xmlrule import *

class SFATablesRules:
    def __init__(self, chain_name):
        self.sorted_rule_list = []
        chain_dir_path = "%s/%s"%(sfatables_config,chain_name)
        rule_list = List().get_rule_list(chain_dir_path)
        for rule_number in rule_list:
            self.sorted_rule_list.append(XMLRule(chain_name, rule_number))
        return


    def apply(self, rspec):
        intermediate_rspec = rspec
        for rule in self.sorted_rule_list:
            intermediate_rspec  = rule.apply_interpreted(intermediate_rspec)
            if (rule.terminal):
                break

        return intermediate_rspec

def main():
    incoming = SFATablesRules('INCOMING')
    outgoing = SFATablesRules('OUTGOING')

    rspec = open(sys.argv[1]).read()


    
    print "%d rules loaded for INCOMING chain\n"%len(incoming.sorted_rule_list)
    print "%d rules loaded for OUTGOING chain\n"%len(outgoing.sorted_rule_list)

    newrspec = incoming.apply(rspec)
    print newrspec
    return

if __name__=="__main__":
    main()
