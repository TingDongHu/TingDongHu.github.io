<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html lang="zh-cn">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title><xsl:value-of select="/rss/channel/title"/> · RSS</title>
        <style>
          body{max-width:760px;margin:2.5rem auto;padding:0 1rem;
            font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
            color:#222;line-height:1.6;background:#fafafa}
          .banner{background:#f4a261;color:#fff;padding:.6rem 1rem;border-radius:8px;
            font-size:.9rem;margin-bottom:1.5rem}
          h1{font-size:1.6rem;margin:.2rem 0}
          .desc{color:#666;margin-bottom:1.5rem}
          ul{list-style:none;padding:0}
          li{padding:1rem;background:#fff;border:1px solid #eee;border-radius:8px;margin-bottom:.8rem}
          li a{font-size:1.1rem;font-weight:600;color:#1d6fb8;text-decoration:none}
          li a:hover{text-decoration:underline}
          .date{display:block;color:#999;font-size:.85rem;margin-top:.3rem}
        </style>
      </head>
      <body>
        <div class="banner">📡 这是 RSS 订阅源。复制本页网址到 Feedly / Inoreader 等阅读器即可订阅。</div>
        <h1><xsl:value-of select="/rss/channel/title"/></h1>
        <p class="desc"><xsl:value-of select="/rss/channel/description"/></p>
        <ul>
          <xsl:for-each select="/rss/channel/item">
            <li>
              <a href="{link}"><xsl:value-of select="title"/></a>
              <span class="date"><xsl:value-of select="pubDate"/></span>
            </li>
          </xsl:for-each>
        </ul>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
