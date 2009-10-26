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

    <xsl:variable name="whitelist_suffix" select="//rspec//target-context/argument[name='whitelist']/value"/>
    <xsl:variable name="blacklist_suffix" select="//rspec//target-context/argument[name='blacklist']/value"/>

    <!-- Drop nodes that are not in the whitelist. This is the legacy version that works on the current
    rspec. The current rspec refers to dns names, not sfa names for nodes.-->
    <xsl:template match="NodeSpec">
            <xsl:choose>
                <xsl:when test="ends-with(@name,$whitelist_suffix) and not($blacklist_suffix and ends-with(@name,$blacklist_suffix))">
                    <xsl:copy-of select="."/>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
