import libxml2

class Xmlextension:
    context = ""
    processor = ""
    operand = "VALUE"
    arguments = []

    def __init__(filename):
        self.xmldoc = libxml2.parseFile(filename)
        # TODO: Check xmldoc against a schema

        p = self.xmldoc.XPathNewContext()

        # <context select="..."/>
        # <rule><argument param="..."/></rule>
        # <processor name="..."/>

        context = p.xpathEval('//context/@select')
        self.context = context[0].value

        processor = p.xpathEval('//processor@name')
        self.context = processor[0].value

        params = p.xpathEval('//rule/argument/@param')
        self.arguments = [node.value for node in params]


        return

