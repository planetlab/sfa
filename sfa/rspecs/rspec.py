#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from datetime import datetime, timedelta
from sfa.util.xrn import *
from sfa.util.plxrn import hostname_to_urn
from sfa.util.enumeration import Enum
from sfa.util.faults import SfaNotImplemented, InvalidRSpec, InvalidRSpecElement


class XpathFilter:
    @staticmethod
    def xpath(filter={}):
        xpath = ""
        if filter:
            filter_list = []
            for (key, value) in filter.items():
                if key == 'text':
                    key = 'text()'
                else:
                    key = '@'+key
                if isinstance(value, str):
                    filter_list.append('%s="%s"' % (key, value))
                elif isinstance(value, list):
                    filter_list.append('contains("%s", %s)' % (' '.join(map(str, value)), key))
            if filter_list:
                xpath = ' and '.join(filter_list)
                xpath = '[' + xpath + ']'
        return xpath

# recognized top level rspec elements 
RSpecElements = Enum('NETWORK', 'NODE', 'SLIVER', 'INTERFACE', 'LINK', 'VLINK')

class RSpecElement:
    def __init__(self, element_type, name, path):
        if not element_type in RSpecElements:
            raise InvalidRSpecElement(element_type)
        self.type = element_type
        self.name = name
        self.path = path     

class RSpec:
    header = '<?xml version="1.0"?>\n'
    template = """<RSpec></RSpec>"""
    xml = None
    type = None
    version = None
    namespaces = None
    user_options = {}
 
    def __init__(self, rspec="", namespaces={}, type=None, user_options={}):
        self.type = type
        self.user_options = user_options
        self.elements = {}
        if rspec:
            self.parse_rspec(rspec, namespaces)
        else:
            self.create()

    def create(self):
        """
        Create root element
        """
        # eg. 2011-03-23T19:53:28Z 
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        now = datetime.utcnow()
        generated_ts = now.strftime(date_format)
        expires_ts = (now + timedelta(hours=1)).strftime(date_format) 
        self.parse_rspec(self.template, self.namespaces)
        self.xml.set('expires', expires_ts)
        self.xml.set('generated', generated_ts)
    
    def parse_rspec(self, rspec, namespaces={}):
        """
        parse rspec into etree
        """
        parser = etree.XMLParser(remove_blank_text=True)
        try:
            tree = etree.parse(rspec, parser)
        except IOError:
            # 'rspec' file doesnt exist. 'rspec' is proably an xml string
            try:
                tree = etree.parse(StringIO(rspec), parser)
            except Exception, e:
                raise InvalidRSpec(str(e))
        self.xml = tree.getroot()  
        if namespaces:
           self.namespaces = namespaces

    def validate(self, schema):
        """
        Validate against rng schema
        """

        relaxng_doc = etree.parse(schema)
        relaxng = etree.RelaxNG(relaxng_doc)
        if not relaxng(self.xml):
            error = relaxng.error_log.last_error
            message = "%s (line %s)" % (error.message, error.line)
            raise InvalidRSpec(message)
        return True

    def xpath(self, xpath):
        return self.xml.xpath(xpath, namespaces=self.namespaces)

    def register_element_type(self, element_type, element_name, element_path):
        if element_type not in RSpecElements:
            raise InvalidRSpecElement(element_type, extra="no such element type: %s. Must specify a valid RSpecElement" % element_type)
        self.elements[element_type] = RSpecElement(element_type, element_name, element_path)

    def get_element_type(self, element_type):
        if element_type not in self.elements:
            msg = "ElementType %s not registerd for this rspec" % element_type
            raise InvalidRSpecElement(element_type, extra=msg)
        return self.elements[element_type]

    def add_attribute(self, elem, name, value):
        """
        Add attribute to specified etree element    
        """
        opt = etree.SubElement(elem, name)
        opt.text = value

    def add_element(self, name, attrs={}, parent=None, text=""):
        """
        Generic wrapper around etree.SubElement(). Adds an element to 
        specified parent node. Adds element to root node is parent is 
        not specified. 
        """
        if parent == None:
            parent = self.xml
        element = etree.SubElement(parent, name)
        if text:
            element.text = text
        if isinstance(attrs, dict):
            for attr in attrs:
                element.set(attr, attrs[attr])  
        return element

    def remove_attribute(self, elem, name, value):
        """
        Removes an attribute from an element
        """
        if elem is not None:
            opts = elem.iterfind(name)
            if opts is not None:
                for opt in opts:
                    if opt.text == value:
                        elem.remove(opt)

    def remove_element(self, element_name, root_node = None):
        """
        Removes all occurences of an element from the tree. Start at 
        specified root_node if specified, otherwise start at tree's root.   
        """
        if not root_node:
            root_node = self.xml

        if not element_name.startswith('//'):
            element_name = '//' + element_name

        elements = root_node.xpath('%s ' % element_name, namespaces=self.namespaces)
        for element in elements:
            parent = element.getparent()
            parent.remove(element)

    def attributes_list(self, elem):
        # convert a list of attribute tags into list of tuples
        # (tagnme, text_value)
        opts = []
        if elem is not None:
            for e in elem:
                opts.append((e.tag, str(e.text).strip()))
        return opts

    def get_element_attributes(self, elem=None, depth=0):
        if elem == None:
            elem = self.root_node
        attrs = dict(elem.attrib)
        attrs['text'] = str(elem.text).strip()
        if isinstance(depth, int) and depth > 0:
            for child_elem in list(elem):
                key = str(child_elem.tag)
                if key not in attrs:
                    attrs[key] = [self.get_element_attributes(child_elem, depth-1)]
                else:
                    attrs[key].append(self.get_element_attributes(child_elem, depth-1))
        else:
            attrs['child_nodes'] = list(elem)
        return attrs

    def find(self, element_type, filter={}, depth=0):
        elements = [self.get_element_attributes(element, depth=depth) for element in \
                    self.find_elements(element_type, filter)]
        return elements

    def find_elements(self, element_type, filter={}):
        """
        search for a registered element
        """
        if element_type not in self.elements:
            msg = "Unable to search for element %s in rspec, expath expression not found." % \
                   element_type
            raise InvalidRSpecElement(element_type, extra=msg)
        rspec_element = self.get_element_type(element_type)
        xpath = rspec_element.path + XpathFilter.xpath(filter)
        return self.xpath(xpath)

    def merge(self, in_rspec):
        pass

    def cleanup(self):
        """
        Optional method which inheriting classes can choose to implent. 
        """
        pass 

    def _process_slivers(self, slivers):
        """
        Creates a dict of sliver details for each sliver host
        
        @param slivers a single hostname, list of hostanmes or list of dicts keys on hostname,
        Returns a list of dicts 
        """
        if not isinstance(slivers, list):
            slivers = [slivers]
        dicts = []
        for sliver in slivers:
            if isinstance(sliver, dict):
                dicts.append(sliver)
            elif isinstance(sliver, basestring):
                dicts.append({'hostname': sliver}) 
        return dicts

    def __str__(self):
        return self.toxml()

    def toxml(self, cleanup=False):
        if cleanup:
            self.cleanup()
        return self.header + etree.tostring(self.xml, pretty_print=True)  
        
    def save(self, filename):
        f = open(filename, 'w')
        f.write(self.toxml())
        f.close()
 
if __name__ == '__main__':
    rspec = RSpec('/tmp/resources.rspec')
    print rspec
    #rspec.register_element_type(RSpecElements.NETWORK, 'network', '//network')
    #rspec.register_element_type(RSpecElements.NODE, 'node', '//node')
    #print rspec.find(RSpecElements.NODE)[0]
    #print rspec.find(RSpecElements.NODE, depth=1)[0]

