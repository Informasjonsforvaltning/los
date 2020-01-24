<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:s="urn:fdc:difi.no:2019:data:Skos-1"
                xmlns="urn:fdc:difi.no:2019:data:Skos-1"
                exclude-result-prefixes="s"
                version="2.0">

    <xsl:output method="html" version="5.0" encoding="UTF-8" indent="yes" />

    <xsl:variable name="root" select="/*"/>
    <xsl:variable name="config" select="//s:Config[1]"/>
    <xsl:variable name="siteroot" select="if ($config/s:Options[@key = 'site']/s:Option[@key = 'root']) then $config/s:Options[@key = 'site']/s:Option[@key = 'root'] else ''"/>

    <xsl:template match="s:Skos">
        <xsl:apply-templates select="s:Collection"/>
    </xsl:template>

    <xsl:template match="s:Collection">
        <xsl:variable name="collection" select="current()"/>

        <xsl:variable name="skos">
            <xsl:apply-templates select="s:Member"/>
        </xsl:variable>

        <xsl:variable name="washed">
            <xsl:apply-templates select="$skos" mode="wash">
                <xsl:with-param name="collection" select="$skos"/>
            </xsl:apply-templates>
        </xsl:variable>

        <xsl:variable name="schemes" select="$root/s:ConceptScheme[some $path in $washed//s:InScheme/text() satisfies $path = @path]"/>

        <xsl:variable name="complete" select="$washed/s:Concept | $schemes"/>

        <xsl:variable name="result">
            <Skos>
                <xsl:for-each select="distinct-values($complete/@path)">
                    <xsl:sort/>
                    <xsl:variable name="current" select="current()"/>

                    <xsl:copy-of select="$complete[@path = $current][1]"/>
                </xsl:for-each>
            </Skos>
        </xsl:variable>

        <xsl:apply-templates select="$result" mode="html">
            <xsl:with-param name="collection" select="$collection"/>
            <xsl:with-param name="skos" select="$result"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="s:Member | s:Broader">
        <xsl:variable name="path" select="normalize-space()"/>
        <xsl:copy-of select="$root//*[@path = $path]"/>
        <xsl:apply-templates select="$root//*[@path = $path]/s:Broader"/>
    </xsl:template>



    <xsl:template match="node()|@*" mode="wash">
        <xsl:param name="collection"/>

        <xsl:copy>
            <xsl:apply-templates select="node()|@*" mode="wash">
                <xsl:with-param name="collection" select="$collection"/>
            </xsl:apply-templates>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="s:Narrower | s:Broader | s:Related" mode="wash">
        <xsl:param name="collection"/>

        <xsl:variable name="current" select="normalize-space()"/>

        <xsl:if test="count($collection/*[@path = $current])">
            <xsl:copy>
                <xsl:apply-templates select="node()|@*" mode="wash">
                    <xsl:with-param name="collection" select="$collection"/>
                </xsl:apply-templates>
            </xsl:copy>
        </xsl:if>
    </xsl:template>







    <xsl:template match="*" mode="html">
        <xsl:param name="collection"/>
        <xsl:param name="skos"/>

        <xsl:variable name="languages" select="distinct-values(//@*:lang)"/>

        <xsl:for-each select="$languages">
            <xsl:variable name="lang" select="current()"/>

            <xsl:result-document href="../table-{current()}/{$collection/@path}/index.html">
                <html>
                    <head>
                        <!-- Required meta tags -->
                        <meta charset="utf-8"/>
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>

                        <!-- Bootstrap CSS -->
                        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
                              integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
                              crossorigin="anonymous"/>
                        <style>
                            dl { border-bottom: 1px solid #eee; }
                            dd, dt { border-top: 1px solid #eee; padding-top: .5rem; }
                            div.concept { margin-bottom: 15pt; }
                        </style>

                        <title><xsl:value-of select="$collection/s:PrefLabel[@lang = $lang][1]"/> | <xsl:value-of select="$config/s:Name"/></title>
                    </head>
                    <body>
                        <div class="container">
                            <h1><xsl:value-of select="$config/s:Name"/>: <xsl:value-of select="$collection/s:PrefLabel[@lang = $lang][1]"/></h1>

                            <xsl:for-each select="$skos//s:Concept[count(s:Broader) = 0][s:InScheme = 'ontologi/tema']">
                                <xsl:sort select="s:PrefLabel[@lang = $lang][1]"/>
                                <xsl:apply-templates select="current()" mode="html">
                                    <xsl:with-param name="lang" select="$lang"/>
                                    <xsl:with-param name="skos" select="$skos"/>
                                </xsl:apply-templates>
                            </xsl:for-each>
                        </div>
                    </body>
                </html>
            </xsl:result-document>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="s:Concept" mode="html">
        <xsl:param name="skos"/>
        <xsl:param name="lang"/>
        <xsl:param name="level" select="0"/>

        <div class="concept" style="margin-left: {$level * 25}pt;">
            <div><strong><a href="{$siteroot}{@path}.html"><xsl:value-of select="s:PrefLabel[@lang = $lang][1]"/></a></strong><xsl:text> </xsl:text><span class="text-muted">(<xsl:value-of select="$level + 1"/>)</span></div>

            <xsl:if test="s:AltLabel[@lang = $lang] | s:HiddenLabel[@lang = $lang]">
                <div>
                    <em>
                        <xsl:for-each select="s:AltLabel[@lang = $lang] | s:HiddenLabel[@lang = $lang]">
                            <xsl:sort/>

                            <xsl:if test="position() &gt; 1">
                                <xsl:text>, </xsl:text>
                            </xsl:if>

                            <span>
                                <xsl:if test="local-name() = 'HiddenLabel'">
                                    <xsl:attribute name="class">text-muted</xsl:attribute>
                                </xsl:if>
                                <xsl:value-of select="normalize-space()"/>
                            </span>
                        </xsl:for-each>
                    </em>
                </div>
            </xsl:if>

            <xsl:if test="s:Note[@lang = $lang]">
                <div style="margin-top: 5pt;"><xsl:value-of select="s:Note[@lang = $lang][1]"/></div>
            </xsl:if>
        </div>

        <xsl:variable name="narrower" select="s:Narrower/normalize-space()"/>
        <xsl:for-each select="$skos//s:Concept[some $ref in $narrower satisfies @path = $ref]">
            <xsl:sort select="s:PrefLabel[@lang = $lang][1]"/>
            <xsl:apply-templates select="current()" mode="html">
                <xsl:with-param name="lang" select="$lang"/>
                <xsl:with-param name="level" select="$level + 1"/>
                <xsl:with-param name="skos" select="$skos"/>
            </xsl:apply-templates>
        </xsl:for-each>
    </xsl:template>


</xsl:stylesheet>
