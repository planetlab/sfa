<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:variable name="whitelist_prefix" select="//rule/argument[name='whitelist']/value"/>
        <xsl:variable name="nodes_minus_whitelist" select="//request/nodespec/node"/>
        <xsl:value-of select="$nodes_minus_whitelist"/>
    </xsl:template>
</xsl:stylesheet>
