<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- Metadata -->
    <xsl:output method="html" indent="yes"/>

    <!-- Root Template -->
    <xsl:template match="/">
        <html>
            <head>
                <title>XML Transformation Output</title>
            </head>
            <body>
                <h1>Transformed Data</h1>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <!-- Template for Items -->
    <xsl:template match="item">
        <div>
            <h2><xsl:value-of select="title"/></h2>
            <p><xsl:value-of select="description"/></p>
            <p><b>Price:</b> <xsl:value-of select="price"/></p>
        </div>
    </xsl:template>

    <!-- Default Template for Unmatched Elements -->
    <xsl:template match="*">
        <p>Unmatched Element: <xsl:value-of select="name()"/></p>
    </xsl:template>
</xsl:stylesheet>
