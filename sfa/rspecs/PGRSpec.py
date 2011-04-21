#!/usr/bin/python 
from __future__ import with_statement
from lxml import etree
from xmlbuilder import XMLBuilder
from StringIO import StringIO
from sfa.util.xrn import *

xslt='''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="no"/>

<xsl:template match="/|comment()|processing-instruction()">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

<xsl:template match="*">
    <xsl:element name="{local-name()}">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:element>
</xsl:template>

<xsl:template match="@*">
    <xsl:attribute name="{local-name()}">
      <xsl:value-of select="."/>
    </xsl:attribute>
</xsl:template>
</xsl:stylesheet>
'''

xslt_doc=etree.parse(StringIO(xslt))
transform=etree.XSLT(xslt_doc)

class PGRSpec:
    xml_tree = None
    namespaces = {'rspecv2':'http://www.protogeni.net/resources/rspec/0.2'}
  

    def __init__(self, rspec="", namespaces={}):
        try:
            self.xml_tree = etree.parse(rspec)
            if namespaces:
               self.namespaces = namespaces   
 
        except IOError:
            # 'rspec' file doesnt exist. 'rspec' is proably an xml string
            try: 
                self.xml_tree = etree.parse(StringIO(rspec))
            except:
                raise IOError("Must specify a xml file or xml string. Received: " + rspec )

    def get_network(self):
        network = None 
        root = self.xml_tree.getroot()
        nodes = root.xpath("//rspecv2:node[@component_manager_uuid][1]", self.namespaces)
        if nodes:
            network  = nodes[0].get('component_manager_uuid')
        return network

    def get_nodes(self, nodes_with_slivers=False):
        root = self.xml_tree.getroot()
        nodes = root.xpath("//rspecv2:node", self.namespaces)
        return nodes


    def to_sfa_node(self, site, node, i=0):
        cm_urn = node.get('component_manager_uuid')
        c_name = node.get('component_name')
        c_urn = node.get('component_uuid')
        c_hrn, _ = urn_to_hrn(c_urn)
        node_tag = etree.SubElement(site, "node")
        node_tag.set("component_manager_uuid", cm_urn)
        node_tag.set("component_name", c_name)
        node_tag.set("component_uuid", c_urn)
        hostname_tag = etree.SubElement(node_tag, "hostname").text = c_hrn
        urn_tag = etree.SubElement(node_tag, "urn").text = c_hrn
        for child in node.getchildren():
            node_tag.append(transform(child).getroot())      


    def to_sfa_network(self, xml): 
        network_urn = self.get_network()
        network,  _ = urn_to_hrn(network_urn)
        nodes = self.get_nodes()
        network_tag = etree.SubElement(xml, "network")
        network_tag.set("name", network)
        network_tag.set("id", network)
        site_tag = etree.SubElement(network_tag, "Site")
        site_tag.set("id", network)
        name = etree.SubElement(site_tag, "name").text = network
        i = 0
        for node in nodes:
            self.to_sfa_node(site_tag, node, i)
        
    def to_sfa_rspec(self):
        header = '<?xml version="1.0"?>\n'
        xml = etree.Element("RSpec", type="SFA") 
        self.to_sfa_network(xml) 
        return header + etree.tostring(xml, pretty_print=True)

if __name__ == '__main__':
   rspec = 'protogeni.rspec' 
   PGRSpec = PGRSpec(rspec)
   print PGRSpec.to_sfa_rspec()  
