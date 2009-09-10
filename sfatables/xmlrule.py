import libxml2
from sfatables.globals import *

class XMLRule:
    rule_number = None
    chain = None
    xmldoc = None

    arguments = {'match':None,'target':None}
    processors = {'match':None,'target':None}
    context = {'match':None,'target':None}

    def load_xml_extension (self, type, chain, rule_number):
        filename = sfatables_config+"/"+chain+"/"+"sfatables-%d-%s"%(rule_number,type)

        self.xmldoc = libxml2.parseFile(filename)
        p = self.xmldoc.xpathNewContext()

        context = p.xpathEval('//context/@select')
        self.context[type] = context[0].content

        processor = p.xpathEval('//processor/@filename')

        self.processors[type] = processor[0].content
        self.arguments[type] = p.xpathEval('//rule')

        p.xpathFreeContext()


    def wrap_rspec (self, type, rspec):
        argument = self.arguments[type]
        p = rspec.xmldoc.xpathNewContext()
        root_node = p.xpathEval('/RSpec')
        if (not root_node or not root_node):
            raise Exception('An evil aggregate manager sent me a malformed RSpec. Please see the stack trace to identify it.')

        root_node.addChild(arguments[type])
        return rspec

    def __init__(self, chain, rule_number):

        self.load_xml_extension('match', chain, rule_number)
        self.load_xml_extension('target',chain, rule_number)
        self.rule_number = rule_number
        self.chain = chain

        return
        
    def free(self):
        self.xmldoc.freeDoc()
