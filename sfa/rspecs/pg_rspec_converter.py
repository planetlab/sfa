#!/usr/bin/python 
from lxml import etree
from StringIO import StringIO
from sfa.util.xrn import *
from sfa.rspecs.pg_rspec import PGRSpec 
from sfa.rspecs.sfa_rspec import SfaRSpec

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
    def to_sfa_rspec(rspec):
        if isinstance(rspec, PGRSpec):
            pg_rspec = rspec
        else:        
            pg_rspec = PGRSpec(rspec=rspec)
        sfa_rspec = SfaRSpec()

        # get network
        network_urn = pg_rspec.get_network()
        network,  _ = urn_to_hrn(network_urn)
        network_element = sfa_rspec.add_element('network', {'name': network, 'id': network})
        
        # get nodes
        pg_nodes_elements = pg_rspec.get_node_elements()
        i = 1
        for pg_node_element in pg_nodes_elements:
            urn = pg_node_element.get('component_uuid')
            hostname = Xrn.urn_split(urn)[-1]
            node_element = sfa_rspec.add_element('node', {'id': 'n'+str(i)}, parent=network_element)
            hostname_element = sfa_rspec.add_element('hostname', parent=node_element, text=hostname) 
            urn_element = sfa_rspec.add_element('urn', parent=node_element, text=urn)

            # TODO: convert sliver element
            for child in pg_node_element.getchildren():
                node_element.append(transform(child).getroot())
            i = i+1
 
        return sfa_rspec.toxml()
         
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:        
        print PGRSpecConverter.to_sfa_rspec(sys.argv[1])  
