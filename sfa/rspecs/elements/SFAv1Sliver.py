#!/usr/bin/python

from sfa.rspecs.elements.sliver import Sliver
from sfa.rspecs.elements.SFAv1Node import SFVv1Node

class SFAv1Sliver(Sliver):

    def get_sliver_elements(self, network=None):
        if network:
            slivers = self.root_node.xpath('//network[@name="%s"]//node/sliver' % network)
        else:
            slivers = self.root_node.xpath('//node/sliver')
        return slivers

    def get_slivers(self, network=None):
        sliver_elems = self.get_sliver_elements(network)
        slivers = [self.get_attributes(sliver_elem, recursive=True) \
                 for sliver_elem in sliver_elems]
        return slivers

    def add_slivers(self, slivers, network=None):
        if not isinstance(slivers, list):
            slivers = [slivers]
        nodes = SfaV1Node(self.root_node) 
        for sliver in slivers:
            if isinstance(sliver, basestring):
                sliver = {'hostname': sliver}
            if 'hostname' in sliver:
                node_elem = nodes.get_node_elements(hostnames=sliver['hostname'])
                if node_elem:
                    node_elem[0]
                sliver_elem = self.add_element('sliver', parent=node_elem)
                if 'tags' in sliver:
                    for tag in sliver['tags']:
                        self.add_element(tag['tagname'], parent=sliver_elem, text=tag['value'])

    def remove_slivers(self, slivers, network=node):
        nodes = SfaV1Node(self.root_node) 
        for sliver in slivers:
            if isinstance(sliver, str):
                hostname = sliver
            else:
                hostname = sliver['hostname']
            node_elem = nodes.get_node_elements(network=network, hostnames=hostname)
            sliver_elem = node_elem.find('sliver')
            if sliver_elem != None:
                node_elem.remove(sliver_elem)    
                         
                
    def get_sliver_defaults(self, network=None):
        if network:
            defaults = self.xml.xpath("//network[@name='%s']/sliver_defaults" % network)     
        else:
            defaults = self.xml.xpath("//network/sliver_defaults" % network)
        return self.attributes_list(defaults)

    def add_default_sliver_attribute(self, name, value, network=None):
        if network:
            defaults = self.xpath("//network[@name='%s']/sliver_defaults" % network)
        else:
            defaults = self.xpath("//sliver_defaults" % network)
        if not defaults:
            network_tag = self.xpath("//network[@name='%s']" % network)
            if isinstance(network_tag, list):
                network_tag = network_tag[0]
            defaults = self.add_element('sliver_defaults', attrs={}, parent=network_tag)
        elif isinstance(defaults, list):
            defaults = defaults[0]
        self.add_attribute(defaults, name, value)

    def add_sliver_attribute(self, hostname, name, value, network=None):
        node = self.get_node_elements(network, hostname)
        sliver = node.find("sliver")
        self.add_attribute(sliver, name, value)
    
    def remove_default_sliver_attribute(self, name, value, network=None):
        if network:
            defaults = self.xpath("//network[@name='%s']/sliver_defaults" % network)
        else:
            defaults = self.xpath("//sliver_defaults" % network)
        self.remove_attribute(defaults, name, value)
    
    def remove_sliver_attribute(self, hostname, name, value, network=None):
        node = self.get_node_elements(network, hostname)
        sliver = node.find("sliver")
        self.remove_attribute(sliver, name, value)    
            
    
if __name__ == '__main__':
    import sys
    from lxml import etree
    args = sys.argv[1:]
    filename = args[0]

    root_node = etree.parse(filename)
    network = SFAv1Node(root_node)
    print network.get_nodes()
