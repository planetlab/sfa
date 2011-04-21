#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from sfa.util.xrn import *
from sfa.rspecs.pg_rspec import PGRSpec 

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

class PGRSpecConverter:

    @staticmethod
    def to_sfa_node(site, node, i=0):
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

    @staticmethod
    def to_sfa_network(pg_rspec, xml): 
        network_urn = pg_rspec.get_network()
        network,  _ = urn_to_hrn(network_urn)
        nodes = pg_rspec.get_nodes()
        network_tag = etree.SubElement(xml, "network")
        network_tag.set("name", network)
        network_tag.set("id", network)
        site_tag = etree.SubElement(network_tag, "Site")
        site_tag.set("id", network)
        name = etree.SubElement(site_tag, "name").text = network
        i = 0
        for node in nodes:
           PGRSpecConverter.to_sfa_node(site_tag, node, i)
        
    @staticmethod
    def to_sfa_rspec(rspec):
        pg_rspec = PGRSpec(rspec=rspec)
        header = '<?xml version="1.0"?>\n'
        xml = etree.Element("RSpec", type="SFA") 
        PGRSpecConverter.to_sfa_network(pg_rspec, xml) 
        return header + etree.tostring(xml, pretty_print=True)

if __name__ == '__main__':
   rspec = 'protogeni.rspec' 
   print PGRSpecConverter.to_sfa_rspec(rspec)  
