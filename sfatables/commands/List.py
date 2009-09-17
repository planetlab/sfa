import os, time
import libxml2
import pdb

from sfatables.globals import *
from sfatables.pretty import Pretty
from sfatables.command import Command

class List(Command):
    options = [('-L','--list')]
    help = 'List a chain'
    key='list_rule'
    matches = False
    targets = False

    def __init__(self):
        return

    def get_info(self, type, xmlextension_path):
        xmldoc = libxml2.parseFile(xmlextension_path)
        p = xmldoc.xpathNewContext()
        
        ext_name_node = p.xpathEval("/%s/@name"%type)
        ext_name = ext_name_node[0].content

        name_nodes = p.xpathEval("//rule/argument[value!='']/name")
        value_nodes = p.xpathEval("//rule/argument[value!='']/value")

        names = [n.content for n in name_nodes]
        values = [v.content for v in value_nodes]

        name_values = zip(names,values)
        name_value_pairs = map(lambda (n,v):n+'='+v, name_values)

        argument_str = ",".join(name_value_pairs)

        p.xpathFreeContext()
        xmldoc.freeDoc()

        return {'name':ext_name, 'arguments':argument_str}

    def get_rule_list(self, chain_dir_path):
        broken_semantics = os.walk(chain_dir_path)
        rule_numbers = {}

        for (root, dirs, files) in broken_semantics:
            for file in files:
                if (file.startswith('sfatables')):
                    (magic,number,type) = file.split('-')
                    rule_numbers[int(number)]=1

        rule_list = rule_numbers.keys()
        rule_list.sort()
        return rule_list

    def call(self, command_options, match_options, target_options):
        if (len(command_options.args) < 1):
            print "Please specify the name of the chain you would like to list, e.g. sfatables -L INCOMING."
            return

        chain = command_options.args[0]
        chain_dir = sfatables_config + "/" + chain

        rule_list = self.get_rule_list(chain_dir)

        pretty = Pretty(['Rule','Match','Arguments','Target','Arguments'])

        for number in rule_list:
            match_file = "sfatables-%d-%s"%(number,'match')
            target_file = "sfatables-%d-%s"%(number,'target')

            match_path = sfatables_config + '/' + chain + '/' + match_file
            target_path = sfatables_config + '/' + chain + '/' + target_file
            
            match_info = self.get_info ('match',match_path)
            target_info = self.get_info ('target',target_path)

            pretty.push_row(["%d"%number,  match_info['name'], match_info['arguments'], target_info['name'], target_info['arguments']])
        
        
        pretty.pprint()

            






