import libxml2
import libxslt
from sfatables.globals import *

class XMLRule:
    
    def apply_processor(self, type, doc, output_xpath_filter=None):
        processor = self.processors[type]

        # XXX TO CLEAN UP
        filepath = os.path.join(sfatables_config, 'processors', processor)
        # XXX

        styledoc = libxml2.parseFile(filepath)
        style = libxslt.parseStylesheetDoc(styledoc)
        result = style.applyStylesheet(doc, None)
        if (output_xpath_filter):
            p = result.xpathNewContext()
            xpath_result = p.xpathEval(output_xpath_filter)
            if (xpath_result == []):
                raise Exception("Could not apply processor %s."%processor)

            stylesheet_result = xpath_result
            p.xpathFreeContext()
        else:
            stylesheet_result = result #style.saveResultToString(result)

        style.freeStylesheet()
        #doc.freeDoc()
        #result.freeDoc()

        return stylesheet_result

    def wrap_up(self, doc):
        filepath = os.path.join(sfatables_config, 'processors', self.final_processor)

        if not os.path.exists(filepath):
            # TODO: final_processor is not there yet
            return doc#rspec

        styledoc = libxml2.parseFile(filepath)
        style = libxslt.parseStylesheetDoc(styledoc)
        #doc = libxml2.parseDoc(rspec)
        result = style.applyStylesheet(doc, None)
        stylesheet_result = result #style.saveResultToString(result)
        style.freeStylesheet()
        #doc.freeDoc()
        #result.freeDoc()

        return stylesheet_result

    def match(self, rspec):
        match_result = self.apply_processor('match',rspec,"//result/@verdict") 
        return (match_result[0].content=='True')

    def target(self, rspec):
        target_result = self.apply_processor('target',rspec,None)
        return target_result

    def apply_interpreted(self, rspec):
        # Interpreted
        #
        # output =
        #    if (match(match_args, rspec)
        #       then target(target_args, rspec)
        #       else rspec

        if (self.match(rspec)):
            return self.target(rspec)
        else:
            return rspec


    def apply_compiled(rspec):
        # Not supported yet
        return None

    def load_xml_extension (self, type, chain, rule_number):
        filename = sfatables_config+"/"+chain+"/"+"sfatables-%d-%s"%(rule_number,type)

        self.xmldoc = libxml2.parseFile(filename)
        p = self.xmldoc.xpathNewContext()

        context = p.xpathEval('//context/@select')
        self.context[type] = context[0].content

        processor = p.xpathEval('//processor/@filename')

        context = p.xpathEval('//attributes/attribute[@terminal="yes"]')
        if (context != []):
            self.terminal = 1
        
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

    def __init__(self, chain=None, rule_number=None):
        self.rule_number = None
        self.chain = None
        self.xmldoc = None
        self.terminal = 0
        self.final_processor = '__sfatables_wrap_up__.xsl'

        self.arguments = {'match':None,'target':None}
        self.processors = {'match':None,'target':None}
        self.context = {'match':None,'target':None}

        if (chain and rule_number):
            self.load_xml_extension('match', chain, rule_number)
            self.load_xml_extension('target',chain, rule_number)
            self.rule_number = rule_number
            self.chain = chain
        return
        
    def free(self):
        self.xmldoc.freeDoc()
