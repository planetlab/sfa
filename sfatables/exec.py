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
    sorted_rule_list = None

    def __init__(self, chain_name):
        chain_dir_path = "%s/%s"%(sfatables_config,chain_name)
        rule_list = List().get_rule_list(chain_dir_path)
        for rule_number in rule_list:
            self.sorted_rule_list.append(XMLRule(rule_number))
        return

    def apply(self, rspec):
        intermediate_rspec = rspec
        for rule in self.sorted_rule_list:
            intermediate_rspec  = rule.apply(intermediate_rspec)

        return intermediate_rspec
