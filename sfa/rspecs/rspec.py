#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from datetime import datetime, timedelta
from sfa.util.xrn import *
from sfa.util.plxrn import hostname_to_urn
from sfa.util.config import Config  
from sfa.util.faults import SfaNotImplemented, InvalidRSpec

class RSpec:
    xml = None
    header = '<?xml version="1.0"?>\n'
    namespaces = {}
    config = Config()
  
    def __init__(self, rspec="", namespaces={}):
        if rspec:
            self.parse_rspec(rspec, namespaces)
        else:
            self.create()

    def create(self, type="advertisement"):
        # eg. 2011-03-23T19:53:28Z 
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        now = datetime.utcnow()
        generated_ts = now.strftime(date_format)
        expires_ts = (now + timedelta(minutes=30)).strftime(date_format) 
        self.xml = etree.Element("rspec", type = type, 
                                 valid_until=expires_ts,   
                                 generated=generated_ts)
    
    def parse_rspec(self, rspec, namespaces={}):
        parser = etree.XMLParser(remove_blank_text=True)
        try:
            tree = etree.parse(rspec, parser)
        except IOError:
            # 'rspec' file doesnt exist. 'rspec' is proably an xml string
            try:
                tree = etree.parse(StringIO(rspec), parser)
            except:
                raise InvalidRSpec('Must specify a xml file or xml string. Received: ' + rspec )

        self.xml = tree.getroot()  
        if namespaces:
           self.namespaces = namespaces

    def get_network(self):
        raise SfaNotImplemented()

    def get_nodes(self, nodes_with_slivers=False):
        raise SfaNotImplemented()
        
    def add_nodes(self, nodes, check_for_dupes=False):
        raise SfaNotImplemented()

    def add_slivers(self, slivers, check_for_dupes=False): 
        raise SfaNotImplemented()
            
    def add_links(self, links, check_for_dupes=False):
        raise SfaNotImplemented()

    def add_attribute(self, elem, name, value):
        opt = etree.SubElement(elem, name)
        opt.text = value

    def remove_attribute(self, elem, name, value):
        if elem is not None:
            opts = elem.iterfind(name)
            if opts is not None:
                for opt in opts:
                    if opt.text == value:
                        elem.remove(opt)

    def __str__(self):
        return self.toxml()

    def toxml(self):
        return self.header + etree.tostring(self.xml, pretty_print=True)  
        
    def save(self, filename):
        f = open(filename, 'w')
        f.write(self.toxml())
        f.close()
 
if __name__ == '__main__':
    rspec = RSpec()
    print rspec
