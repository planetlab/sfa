import os, time
from sfatables.command import Command

import sfatables.globals

class Add(Command):
    options = [('-A','--add')]
    help = 'Add a rule to a chain'
    matches = True
    targets = True

    def __init__(self):
        return

    def call(self, command_options, match_options, target_options):
        filename = match_dir + "/"+match_options.name+".xml"
        xmldoc = libxml2.parseFile(filename)
    
        p = self.xmldoc.xpathNewContext()

        context = p.xpathEval("//rule/argument[name='user-hrn']")
        pdb.set_trace()



        return True

