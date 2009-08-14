<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="//rspec-match">
        <xsl:variable name="result">
            <xsl:for-each select="//rspec-match/context-input//user">
                <xsl:variable name="context-hrn" select="hrn"/>
                <xsl:for-each select="//rspec-match/rule-input//user">
                    <xsl:choose>
                    <xsl:when test="starts-with($context-hrn, hrn)">
                        True
                    </xsl:when>
                    <xsl:otherwise>
                        False
                    </xsl:otherwise>
                </xsl:choose>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:variable>
        <xsl:value-of select="$result"/>
    </xsl:template>
</xsl:stylesheet>
