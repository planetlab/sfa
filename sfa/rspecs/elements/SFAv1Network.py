#!/usr/bin/python
from sfa.rspecs.elements.network import Network

class SFAv1Network(Network):

    def get_network_elements(self):
        return self.root_node.xpath('//network')        

    def get_networks(self):
        network_elems = self.get_network_elements()
        networks = [self.get_attributes(network_elem) \
                    for network_elem in network_elems]
        return networks

    def add_networks(self, networks):
        if not isinstance(networks, list):
            networks = [networks]
        return self.add_element('network', {'id': network}, self.root_node)



if __name__ == '__main__':
    import sys
    from lxml import etree
    args = sys.argv[1:]
    filename = args[0]

    root_node = etree.parse(filename)
    network = SFAv1Network(root_node)
    print network.get_networks()

    
