<xsl:template name="impact-wos">
    <script src="{$theme-path}scripts/impact.js" defer="defer">&#160;</script>
    <p id="wos" class="hidden">
        <xsl:attribute name="data-doi">
            <xsl:value-of select="$identifier_doi" />
        </xsl:attribute>
        <a href="to be filled by impact.js">
            <img src="{concat($theme-path,'/images/wos.png')}"
                i18n:attr="alt"
                alt="xmlui.mirage2.itemSummaryView.ImpactSection.WosLogoAlt" />&#x2002;
            <span class="citation-count"></span>&#x000A0;
            <i18n:text>xmlui.mirage2.itemSummaryView.ImpactSection.WosLink</i18n:text>
        </a>
    </p>
</xsl:template>

<xsl:template name="impact-scopus">
    <script src="{$theme-path}scripts/impact.js" defer="defer">&#160;</script>
    <p id="scopus" class="hidden">
        <xsl:attribute name="data-doi">
            <xsl:value-of select="$identifier_doi" />
        </xsl:attribute>
        <a href="to be filled by impact.js">
            <img src="{concat($theme-path,'/images/scopus.png')}"
                i18n:attr="alt"
                alt="xmlui.mirage2.itemSummaryView.ImpactSection.ScopusLogoAlt" />&#x2002;
            <span class="citedby-count"></span>&#x000A0;
            <i18n:text>xmlui.mirage2.itemSummaryView.ImpactSection.ScopusLink</i18n:text>
        </a>
    </p>
</xsl:template>
