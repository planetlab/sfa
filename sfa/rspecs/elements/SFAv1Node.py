#!/usr/bin/python

from sfa.rspecs.elements.node import Node

class SFAv1Node(Node):

    def get_node_elements(self, network=None, hostnames=None):
        if network:
            query = '//network[@name="%s"]//node' % network
        else:
            query = '//node'

        if isinstance(hostnames, str):
            query = query + '/hostname[text() = "%s"]' % hostnames
        elif isinstance(hostnames, list):
            query = query + '/hostname[contains( "%s" , text())]' \
                    %(" ".join(hostnames))
            
        return self.xpath(query)

    def get_nodes(self, network=None, hostnames):
        node_elems = self.get_node_elements(network, hostnames)
        nodes = [self.get_attributes(node_elem, recursive=True) \
                 for node_elem in node_elems]
        return nodes

    def add_nodes(self, nodes, network=None, no_dupes=False):
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            if no_dupes and \
              self.get_node_element(node['hostname']):
                # node already exists
                continue

            network_tag = self.root_node
            if 'network' in node:
                network = node['network']
                network_tags = self.root_node.xpath('//network[@name="%s"]' % network)
                if not network_tags:
                    #network_tag = etree.SubElement(self.root_node, 'network', name=network)
                    network_tag = self.add_element('network', {'name': network}, self.root_node)
                else:
                    network_tag = network_tags[0]

            #node_tag = etree.SubElement(network_tag, 'node')
            node_tag = self.add_element('node', parent=network_tag)
            if 'network' in node:
                node_tag.set('component_manager_id', network)
            if 'urn' in node:
                node_tag.set('component_id', node['urn'])
            if 'site_urn' in node:
                node_tag.set('site_id', node['site_urn'])
            if 'node_id' in node:
                node_tag.set('node_id', 'n'+str(node['node_id']))
            if 'hostname' in node:
                #hostname_tag = etree.SubElement(node_tag, 'hostname').text = node['hostname']
                hostname_tag = self.add_element('hostname', parent=node_tag)
                hostname_tag.text = node['hostname']
            if 'interfaces' in node:
                for interface in node['interfaces']:
                    if 'bwlimit' in interface and interface['bwlimit']:
                        #bwlimit = etree.SubElement(node_tag, 'bw_limit', units='kbps').text = str(interface['bwlimit']/1000)
                        bwlimit_tag = self.add_element('bw_limit', {'units': 'kbps'}, parent=node_tag)
                        bwlimit_tag.text = str(interface['bwlimit']/1000)
            if 'tags' in node:
                for tag in node['tags']:
                   # expose this hard wired list of tags, plus the ones that are marked 'sfa' in their category
                   if tag['tagname'] in ['fcdistro', 'arch'] or 'sfa' in tag['category'].split('/'):
                        #tag_element = etree.SubElement(node_tag, tag['tagname'], value=tag['value'])
                        tag_element = self.add_element(tag['tagname'], parent=node_tag)
                        tag_element.text = tag['value']

            if 'site' in node:
                longitude = str(node['site']['longitude'])
                latitude = str(node['site']['latitude'])
                #location = etree.SubElement(node_tag, 'location', country='unknown', \
                #                            longitude=longitude, latitude=latitude) 
                location_attrs = {'country': 'unknown', 'longitude': longitude, 'latitude': latitude} 
                self.add_element('location', location_attrs, node_tag) 

if __name__ == '__main__':
    import sys
    from lxml import etree
    args = sys.argv[1:]
    filename = args[0]

    root_node = etree.parse(filename)
    network = SFAv1Node(root_node)
    print network.get_nodes()
