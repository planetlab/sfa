<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- Magic sauce copied from a manual. This fragment basically copies everything except for
    stuff that explicitly matches with the templates defined below. In the case of such a match,
    the matched node is treated differently.-->
    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:variable name="wswitch" select="//RSpec//target-context/argument[name='whitelist-switch']/value"/>
    <xsl:variable name="wtpsrc" select="//RSpec//target-context/argument[name='whitelist-tpsrc']/value"/>
    <xsl:variable name="wtpdst" select="//RSpec//target-context/argument[name='whitelist-tpdst']/value"/>
    <xsl:variable name="wipsrc" select="//RSpec//target-context/argument[name='whitelist-ipsrc']/value"/>
    <xsl:variable name="wipdst" select="//RSpec//target-context/argument[name='whitelist-ipdst']/value"/>

    <!-- Drop nodes that are not in the whitelist -->
    <xsl:template match="//switchEntry">
            <xsl:choose>
                <xsl:when test="(nodeId==$wswitch) and 
                    (interfaceEntry/flowSpaceEntry/tp_src==$wtpsrc) and
                    (interfaceEntry/flowSpaceEntry/tp_dst==$wtpdst)">
                    <xsl:copy-of select="."/>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
