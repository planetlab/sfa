#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from sfa.rspecs.rspec import RSpec 
from sfa.util.xrn import *
from sfa.util.plxrn import hostname_to_urn
from sfa.util.config import Config  


# define some useful xpath queries for this rspec
xpath_nodes = '//node'
xpath_nodes_hostnames = '//node/hostname/text()'
xpath_nodes_with_hostname = '//node[hostname="%s"]/hostname/text()'
xpath_nodes_with_network = '//network[@name="%s"]//node/hostname/text()'
xpath_networks = '//network'
xpath_networks_names = '//network[@name]/@name'
 

class SfaRSpec(RSpec):
    xml = None
    header = '<?xml version="1.0"?>\n'
    namespaces = {}

    ########
    # Parser
    ########
    def get_networks(self):
        network = None 
        return = self.xml.xpath(xpath_network_names, self.namespaces)

    def get_network_elements(self):
        return self.xml.xpath(xpath_networks, self.namespaces)

    def get_node_elements(self):
        return self.xml.xpath(xpath_nodes, self.namespaces)

    def get_nodes(self, network=None, nodes_with_slivers=False):
        if network == None:
            nodes = self.xml.xpath(xpath_nodes_hostnames, self.namespaces)
        else:
            nodes = self.xml.xpath(xpath_nodes_with_network % network, self.namespaces)
        return nodes

    #########
    # Builder
    ########

    def add_nodes(self, nodes, check_for_dupes=False):
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            urn = ""
            if check_for_dupes and \
              self.xml.xpath('//rspecv2:node[@component_uuid="%s"]' % urn, self.namespaces):
                # node already exists
                continue
                
            node_tag = etree.SubElement(self.xml, 'node')
            node_type_tag = etree.SubElement(node_tag, 'node_type', type_name='pcvm', type_slots='100')
            available_tag = etree.SubElement(node_tag, 'available').text = 'true'
            exclusive_tag = etree.SubElement(node_tag, 'exclusive').text = 'false'
            location_tag = etree.SubElement(node_tag, 'location')
            interface_tag = etree.SubElement(node_tag, 'interface')
            

    def add_slivers(self, slivers, check_for_dupes=False): 
        pass

    def add_links(self, links, check_for_dupes=False):
        pass


if __name__ == '__main__':
    rspec = SfaRSpec()
    rspec.add_nodes([1])
    print rspec
