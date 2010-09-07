<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- 
    This processor is called at the end, to remove sfatables-specific tags.
-->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="request-context"/>
</xsl:stylesheet>
