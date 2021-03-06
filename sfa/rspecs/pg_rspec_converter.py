#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from sfa.util.xrn import *
from sfa.rspecs.rspec import RSpec
from sfa.rspecs.version_manager import VersionManager

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
    def to_sfa_rspec(rspec, content_type = None):
        if not isinstance(rspec, RSpec):
            pg_rspec = RSpec(rspec)
        else:
            pg_rspec = rspec
        
        version_manager = VersionManager()
        sfa_version = version_manager._get_version('sfa', '1')    
        sfa_rspec = RSpec(version=sfa_version)

        # get network
        network_urn = pg_rspec.version.get_network()
        network,  _ = urn_to_hrn(network_urn)
        network_element = sfa_rspec.xml.add_element('network', {'name': network, 'id': network})
        
        # get nodes
        pg_nodes_elements = pg_rspec.version.get_node_elements()
        nodes_with_slivers = pg_rspec.version.get_nodes_with_slivers()
        i = 1
        for pg_node_element in pg_nodes_elements:
            attribs = dict(pg_node_element.attrib.items()) 
            attribs['id'] = 'n'+str(i)
            
            node_element = sfa_rspec.xml.add_element('node', attribs, parent=network_element)
            urn = pg_node_element.xpath('@component_id', namespaces=pg_rspec.namespaces)
            if urn:
                urn = urn[0]
                hostname = Xrn.urn_split(urn)[-1]
                hostname_element = sfa_rspec.xml.add_element('hostname', parent=node_element, text=hostname)
                if hostname in nodes_with_slivers:
                    sfa_rspec.xml.add_element('sliver', parent=node_element)
                     
            urn_element = sfa_rspec.xml.add_element('urn', parent=node_element, text=urn)


            # just copy over remaining child elements  
            for child in pg_node_element.getchildren():
                node_element.append(transform(child).getroot())
            i = i+1
 
        return sfa_rspec.toxml()
         
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:        
        print PGRSpecConverter.to_sfa_rspec(sys.argv[1])  
