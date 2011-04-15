<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet 
version="1.0"  
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
xmlns:fn="http://www.w3.org/2005/02/xpath-functions" 
>
<xsl:output method="html" />

<!-- to locate the out message -->
<xsl:key name="messages" match="wsdl:message" use="@name"/>

<xsl:template match="wsdl:definitions">
<html>
<head> <title> <xsl:value-of select="./@name" /> </title> </head>
<body>
<table border='1'><tr><th>method</th><th>in</th><th>out</th></tr>
<xsl:apply-templates mode="messages" />
</table>
</body>
</html>
</xsl:template>

<xsl:template match="wsdl:message" mode="messages">
<xsl:variable name="methodname" select="substring-before(@name,'_in')" />
<xsl:variable name="outmessage" select="concat($methodname,'_out')" />
<xsl:if test="contains(@name,'_in')">
<tr>
<td>
<xsl:value-of select="$methodname" />
</td>
<td>
<xsl:for-each select="wsdl:part">
<xsl:value-of select="@name" />
(<xsl:value-of select="@type" />)
<xsl:text> </xsl:text>
</xsl:for-each>
</td>
<td> 
<xsl:value-of select="key('messages',$outmessage)/wsdl:part/@type" />

</td>
</tr>
</xsl:if>
</xsl:template>

</xsl:stylesheet>

