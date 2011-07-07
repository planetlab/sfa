#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from sfa.rspecs.rspec import RSpec 
from sfa.util.xrn import *
from sfa.util.plxrn import hostname_to_urn, xrn_to_hostname
from sfa.util.config import Config 
from sfa.rspecs.rspec_version import RSpecVersion 

_ad_version = {'type':  'ProtoGENI',
            'version': '2',
            'schema': 'http://www.protogeni.net/resources/rspec/2/ad.xsd',
            'namespace': 'http://www.protogeni.net/resources/rspec/2',
            'extensions':  [
                'http://www.protogeni.net/resources/rspec/ext/gre-tunnel/1',
                'http://www.protogeni.net/resources/rspec/ext/other-ext/3'
            ]
}

_request_version = {'type':  'ProtoGENI',
            'version': '2',
            'schema': 'http://www.protogeni.net/resources/rspec/2/request.xsd',
            'namespace': 'http://www.protogeni.net/resources/rspec/2',
            'extensions':  [
                'http://www.protogeni.net/resources/rspec/ext/gre-tunnel/1',
                'http://www.protogeni.net/resources/rspec/ext/other-ext/3'
            ]
}
pg_rspec_ad_version = RSpecVersion(_ad_version)
pg_rspec_request_version = RSpecVersion(_request_version)

class PGRSpec(RSpec):
    xml = None
    header = '<?xml version="1.0"?>\n'
    template = '<rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.protogeni.net/resources/rspec/2" xsi:schemaLocation="http://www.protogeni.net/resources/rspec/2 http://www.protogeni.net/resources/rspec/2/%(rspec_type)s.xsd" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" />'

    def __init__(self, rspec="", namespaces={}, type=None):
        if not type:
            type = 'advertisement'
        self.type = type

        if type == 'advertisement':
            self.version = pg_rspec_ad_version
            rspec_type = 'ad'
        else:
            self.version = pg_rspec_request_version
            rspec_type = type
        
        self.template = self.template % {'rspec_type': rspec_type}

        if not namespaces:
            self.namespaces = {'rspecv2': self.version['namespace'],
                               'flack': 'http://www.protogeni.net/resources/rspec/ext/flack/1' }

        else:
            self.namespaces = namespaces 

        if rspec:
            self.parse_rspec(rspec, self.namespaces)
        else: 
            self.create()

    def create(self):
        RSpec.create(self)
        if self.type:
            self.xml.set('type', self.type) 
       
    def get_network(self):
        network = None 
        nodes = self.xml.xpath('//rspecv2:node[@component_manager_uuid][1]', namespaces=self.namespaces)
        if nodes:
            network  = nodes[0].get('component_manager_uuid')
        return network

    def get_networks(self):
        networks = self.xml.xpath('//rspecv2:node[@component_manager_uuid]/@component_manager_uuid', namespaces=self.namespaces)
        return set(networks)

    def get_node_element(self, hostname, network=None):
        nodes = self.xml.xpath('//rspecv2:node[@component_id[contains(., "%s")]] | node[@component_id[contains(., "%s")]]' % (hostname, hostname), namespaces=self.namespaces)
        if isinstance(nodes,list) and nodes:
            return nodes[0]
        else:
            return None

    def get_node_elements(self, network=None):
        nodes = self.xml.xpath('//rspecv2:node | //node', namespaces=self.namespaces)
        return nodes

    def get_nodes(self, network=None):
        xpath = '//rspecv2:node[@component_name]/@component_id | //node[@component_name]/@component_id'
        nodes = self.xml.xpath(xpath, namespaces=self.namespaces)
        nodes = [xrn_to_hostname(node) for node in nodes]
        return nodes 

    def get_nodes_with_slivers(self, network=None):
        if network:
            nodes = self.xml.xpath('//rspecv2:node[@component_manager_id="%s"][sliver_type]/@component_id' % network, namespaces=self.namespaces)
        else:
            nodes = self.xml.xpath('//rspecv2:node[rspecv2:sliver_type]/@component_id', namespaces=self.namespaces)
        nodes = [xrn_to_hostname(node) for node in nodes]
        return nodes

    def get_nodes_without_slivers(self, network=None):
        return []

    def get_sliver_attributes(self, hostname, network=None):
        node = self.get_node_element(hostname, network)
        sliver = node.xpath('//rspecv2:sliver_type', namespaces=self.namespaces)
        if sliver is not None and isinstance(sliver, list):
            sliver = sliver[0]
        return self.attributes_list(sliver)
   
    def get_slice_attributes(self, network=None):
        slice_attributes = []
        nodes_with_slivers = self.get_nodes_with_slivers(network)
        # TODO: default sliver attributes in the PG rspec?
        default_ns_prefix = self.namespaces['rspecv2']
        for node in nodes_with_slivers:
            sliver_attributes = self.get_sliver_attributes(node, network)
            for sliver_attribute in sliver_attributes:
                name=str(sliver_attribute[0]) 
                value=str(sliver_attribute[1])
                # we currently only suppor the <initscript> and <flack> attributes 
                if  'info' in name:
                    attribute = {'name': 'flack_info', 'value': str(sliver_attribute[2]), 'node_id': node}
                    slice_attributes.append(attribute) 
                elif 'initscript' in name: 
                    attribute = {'name': 'initscript', 'value': value, 'node_id': node}
                    slice_attributes.append(attribute) 

        return slice_attributes

    def attributes_list(self, elem):
        opts = []
        if elem is not None:
            for e in elem:
                opts.append((e.tag, e.text, e.attrib))
        return opts

    def get_default_sliver_attributes(self, network=None):
        return []

    def add_default_sliver_attribute(self, name, value, network=None):
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
                
            node_tag = etree.SubElement(self.xml, 'node', exclusive='false')
            if 'network_urn' in node:
                node_tag.set('component_manager_id', node['network_urn'])
            if 'urn' in node:
                node_tag.set('component_id', node['urn'])
            if 'hostname' in node:
                node_tag.set('component_name', node['hostname'])
            # TODO: should replace plab-pc with pc model 
            node_type_tag = etree.SubElement(node_tag, 'hardware_type', name='plab-pc')
            node_type_tag = etree.SubElement(node_tag, 'hardware_type', name='pc')
            available_tag = etree.SubElement(node_tag, 'available', now='true')
            sliver_type_tag = etree.SubElement(node_tag, 'sliver_type', name='plab-vnode')
            # protogeni uses the <sliver_type> tag to identify the types of
            # vms available at the node. 
            # only add location tag if longitude and latitude are not null
            if 'site' in node:
                longitude = node['site'].get('longitude', None)
                latitude = node['site'].get('latitude', None)
                if longitude and latitude:
                    location_tag = etree.SubElement(node_tag, 'location', country="us", \
                                                    longitude=str(longitude), latitude=str(latitude))


    def add_slivers(self, slivers, sliver_urn=None, no_dupes=False): 

        # all nodes hould already be present in the rspec. Remove all 
        # nodes that done have slivers
        from sfa.util.sfalogging import logger
        slivers = self._process_slivers(slivers)
        slivers_dict = {}
        for sliver in slivers:
            slivers_dict[sliver['hostname']] = sliver
        nodes = self.get_node_elements()
        for node in nodes:
            urn = node.get('component_id')
            hostname = xrn_to_hostname(urn)
            if hostname not in slivers_dict:
                parent = node.getparent()
                parent.remove(node)
            else:
                sliver_info = slivers_dict[hostname]
                node.set('client_id', hostname)
                if sliver_urn:
                    node.set('sliver_id', sliver_urn)
                sliver_elem = node.xpath('//rspecv2:sliver_type | //sliver_type', namespaces=self.namespaces)
                if sliver_elem and isinstance(sliver_elem, list):
                    sliver_elem = sliver_elem[0]
                    for tag in sliver_info['tags']:
                        if tag['tagname'] == 'flack_info':
                            e = etree.SubElement(sliver_elem, '{%s}info' % self.namespaces['flack'], attrib=eval(tag['value']))
                              
     
    def add_default_sliver_attribute(self, name, value, network=None):
        pass

    def add_interfaces(self, interfaces, no_dupes=False):
        pass

    def add_links(self, links, no_dupes=False):
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
                  
    def cleanup(self):
        # remove unncecessary elements, attributes
        if self.type in ['request', 'manifest']:
            # remove 'available' element from remaining node elements
            self.remove_element('//rspecv2:available | //available')

if __name__ == '__main__':
    rspec = PGRSpec()
    rspec.add_nodes([1])
    print rspec
