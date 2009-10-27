<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:variable name="context-hrn" select="//request-context/sfa/user/hrn"/>

    <!-- Magic sauce -->

    <xsl:template match="@* | node()">
            <xsl:apply-templates select="@* | node()"/>
    </xsl:template>

    <xsl:template match="//match-context/argument[name='user-hrn']">
                    <xsl:value-of select="hrn"/>
                    <xsl:choose>
                    <xsl:when test="starts-with($context-hrn, value)">
                        <result verdict="True"/> <!--Match -->
                    </xsl:when>
                    <xsl:otherwise>
                        <result verdict="False"/> <!-- No match -->
                    </xsl:otherwise>
                </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
