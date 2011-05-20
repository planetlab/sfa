#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from sfa.rspecs.rspec import RSpec 
from sfa.util.xrn import *
from sfa.util.plxrn import hostname_to_urn
from sfa.util.config import Config 
from sfa.rspecs.rspec_version import RSpecVersion 

_version = {'type':  'ProtoGENI',
            'version': '2',
            'schema': 'http://www.protogeni.net/resources/rspec/2/ad.xsd',
            'namespace': 'http://www.protogeni.net/resources/rspec/2',
            'extensions':  [
                'http://www.protogeni.net/resources/rspec/ext/gre-tunnel/1',
                'http://www.protogeni.net/resources/rspec/ext/other-ext/3'
            ]
}
pg_rspec_version = RSpecVersion(_version)

class PGRSpec(RSpec):
    xml = None
    header = '<?xml version="1.0"?>\n'
    template = """<rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.protogeni.net/resources/rspec/2" xsi:schemaLocation="http://www.protogeni.net/resources/rspec/2 http://www.protogeni.net/resources/rspec/2/ad.xsd"></rspec>"""
    version = pg_rspec_version
    namespaces = {'rspecv2': version['namespace']}

    def get_network(self):
        network = None 
        nodes = self.xml.xpath('//rspecv2:node[@component_manager_uuid][1]', namespaces=self.namespaces)
        if nodes:
            network  = nodes[0].get('component_manager_uuid')
        return network

    def get_networks(self):
        networks = self.xml.xpath('//rspecv2:node[@component_manager_uuid]/@component_manager_uuid', namespaces=self.namespaces)
        return set(networks)

    def get_node_elements(self):
        nodes = self.xml.xpath('//rspecv2:node', namespaces=self.namespaces)
        return nodes

    def get_nodes(self, network=None):
        return self.xml.xpath('//rspecv2:node[@component_name]/@component_name', namespaces=self.namespaces) 

    def get_nodes_with_slivers(self, network=None):
        if network:
            return self.xml.xpath('//rspecv2:node[@component_manager_id="%s"][sliver_type]/@component_name' % network, namespaces=self.namespaces)
        else:
            return self.xml.xpath('//rspecv2:node[rspecv2:sliver_type]/@component_name', namespaces=self.namespaces)

    def get_nodes_without_slivers(self, network=None):
        pass

    def add_nodes(self, nodes, check_for_dupes=False):
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            urn = ""
            if check_for_dupes and \
              self.xml.xpath('//rspecv2:node[@component_uuid="%s"]' % urn, namespaces=self.namespaces):
                # node already exists
                continue
                
            node_tag = etree.SubElement(self.xml, 'node')
            if 'network_urn' in node:
                node_tag.set('component_manager_id', node['network_urn'])
            if 'urn' in node:
                node_tag.set('component_id', node['urn'])
            if 'hostname' in node:
                node_tag.set('component_name', node['hostname'])
            node_type_tag = etree.SubElement(node_tag, 'node_type', type_name='pcvm', type_slots='100')
            available_tag = etree.SubElement(node_tag, 'available').text = 'true'
            exclusive_tag = etree.SubElement(node_tag, 'exclusive').text = 'false'
            location_tag = etree.SubElement(node_tag, 'location', location="US")
            if 'site' in node:
                if 'longitude' in node['site']:
                    location_tag.set('longitude', str(node['site']['longitude']))
                if 'latitude' in node['site']:
                    location_tag.set('latitude', str(node['site']['latitude']))
            #if 'interfaces' in node:
            

    def add_slivers(self, slivers, check_for_dupes=False): 
        if not isinstance(slivers, list):
            slivers = [slivers]

        nodes_with_slivers = self.get_nodes_with_slivers()
        for sliver in slivers:
            hostname = sliver['hostname']
            if hostname in nodes_with_slivers:
                continue
            nodes = self.xml.xpath('//rspecv2:node[@component_name="%s"] | //node[@component_name="%s"]' % (hostname, hostname), namespaces=self.namespaces)
            if nodes:
                node = nodes[0]
                node.set('client_id', hostname)
                etree.SubElement(node, 'sliver_type', name='planetlab-vnode')

    def add_interfaces(self, interfaces, check_for_dupes=False):
        pass

    def add_links(self, links, check_for_dupes=False):
        pass


    def merge(self, in_rspec):
        """
        Merge contents for specified rspec with current rspec
        """
        
        # just copy over all the child elements under the root element
        tree = etree.parse(StringIO(in_rspec))
        root = tree.getroot()
        for child in root.getchildren():
            self.xml.append(child)
                  
    

if __name__ == '__main__':
    rspec = PGRSpec()
    rspec.add_nodes([1])
    print rspec
