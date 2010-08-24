<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <!-- Magic sauce copied from a manual. This fragment basically
    copies everything except for stuff that explicitly matches with
    the templates defined below. In the case of such a match, the
    matched node is treated differently.-->
  <xsl:template match="@* | node()">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>
  <!-- End of magic sauce -->

  <!-- Read in the value of the argument. -->
  <xsl:variable name="max-link-kbps" select="//RSpec//target-context/argument[name='max-link-kbps']/value"/>

  <!-- Modify LinkSpecs for which kbps > max-link-kbps -->
  <xsl:template match="vlink/kbps">
    <xsl:choose>
      <xsl:when test=". &gt; $max-link-kbps">
	<kbps><xsl:value-of select="$max-link-kbps"/></kbps>
      </xsl:when>
      <xsl:otherwise>
	<xsl:copy-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
      
  <!-- Fill in missing kbps values --> 
  <xsl:template match="vlink[not(kbps)]">
    <xsl:copy>
      <xsl:copy-of select="@* | *"/>
      <kbps><xsl:value-of select="$max-link-kbps"/></kbps>
    </xsl:copy>
  </xsl:template>
  
  <xsl:template match="sfatables-input"/>
</xsl:stylesheet>

