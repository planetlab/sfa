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

    <xsl:variable name="whitelist_prefix" select="//RSpec//target-context/argument[name='whitelist']/value"/>
    <xsl:variable name="blacklist_prefix" select="//RSpec//target-context/argument[name='blacklist']/value"/>

    <!-- Drop nodes that are not in the whitelist -->
    <xsl:template match="node">
            <xsl:choose>
                <xsl:when test="starts-with(@name,$whitelist_prefix) and not($blacklist_prefix and starts-with(@name,$blacklist_prefix))">
                    <xsl:copy-of select="."/>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
