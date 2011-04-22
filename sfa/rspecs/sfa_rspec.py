#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from sfa.rspecs.rspec import RSpec 
from sfa.util.xrn import *
from sfa.util.plxrn import hostname_to_urn
from sfa.util.config import Config  


class SfaRSpec(RSpec):
    xml = None
    header = '<?xml version="1.0"?>\n'
    namespaces = {}

    ########
    # Parser
    ########
    def get_network_elements(self):
        return self.xml.xpath('//network', self.namespaces)

    def get_networks(self):
        return self.xml.xpath('//network[@name]/@name', self.namespaces)

    def get_node_element(self, hostname, network=None):
        if network:
            names = self.xml.xpath('//network[@name="%s"]//node/hostname' % network)
        else:
            names = self.xml.xpath('//node/hostname')
        for name in names:
            if name.text == hostname:
                return name.getparent()
        return None
 
    def get_node_elements(self):
        return self.xml.xpath('//node', self.namespaces)

    def get_nodes(self, network=None):
        if network == None:
            nodes = self.xml.xpath('//node/hostname/text()', self.namespaces)
        else:
            nodes = self.xml.xpath('//network[@name="%s"]//node/hostname/text()' % network, self.namespaces)
        return nodes

    def get_nodes_with_slivers(self, network = None):
        if network:
            return self.xml.xpath('//network[@name="%s"]//node[sliver]/hostname/text()' % network, self.namespaces)   
        else:
            return self.xml.xpath('//node[sliver]/hostname/text()', self.namespaces)

    def get_nodes_without_slivers(self, network=None): 
        xpath_nodes_without_slivers = '//node[not(sliver)]/hostname/text()'
        xpath_nodes_without_slivers_in_network = '//network[@name="%s"]//node[not(sliver)]/hostname/text()' 
        if network:
            return self.xml.xpath('//network[@name="%s"]//node[not(sliver)]/hostname/text()' % network, self.namespaces)
        else:
            return self.xml.xpath('//node[not(sliver)]/hostname/text()', self.namespaces)      


    def attributes_list(self, elem):
        # convert a list of attribute tags into list of tuples
        # (tagnme, text_value) 
        opts = []
        if elem is not None:
            for e in elem:
                opts.append((e.tag, e.text))
        return opts

    def get_default_sliver_attributes(self, network=None):
        if network:
            defaults = self.xml.xpath("//network[@name='%s']/sliver_defaults" % network, self.namespaces)        
        else:
            defaults = self.xml.xpath("//network/sliver_defaults" % network, self.namespaces)
        return self.attributes_list(defaults)

    def get_sliver_attributes(self, hostname, network=None):
        node = self.get_node_element(hostname, network)
        sliver = node.find("sliver")
        return self.attributes_list(sliver)

    def get_site_nodes(self, siteid, network=None):
        if network:
            nodes = self.xml.xpath('//network[@name="%s"]/site[@id="%s"]/node/hostname/text()' % \
                                    (network, siteid), self.namespaces)
        else:
            nodes = self.xml.xpath('//site[@id="%s"]/node/hostname/text()' % siteid, self.namespaces)
        return nodes
        
    def get_links(self, network=None):
        if network: 
            links = self.xml.xpath('//network[@name="%s"]/link' % network, self.namespaces)
        else:
            links = self.xml.xpath('//link')    
        linklist = []
        for link in links:
            (end1, end2) = link.get("endpoints").split()
            name = link.find("description")
            linklist.append((name.text,
                             self.get_site_nodes(end1, network),
                             self.get_site_nodes(end2, network)))
        return linklist

    def get_link(self, fromnode, tonode, network=None):
        fromsite = fromnode.getparent()
        tosite = tonode.getparent()
        fromid = fromsite.get("id")
        toid = tosite.get("id")
        if network:
            query = "//network[@name='%s']" % network + "/link[@endpoints = '%s %s']"
        else:
            query = "//link[@endpoints = '%s %s']"

        results = self.rspec.xpath(query % (fromid, toid))
        if not results:
            results = self.rspec.xpath(query % (toid, fromid))
        return results

    def query_links(self, fromnode, tonode, network=None):
        return get_link(fromnode, tonode, network)

    def get_vlinks(self, network=None):
        vlinklist = []
        if network: 
            vlinks = self.xml.xpath("//network[@name='%s']//vlink" % network, self.namespaces)
        else:
            vlinks = self.xml.xpath("//vlink", self.namespaces) 
        for vlink in vlinks:
            endpoints = vlink.get("endpoints")
            (end1, end2) = endpoints.split()
            if network: 
                node1 = self.xml.xpath('//network[@name="%s"]//node[@id="%s"]/hostname/text()' % \
                                       (network, end1))[0]
                node2 = self.xml.xpath('//network[@name="%s"]//node[@id="%s"]/hostname/text()' % \
                                       (network, end2))[0]
            else: 
                node1 = self.xml.xpath('//node[@id="%s"]/hostname/text()' % end1)[0]
                node2 = self.xml.xpath('//node[@id="%s"]/hostname/text()' % end2)[0]
            desc = "%s <--> %s" % (node1, node2)
            kbps = vlink.find("kbps")
            vlinklist.append((endpoints, desc, kbps.text))
        return vlinklist

    def get_vlink(self, endponts, network=None):
        if network:
            query = "//network[@name='%s']//vlink[@endpoints = '%s']" % (network, endpoints)
        else:
            query = "//vlink[@endpoints = '%s']" % (network, endpoints)
        results = self.rspec.xpath(query)
        return results
        
    def query_vlinks(self, endpoints, network=None):
        return get_vlink(endpoints,network)

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
