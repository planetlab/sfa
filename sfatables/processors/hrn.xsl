<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:variable name="context-hrn" select="hrn"/>
    <xsl:template match="user">
                    <xsl:choose>
                    <xsl:when test="starts-with($context-hrn, hrn)">
                        True <!--Match -->
                    </xsl:when>
                    <xsl:otherwise>
                        False <!-- No match -->
                    </xsl:otherwise>
                </xsl:choose>
        <xsl:value-of select="$result"/>
    </xsl:template>

</xsl:stylesheet>
