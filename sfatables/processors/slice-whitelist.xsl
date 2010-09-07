<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- This is a good example of an sfatables match. It's function is to verify the slice in context against a whitelist -->

<!-- The following lines should precede each match/target. -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:exsl="http://exslt.org/common"
    extension-element-prefixes="exsl"
    version="1.0">

    <!-- Enter your whitelist prefixes here. Since XSLT cannot read from/write to an external archive, we need to embed the whitelist in here -->

    <xsl:variable name="whitelist_data">
        <hrn>plc.princeton.acb</hrn>
        <hrn>plc.princeton.sapanb</hrn>
        <hrn>plc.princeton.codeen</hrn>
    </xsl:variable>

    <!-- Read the whitelist into a variable. Normally, one should be able to refer to $whitelist_data directly, but apparently this is something you need to do because libxml2 does not support xslt 2.0 -->

    <xsl:variable name="whitelist" select="exsl:node-set($whitelist_data)/hrn"/>

    <!-- Read the value of the current slice's hrn -->
    <xsl:variable name="current_slice_hrn" select="//request-context/sfa/slice/hrn"/>

    <!-- Define a function that checks if one of a list of prefixes (lst) matches $current_slice_hrn". It's a stupid idea to call a function a 'template' but whatever...  -->
    <xsl:template name="recurse_list">
        <xsl:param name="lst"/>
        <xsl:choose>
            <xsl:when test="count($lst)!=0">
                <!-- Indexing in xpath has a base=1 -->
                <xsl:variable name="head" select="$lst[1]"/>
                <xsl:choose>
                    <xsl:when test="starts-with($current_slice_hrn,$head)">
                        <result verdict="True"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:call-template name="recurse_list">
                            <xsl:with-param name="lst" select="$lst/following-sibling::*"/>
                        </xsl:call-template>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <result verdict="False"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="/">
        <xsl:call-template name="recurse_list">
            <xsl:with-param name="lst" select="$whitelist"/>
        </xsl:call-template>
    </xsl:template>
</xsl:stylesheet>
