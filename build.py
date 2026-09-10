#!/usr/bin/env python3
"""Chase Golden Globe — static site builder (v4).
Run `python3 build.py` from the site root. Shared head, nav and footer live
here; each page supplies its title, meta, hero and body. Output is written
next to this file. The world map SVG is read from map.svg.
"""
import os, re

SITE = "https://chasegoldenglobe.com.au"
HERE = os.path.dirname(os.path.abspath(__file__))
MAP = open(os.path.join(HERE, "map.svg"), encoding="utf-8").read()
MAP_MINI = MAP.replace('id="worldMap"', 'id="worldMapMini"').replace('role="img"', 'role="img" aria-hidden="true"')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600'
         '&family=Public+Sans:wght@400;500;600;700&family=Cairo:wght@400;500;600;700'
         '&family=Markazi+Text:wght@500;600;700&display=swap" rel="stylesheet">')

NAV_ITEMS = [("about", "About"), ("capabilities", "Capabilities"), ("industries", "Industries"),
             ("presence", "Presence"), ("contact", "Contact")]

def head(p):
    canon = SITE + ("/" if p["slug"] == "index" else f"/{p['slug']}.html")
    robots = "noindex, follow" if p.get("noindex") else "index, follow"
    og_title = p["title"]
    h = f'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" href="/assets/favicon.ico">
<link rel="apple-touch-icon" href="/assets/icon-192.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#EEEBE4">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Chase Golden Globe">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/style.css">
'''
    if p.get("preload"):
        h += f'<link rel="preload" as="image" href="{p["preload"]}">\n'
    for s in p.get("schema", []):
        h += f'<script type="application/ld+json">{s}</script>\n'
    return h + "</head>\n"

def crumbs(name_key, name):
    return (f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/" data-i18n="crumb.home">Home</a></li>'
            f'<li aria-hidden="true">/</li><li aria-current="page" data-i18n="{name_key}">{name}</li></ol></nav>')

def breadcrumb_schema(name, slug):
    return ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            f'{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},'
            f'{{"@type":"ListItem","position":2,"name":"{name}","item":"{SITE}/{slug}.html"}}]}}')

def nav(active):
    items = ""
    for s, l in NAV_ITEMS:
        cls = ' class="active"' if s == active else ""
        items += f'    <a href="/{s}.html"{cls} data-i18n="nav.{s}">{l}</a>\n'
    return f'''<a class="skip-link" href="#main" data-i18n="skip">Skip to main content</a>
<nav class="site-nav" id="siteNav" aria-label="Primary">
  <a class="nav-logo" href="/" aria-label="Chase Golden Globe — Home">
    <picture><source srcset="/assets/logo.webp" type="image/webp"><img src="/assets/logo.png" alt="" width="46" height="32"></picture>
    <div><div class="nav-logo-text">Chase Golden Globe</div><div class="nav-logo-sub" data-i18n="nav.sub">Est. 2006 · Sydney</div></div>
  </a>
  <button type="button" class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks" data-i18n="nav.menu">Menu</button>
  <div class="nav-links" id="navLinks">
{items}    <div class="lang-switch" role="group" aria-label="Language">
      <button type="button" data-lang="en" lang="en" aria-label="English" aria-pressed="true" class="active">EN</button>
      <button type="button" data-lang="ar" lang="ar" aria-label="العربية" aria-pressed="false">ع</button>
      <button type="button" data-lang="id" lang="id" aria-label="Bahasa Indonesia" aria-pressed="false">ID</button>
    </div>
  </div>
</nav>
'''

def phero(img, crumb_key, crumb_name, eyebrow_key, eyebrow, title_key, title, lede_key, lede, hid):
    return f'''<section class="tight"><div class="wrap">
  <div class="phero" style="background-image:url('{img}');"><div class="phero-in">
    {crumbs(crumb_key, crumb_name)}
    <div class="eyebrow on-dark" data-i18n="{eyebrow_key}">{eyebrow}</div>
    <h1 class="h-page" id="{hid}" data-i18n="{title_key}">{title}</h1>
    <p class="lede on-dark" data-i18n="{lede_key}">{lede}</p>
  </div></div>
</div></section>
'''

def footer(cta=True, minimal=False):
    cta_html = '''    <div class="f-cta">
      <div>
        <div class="eyebrow on-dark" data-i18n="home.cta.eyebrow">Get in Touch</div>
        <h2 data-i18n="home.cta.title">Begin the conversation.</h2>
        <p data-i18n="home.cta.body">For matters of investment, trade or partnership, enquiries are received directly.</p>
      </div>
      <a class="btn btn-brass" href="/contact.html" data-i18n="home.cta.btn">Contact Us</a>
    </div>
''' if cta else ""
    top = '''    <div class="f-top">
      <div>
        <a class="footer-logo" href="/" aria-label="Chase Golden Globe — Home">
          <picture><source srcset="/assets/logo.webp" type="image/webp"><img src="/assets/logo.png" alt="" width="40" height="28"></picture>
          <span>Chase Golden Globe</span>
        </a>
        <p class="f-blurb" data-i18n="footer.blurb">A private investment house, established 2006. Connecting investors to serious projects across international markets.</p>
      </div>
      <div class="f-col"><h4 data-i18n="footer.explore">Explore</h4><a href="/about.html" data-i18n="nav.about">About</a><br><a href="/capabilities.html" data-i18n="nav.capabilities">Capabilities</a><br><a href="/industries.html" data-i18n="nav.industries">Industries</a><br><a href="/presence.html" data-i18n="nav.presence">Presence</a></div>
      <div class="f-col"><h4 data-i18n="footer.connect">Connect</h4><a href="/contact.html" data-i18n="nav.contact">Contact</a><br><a href="mailto:info@chasegoldenglobe.com.au">info@chasegoldenglobe.com.au</a></div>
    </div>
''' if not minimal else ""
    return f'''<footer class="site-footer{" minimal" if minimal else ""}">
  <div class="wrap">
{cta_html}{top}    <div class="f-bot">
      <p data-i18n="footer.disclaimer">Chase Golden Globe Pty Ltd is not itself a licensed financial services provider. Where a service requires a specific licence, it is delivered in partnership with appropriately licensed professionals and firms.</p>
      <div class="r"><span data-i18n="footer.copyright">© 2026 Chase Golden Globe Pty Ltd</span><div><a href="/legal.html" data-i18n="footer.legal">Legal &amp; Privacy</a><a href="/contact.html" data-i18n="nav.contact">Contact</a></div></div>
    </div>
  </div>
</footer>
<script src="/assets/i18n.js" defer></script>
<script src="/script.js" defer></script>
</body>
</html>
'''

# --------------------------------------------------------------------------
CAPS = [
    ("Structured Project &amp; Export Finance", "Financing frameworks for infrastructure, agri-tech and industrial ventures, connecting global capital with projects that matter regionally."),
    ("Capital Structuring &amp; Risk", "Structures and risk mitigation designed to make a project bankable and keep cross-border delivery efficient."),
    ("Impact &amp; Sustainable Investment", "Capital directed at ventures with a measurable economic and social return, not just a financial one."),
    ("Government &amp; Institutional Liaising", "Direct coordination with ministries and regulators, so approvals never become the reason a project stalls."),
    ("Bankability &amp; Project Readiness", "Getting the technical, financial and regulatory elements in order so a project meets investor standards."),
    ("Capital Raising", "Sourcing capital for growth, for unlocking value in an existing asset, or for refinancing what is already in place."),
    ("Mergers &amp; Acquisitions", "Advisory from first conversation through negotiation, financing and integration."),
    ("Private Equity Advisory", "Working alongside firms and their portfolio companies with a focus on value that lasts."),
    ("Joint Ventures &amp; Alliances", "Building the right partnerships and consortiums for the market being entered."),
]
ICONS = [
    '<path d="M3 21h18M5 21V10l7-6 7 6v11M9 21v-6h6v6"/>',
    '<path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/>',
    '<path d="M3 17h1l2-5h12l2 5h1M6 17v2M18 17v2M7 12V7h10v5M9 7V4h6v3"/>',
    '<path d="M4 9V4h16v5M5 9l1 11h12l1-11M9 13h6"/>',
    '<path d="M3 21V10l5 3V10l5 3V10l5 3v8H3z"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.5 6 3.5 9s-1 6.5-3.5 9c-2.5-2.5-3.5-6-3.5-9s1-6.5 3.5-9z"/>',
    '<path d="M4 21V9l8-6 8 6v12M9 21v-6h6v6M6 12h.01M18 12h.01"/>',
    '<path d="M12 3v6l4 2M4 15c0-2 1-3 3-4l1-1M20 15c0-2-1-3-3-4l-1-1M8 21h8M9 17l-1 4M15 17l1 4"/>',
    '<path d="M4 21h16M6 21V11l-2-2 4-4 4 4-2 2v10M14 21v-6l2-2 4 4-2 2v2"/>',
]
SECTORS = [
    ("Agriculture &amp; Food Security", "Technology-driven agriculture, from precision farming to export-ready supply chains."),
    ("Energy", "Solar, hydro and waste-to-energy projects financing the shift to sustainable power."),
    ("Infrastructure", "Transport corridors, freight capacity and logistics hubs that keep regions connected."),
    ("Retail &amp; Hospitality", "Retail networks, hotels and hospitality ventures, from market entry to operating scale."),
    ("Industrial Manufacturing", "Manufacturing and industrial expansion, including textile and apparel supply chains."),
    ("Cross-Border Trade", "Trade and investment connecting Africa, the Middle East and Asia, where the group began."),
    ("Real Estate &amp; Luxury Development", "High-end interior design, luxury real estate and premium renovations, including prestigious and government properties."),
    ("Oil &amp; Gas", "Upstream and midstream assets and transactions, connecting operators with capital across borders."),
    ("Mining &amp; Natural Resources", "Resource projects assessed on structure, counterparties and commercial viability before capital moves."),
]
COUNTRIES = ["Australia", "Indonesia", "Saudi Arabia", "Qatar", "United Arab Emirates", "Algeria", "Egypt",
             "United Kingdom", "Switzerland", "Luxembourg"]

def strip_html():
    return "".join(f'      <a href="/capabilities.html"><span data-i18n="cap.t{i+1}.title">{t}</span> <span aria-hidden="true">→</span></a>\n'
                   for i, (t, _) in enumerate(CAPS))

def cap_cards():
    out = []
    for i, (t, b) in enumerate(CAPS):
        out.append(f'      <div class="card"><div class="n" aria-hidden="true">{i+1:02d}</div><h3 data-i18n="cap.t{i+1}.title">{t}</h3><p data-i18n="cap.t{i+1}.body">{b}</p></div>')
    return "\n".join(out)

def sector_cards():
    out = []
    for i, (t, b) in enumerate(SECTORS):
        out.append(f'      <div class="card"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">{ICONS[i]}</svg><h3 data-i18n="ind.s{i+1}.title">{t}</h3><p data-i18n="ind.s{i+1}.body">{b}</p></div>')
    return "\n".join(out)

def sector_list():
    return "".join(f'          <div data-i18n="ind.s{i+1}.title">{t}</div>\n' for i, (t, _) in enumerate(SECTORS))

def country_buttons():
    out = []
    for c in COUNTRIES:
        hq = ' <span data-i18n="pres.hq">(HQ)</span>' if c == "Australia" else ""
        out.append(f'          <button type="button" data-country="{c}" aria-pressed="false"><span data-i18n="country.{c}">{c}</span>{hq}</button>')
    return "\n".join(out)

# --------------------------------------------------------------------------
PAGES = {}

PAGES["index"] = dict(
    slug="index",
    title="Chase Golden Globe | Private Investment House, Est. 2006",
    desc="Chase Golden Globe connects investors to projects across international markets, from a house that began trading fine furniture between Indonesia and Australia in 2006.",
    preload="/assets/hero-home.jpg",
    schema=['{"@context":"https://schema.org","@type":"Organization","@id":"' + SITE + '/#organization","name":"Chase Golden Globe","legalName":"Chase Golden Globe Pty Ltd","url":"' + SITE + '/","logo":"' + SITE + '/assets/logo.png","foundingDate":"2006","email":"info@chasegoldenglobe.com.au","description":"Chase Golden Globe is a private international business and investment platform that began by trading fine furniture between Indonesia and Australia in 2006, and today connects investors to projects across international markets.","founder":{"@type":"Person","name":"Fouad Barhoum"},"address":{"@type":"PostalAddress","addressLocality":"Sydney","addressRegion":"NSW","addressCountry":"AU"},"areaServed":["AU","ID","SA","QA","AE","DZ","EG","GB","CH","LU"]}'],
    active=None,
    body=f'''<main id="main">
<div class="hero" style="background-image:url('/assets/hero-home.jpg');">
  <div class="hero-in">
    <div class="eyebrow" data-i18n="hero.eyebrow">Private Investment House · Est. 2006</div>
    <h1 class="h-home" data-i18n="hero.title">From the docks to the deal room.</h1>
    <p class="lede on-dark" data-i18n="hero.lede">Chase Golden Globe began by trading fine furniture between Indonesia and Australia in 2006. Today it connects investors to projects across international markets, from real estate to energy to trade.</p>
    <div class="btn-row"><a class="btn btn-brass" href="/about.html" data-i18n="hero.btn1">Our Story</a><a class="btn btn-line-dark" href="/contact.html" data-i18n="hero.btn2">Start a Conversation</a></div>
  </div>
</div>

<div class="band"><div class="wrap">
  <h2 class="sr-only" data-i18n="home.stats.heading">By the Numbers</h2>
  <div class="stats">
    <div class="stat"><div class="stat-l" data-i18n="home.stats.deals.label">Deals Facilitated</div><div class="stat-n">$3.2B+</div><div class="stat-u" data-i18n="home.stats.deals.unit">USD, cumulative deal value</div></div>
    <div class="stat"><div class="stat-l" data-i18n="home.stats.years.label">In Operation</div><div class="stat-n">20</div><div class="stat-u" data-i18n="home.stats.years.unit">Years, continuously since 2006</div></div>
    <div class="stat"><div class="stat-l" data-i18n="home.stats.countries.label">Global Reach</div><div class="stat-n">10</div><div class="stat-u" data-i18n="home.stats.countries.unit">Countries across four regions, including head office</div></div>
  </div>
</div></div>

<section aria-labelledby="story-h"><div class="wrap">
  <h2 class="sr-only" id="story-h" data-i18n="home.story.heading">The Story</h2>
  <div class="row2">
    <div class="panel panel-dark">
      <div class="eyebrow on-dark" data-i18n="home.origin.eyebrow">Our Origin</div>
      <h3 data-i18n="home.origin.title">A trade in craftsmanship, before it was a trade in capital.</h3>
      <p data-i18n="home.origin.body">In 2006, Chase Golden Globe began by importing fine furniture and handicrafts from Indonesia into Australia, starting with a small showroom before growing into an international trading network.</p>
      <a class="arrow" href="/about.html" data-i18n="home.origin.link">Read the full story →</a>
    </div>
    <div class="panel panel-khaki">
      <div class="eyebrow on-khaki" data-i18n="home.today.eyebrow">Today</div>
      <h3 data-i18n="home.today.title">Investors on one side. Projects on the other.</h3>
      <p data-i18n="home.today.body">Fouad Barhoum now travels the world connecting investors to projects, sitting between the two: due diligence, investor reporting and pitch preparation, so capital understands the risk and projects are ready to receive it.</p>
      <a class="arrow" href="/capabilities.html" data-i18n="home.today.link">See what we do →</a>
    </div>
  </div>
</div></section>

<section class="tight" aria-labelledby="cap-h"><div class="wrap">
  <div class="sec-head"><div class="eyebrow" data-i18n="nav.capabilities">Capabilities</div><h2 class="h-sec" id="cap-h" data-i18n="home.cap.title">Nine ways we move a project toward capital.</h2></div>
  <div class="strip">
{strip_html()}  </div>
</div></section>

<section aria-labelledby="ind-h"><div class="wrap">
  <div class="sector-band" style="background-image:url('/assets/hero-industries.jpg');">
    <div class="sector-in">
      <div>
        <div class="eyebrow on-dark" data-i18n="nav.industries">Industries</div>
        <h2 class="h-sec" id="ind-h" data-i18n="home.ind.title">Sectors we know from the inside.</h2>
        <p class="lede on-dark" data-i18n="home.ind.body">Several of these go back to the group's own ventures — furniture export, food and agriculture, luxury property — not sectors studied from a distance.</p>
        <a class="btn btn-brass" href="/industries.html" data-i18n="home.ind.btn">All nine sectors</a>
      </div>
      <div class="sector-list">
{sector_list()}      </div>
    </div>
  </div>
</div></section>

<section class="tight" aria-labelledby="pres-h"><div class="wrap">
  <div class="pres-teaser">
    <div class="map-mini">{MAP_MINI}</div>
    <div>
      <div class="eyebrow" data-i18n="nav.presence">Presence</div>
      <h2 class="h-sec" id="pres-h" data-i18n="home.pres.title">Headquartered in Sydney. Present in ten countries.</h2>
      <p class="copy" data-i18n="home.pres.body">Australia, Indonesia, Saudi Arabia, Qatar, the United Arab Emirates, Algeria, Egypt, the United Kingdom, Switzerland and Luxembourg — the Gulf, North Africa, Europe and Southeast Asia.</p>
      <a class="btn btn-line" href="/presence.html" data-i18n="home.pres.btn">Where we operate</a>
    </div>
  </div>
</div></section>
</main>
''')

PAGES["about"] = dict(
    slug="about", active="about",
    title="About | Chase Golden Globe",
    desc="From exporting fine furniture out of Indonesia to connecting investors and projects worldwide: the story of Chase Golden Globe and founder Fouad Barhoum.",
    schema=[breadcrumb_schema("About", "about"),
            '{"@context":"https://schema.org","@type":"AboutPage","url":"' + SITE + '/about.html","mainEntity":{"@type":"Organization","name":"Chase Golden Globe","founder":{"@type":"Person","name":"Fouad Barhoum"},"foundingDate":"2006"}}'],
    body=f'''<main id="main">
{phero("/assets/hero-lobby.jpg", "nav.about", "About", "about.eyebrow", "About", "about.title", "Our story.", "about.lede", "From a small furniture showroom in 2006 to an international business and investment platform, in three chapters.", "about-h")}
<section class="tight" aria-labelledby="chapters-h"><div class="wrap">
  <h2 class="sr-only" id="chapters-h" data-i18n="about.chapters">Chapters</h2>
  <div class="timeline" role="tablist" aria-label="Company history">
    <button type="button" role="tab" id="tab-1" aria-controls="chapter-1" aria-selected="true" class="active"><b data-i18n="about.tl1.year">2006</b><span data-i18n="about.tab1">Our Origin</span></button>
    <button type="button" role="tab" id="tab-2" aria-controls="chapter-2" aria-selected="false" tabindex="-1"><b data-i18n="about.tl2.year">2010</b><span data-i18n="about.tab2">Growth &amp; Expansion</span></button>
    <button type="button" role="tab" id="tab-3" aria-controls="chapter-3" aria-selected="false" tabindex="-1"><b data-i18n="about.tl3.year">Today</b><span data-i18n="about.tab3">Investment Platform</span></button>
  </div>
  <div class="chapter active" id="chapter-1" role="tabpanel" aria-labelledby="tab-1">
    <div class="photo" style="background-image:url('/assets/chapter-2006.jpg');" role="img" aria-label="A craftsman carving a teak panel in an Indonesian furniture workshop"></div>
    <div class="panel panel-dark"><div class="eyebrow on-dark" data-i18n="about.ch1.eyebrow">2006 · Indonesia to Australia</div><h2 data-i18n="about.ch1.title">A name inspired by quality and value.</h2><p data-i18n="about.ch1.body">In 2006, Chase Golden Globe began its first trading operations, importing fine furniture and handicrafts from Indonesia into the Australian market. The name was inspired by the Golden Globe grape — distinctive, refined, and naturally associated with quality and value. What started as a small showroom gradually expanded into a broader trading network built on trust, discipline and long-term relationships.</p></div>
  </div>
  <div class="chapter" id="chapter-2" role="tabpanel" aria-labelledby="tab-2" hidden>
    <div class="photo" style="background-image:url('/assets/chapter-2010.jpg');" role="img" aria-label="A gilded reception room with chandelier and marble floor"></div>
    <div class="panel panel-khaki"><div class="eyebrow on-khaki" data-i18n="about.ch2.eyebrow">2010 · Europe, the Middle East, Asia</div><h2 data-i18n="about.ch2.title">From a showroom to an international network.</h2><p data-i18n="about.ch2.body">As the business grew, Chase Golden Globe began re-exporting selected Indonesian furniture and handicraft to markets across Europe and the Middle East, then expanded into food and agricultural products, including Australian honey and premium dairy, supplying Indonesia, Asia and international markets. In 2010 a new chapter began through a venture with Royalty Prussia, extending into high-end interior design, luxury real estate, premium renovations and prestigious properties including embassies and palaces around the world.</p></div>
  </div>
  <div class="chapter" id="chapter-3" role="tabpanel" aria-labelledby="tab-3" hidden>
    <div class="photo" style="background-image:url('/assets/hero-capabilities.jpg');" role="img" aria-label="A boardroom overlooking a city at dusk"></div>
    <div class="panel panel-dark"><div class="eyebrow on-dark" data-i18n="about.ch3.eyebrow">Today · Worldwide</div><h2 data-i18n="about.ch3.title">A broader international business and investment network.</h2><p data-i18n="about.ch3.body">Today, Chase Golden Globe operates as an international business and investment platform. Fouad Barhoum travels the world connecting investors to projects, drawing on relationships built across investment and finance, real estate, oil and gas, mining, international trade and strategic partnerships. The company has worked closely with investment authorities and government-linked institutions in Indonesia, and its network extends to sovereign wealth funds, state-owned companies and private investors worldwide.</p></div>
  </div>
</div></section>

<section class="tight" aria-labelledby="philosophy-h"><div class="wrap">
  <div class="row2">
    <div class="panel panel-khaki"><div class="eyebrow on-khaki" data-i18n="about.philosophy.eyebrow">Our Philosophy</div><h2 id="philosophy-h" data-i18n="about.philosophy.title">Start small. Think big. Go fast.</h2><p data-i18n="about.philosophy.body">The journey has included successes, challenges, setbacks and failures. Failure is not regarded as defeat; it is experience, and a lesson that strengthens the next decision. Sustainable success comes from discipline and consistency, not shortcuts. Markets change, opportunities change, people change. Integrity, professionalism and trust must remain constant.</p></div>
    <div class="panel panel-dark"><div class="eyebrow on-dark" data-i18n="about.trust.eyebrow">Trust Is Our Capital</div><h2 data-i18n="about.trust.title">Trust takes years to build and seconds to lose.</h2><p data-i18n="about.trust.body">For this reason, Chase Golden Globe operates with discipline, discretion and accountability. We do not pursue every opportunity. We focus on those with a credible foundation, a clear commercial purpose and the potential to create real value for all parties.</p></div>
  </div>
</div></section>

<section aria-labelledby="founder-h"><div class="wrap">
  <div class="sec-head"><div class="eyebrow" data-i18n="about.founder.eyebrow">Founder</div><h2 class="h-sec" id="founder-h" data-i18n="about.founder.name">Fouad Barhoum</h2></div>
  <div class="founder">
    <div class="plate"><img src="/assets/founder-fouad.jpg" alt="Portrait of Fouad Barhoum, founder of Chase Golden Globe" width="640" height="800" loading="lazy"></div>
    <div>
      <p class="copy" data-i18n="about.founder.p1">Fouad Barhoum is an Algerian entrepreneur based between Algeria, Australia and Indonesia, with a strong international track record in business structuring, investment strategy and high-level deal execution. His academic foundation in financial services, risk assessment and market analysis comes from the University of Technology Sydney and the University of Sydney, and he has built extensive expertise evaluating opportunities, structuring ventures and negotiating complex transactions across multiple sectors.</p>
      <p class="copy" data-i18n="about.founder.p2">His experience spans agriculture, energy, infrastructure, retail and manufacturing, where he has been actively involved in building businesses, scaling operations and closing strategic partnerships with both private-sector leaders and government entities. He is also actively involved with Boldbridge Capital, an international investment and infrastructure group, contributing to strategic projects including large-scale industrial developments such as &ldquo;5 Pockets by Boldbridge,&rdquo; a vertically integrated textile manufacturing initiative targeting global apparel supply chains.</p>
      <p class="copy" data-i18n="about.founder.p3">His current focus is on developing large-scale projects that create long-term value, particularly in food security, industrial manufacturing and cross-border investments connecting Africa, the Middle East and Asia. Beyond business, he is deeply committed to philanthropy through Barhoum Charity, supporting education, food programs and orphan care, reflecting his belief that success must always be aligned with impact. He operates with a clear philosophy: discipline, loyalty and execution. He values meaningful partnerships, long-term vision, and working with individuals who move with purpose.</p>
      <div class="meta">
        <div><div class="eyebrow" data-i18n="about.founder.languages.label">Languages</div><p class="copy" data-i18n="about.founder.languages.value">Arabic · English · French · Indonesian</p></div>
        <div><div class="eyebrow" data-i18n="about.founder.focus.label">Focus Areas</div><p class="copy" data-i18n="about.founder.focus.value">Investment · Strategic Partnerships · Industrial Projects · Global Trade</p></div>
      </div>
    </div>
  </div>
</div></section>
</main>
''')

PAGES["capabilities"] = dict(
    slug="capabilities", active="capabilities",
    title="Capabilities | Chase Golden Globe",
    desc="Nine core capabilities of Chase Golden Globe, from structured finance and government liaison to capital raising, M&amp;A and joint ventures, with due diligence, investor reporting and pitch preparation on every project.",
    schema=[breadcrumb_schema("Capabilities", "capabilities")],
    body=f'''<main id="main">
{phero("/assets/hero-handshake.jpg", "nav.capabilities", "Capabilities", "cap.eyebrow", "What We Do", "cap.title", "Core capabilities.", "cap.lede", "Nine capabilities that take a project from a conversation to a bankable, fundable proposition.", "cap-h")}
<section class="tight" aria-labelledby="core-h"><div class="wrap">
  <div class="panel panel-dark core">
    <div>
      <div class="eyebrow on-dark" data-i18n="cap.core.eyebrow">Between Opportunity and Capital</div>
      <h2 class="h-sec" id="core-h" data-i18n="cap.core.title">The work that sits underneath every engagement.</h2>
      <p data-i18n="cap.core.body">Our role is to sit between opportunity and capital, examining the structure, counterparties, market conditions and risks before a transaction moves forward. Three things happen on every project, whatever the capability.</p>
      <img class="core-photo" src="/assets/capabilities-desk.jpg" alt="A due-diligence binder of financial statements and an investment memorandum on a desk" width="1264" height="848" loading="lazy">
    </div>
    <div class="core-items">
      <div><b data-i18n="cap.core.1.t">Due diligence</b><p data-i18n="cap.core.1.b">Structure, counterparties, market and risk examined before anyone commits.</p></div>
      <div><b data-i18n="cap.core.2.t">Investor reporting</b><p data-i18n="cap.core.2.b">Clear, regular reporting so capital understands what it is backing.</p></div>
      <div><b data-i18n="cap.core.3.t">Pitch preparation</b><p data-i18n="cap.core.3.b">Investment memoranda and pitch decks built to the standard investors expect.</p></div>
    </div>
  </div>
</div></section>

<section class="tight" aria-labelledby="caps-h"><div class="wrap">
  <div class="sec-head"><div class="eyebrow" data-i18n="cap.h2.eyebrow">How We Move Capital</div><h2 class="h-sec" id="caps-h" data-i18n="cap.h2.title">Work we do directly, not a menu we outsource.</h2><p class="copy" data-i18n="cap.h2.body">Where a capability requires a specific financial services licence, it is delivered in partnership with an appropriately licensed practitioner or firm.</p></div>
  <div class="cards3">
{cap_cards()}
  </div>
</div></section>
</main>
''')

PAGES["industries"] = dict(
    slug="industries", active="industries",
    title="Industries | Chase Golden Globe",
    desc="Nine sectors Chase Golden Globe works across: agriculture and food security, energy, infrastructure, retail and hospitality, manufacturing, cross-border trade, real estate, oil and gas, and mining.",
    schema=[breadcrumb_schema("Industries", "industries")],
    body=f'''<main id="main">
{phero("/assets/hero-sectors.jpg", "nav.industries", "Industries", "ind.eyebrow", "Where We Work", "ind.title", "Sectors we understand.", "ind.lede", "Nine sectors, several of them shaped by the group's own ventures rather than studied from a distance.", "ind-h")}
<section class="tight" aria-labelledby="sectors-h"><div class="wrap">
  <div class="sec-head"><div class="eyebrow" data-i18n="ind.h2.eyebrow">From the Inside</div><h2 class="h-sec" id="sectors-h" data-i18n="ind.h2.title">The group has operated in these sectors, not only advised on them.</h2></div>
  <div class="cards3">
{sector_cards()}
  </div>
</div></section>
</main>
''')

PAGES["presence"] = dict(
    slug="presence", active="presence",
    title="Presence | Chase Golden Globe",
    desc="Chase Golden Globe is headquartered in Sydney and present in ten countries across the Gulf, North Africa, Europe and Southeast Asia.",
    schema=[breadcrumb_schema("Presence", "presence")],
    body=f'''<main id="main">
{phero("/assets/hero-map-wall.jpg", "nav.presence", "Presence", "pres.eyebrow", "Global Presence", "pres.title", "Where we operate.", "pres.lede", "Headquartered in Sydney since 2006, with an established presence in ten countries across the Gulf, North Africa, Europe and Southeast Asia.", "pres-h")}
<section class="tight" aria-labelledby="loc-h"><div class="wrap">
  <h2 class="sr-only" id="loc-h" data-i18n="pres.key">Key Locations</h2>
  <div class="office3">
    <div class="office" style="background-image:url('/assets/office-australia.jpg');"><div><div class="eyebrow on-dark" data-i18n="pres.office.eyebrow">Head Office</div><h3 data-i18n="country.Australia">Australia</h3><p data-i18n="pres.office.body">Headquartered in Sydney, New South Wales, operating continuously since 2006.</p></div></div>
    <div class="office" style="background-image:url('/assets/office-indonesia.jpg');"><div><div class="eyebrow on-dark" data-i18n="pres.idn.eyebrow">Where It Began</div><h3 data-i18n="country.Indonesia">Indonesia</h3><p data-i18n="pres.idn.body">First trading operations began here in 2006; relationships with investment authorities and government-linked institutions continue today.</p></div></div>
    <div class="office" style="background-image:url('/assets/office-algeria.jpg');"><div><div class="eyebrow on-dark" data-i18n="pres.dza.eyebrow">Founder's Roots</div><h3 data-i18n="country.Algeria">Algeria</h3><p data-i18n="pres.dza.body">An active base for cross-border trade and investment across North Africa.</p></div></div>
  </div>
</div></section>

<section aria-labelledby="map-h"><div class="wrap">
  <div class="sec-head"><div class="eyebrow" data-i18n="pres.map.eyebrow">Ten Countries</div><h2 class="h-sec" id="map-h" data-i18n="pres.map.title">Select a country to see its role.</h2></div>
  <div class="map-block">
    <div class="map-wrap">{MAP}</div>
    <div class="map-side">
      <div class="map-stats"><div><b>10</b><span data-i18n="pres.map.stat2">Countries, incl. HQ</span></div><div><b>4</b><span data-i18n="pres.map.stat1">Regions</span></div></div>
      <div class="ccard" id="countryCard" aria-live="polite">
        <div class="eyebrow on-dark" data-role data-fallback-role="Head Office">Head Office</div>
        <h3 data-name>Australia</h3>
        <p data-body>Sydney, New South Wales. The company's registered home since 2006.</p>
      </div>
      <div class="clist" id="countryList" role="group" aria-label="Countries">
{country_buttons()}
      </div>
    </div>
  </div>
</div></section>
</main>
''')

PAGES["contact"] = dict(
    slug="contact", active="contact",
    title="Contact | Chase Golden Globe",
    desc="Reach Chase Golden Globe directly for matters of investment, trade or partnership. Head office in Sydney, Australia.",
    schema=[breadcrumb_schema("Contact", "contact")],
    no_cta=True,
    body=f'''<main id="main">
{phero("/assets/hero-contact-new.jpg", "nav.contact", "Contact", "home.cta.eyebrow", "Get in Touch", "home.cta.title", "Begin the conversation.", "home.cta.body", "For matters of investment, trade or partnership, enquiries are received directly.", "contact-h")}
<section class="tight" aria-labelledby="contact-h2"><div class="wrap">
  <div class="contact">
    <div class="panel panel-dark">
      <div class="eyebrow on-dark" data-i18n="contact.h2.eyebrow">Tell Us About the Project</div>
      <h2 id="contact-h2" data-i18n="contact.h2.title">The most direct way to reach us is by email.</h2>
      <p data-i18n="contact.h2.body">Tell us briefly about the project, the market it sits in and what stage it is at. We reply personally.</p>
      <div class="email"><a href="mailto:info@chasegoldenglobe.com.au">info@chasegoldenglobe.com.au</a><button type="button" class="copybtn" id="copyEmail" data-email="info@chasegoldenglobe.com.au" data-i18n="contact.copy">Copy</button></div>
      <p class="note" data-i18n="contact.office">Head office: Sydney, New South Wales, Australia</p>
      <a class="btn btn-brass" href="mailto:info@chasegoldenglobe.com.au" data-i18n="contact.btn">Send an Enquiry</a>
    </div>
    <div class="panel panel-khaki">
      <div class="eyebrow on-khaki" data-i18n="contact.confidentiality.eyebrow">In Confidence</div>
      <h2 data-i18n="contact.confidentiality.title">Every conversation stays private.</h2>
      <p data-i18n="contact.confidentiality.body">Enquiries are handled with discretion from the first message. A non-disclosure agreement can be put in place before any detail is shared, where the matter calls for it. Only the people directly involved review what you send, and nothing is passed to a third party, partner or other client without your consent.</p>
      <div class="meta-inline">
        <div><div class="eyebrow on-khaki" data-i18n="contact.confidentiality.f1.label">Discretion</div><p data-i18n="contact.confidentiality.f1.value">From the first message</p></div>
        <div><div class="eyebrow on-khaki" data-i18n="contact.confidentiality.f2.label">NDA</div><p data-i18n="contact.confidentiality.f2.value">Available before details are shared</p></div>
      </div>
    </div>
  </div>
</div></section>
</main>
''')

PAGES["legal"] = dict(
    slug="legal", active=None,
    title="Legal &amp; Privacy | Chase Golden Globe",
    desc="Licensing disclosure, privacy notice and terms of use for the Chase Golden Globe website.",
    schema=[breadcrumb_schema("Legal & Privacy", "legal")],
    body=f'''<main id="main" class="legal">
<section class="tight"><div class="wrap">
  <div class="phero phero-plain" style="min-height:0;"><div class="phero-in">
    {crumbs("footer.legal", "Legal &amp; Privacy")}
    <div class="eyebrow on-dark" data-i18n="legal.eyebrow">Legal &amp; Privacy</div>
    <h1 class="h-page" data-i18n="legal.title">A plain-language summary of how this site operates.</h1>
  </div></div>
</div></section>
<section class="tight"><div class="wrap">
  <div class="legal-block">
    <div class="eyebrow" data-i18n="legal.licensing.eyebrow">Financial Services Disclosure</div>
    <h2 data-i18n="legal.licensing.title">Licensing.</h2>
    <p class="copy" data-i18n="legal.licensing.body">Chase Golden Globe Pty Ltd is a private trading, investment and trade facilitation house. It is <strong>not itself a licensed financial services provider</strong>. Where a piece of work requires a specific professional or financial services licence, for example under the Australian Corporations Act or an equivalent regime in another market, that work is carried out in partnership with appropriately licensed practitioners, advisers or firms. Nothing on this website constitutes financial, investment, legal or tax advice, and nothing here should be relied upon as such. Prospective partners and clients should seek their own independent professional advice before entering into any arrangement.</p>
  </div>
  <div class="legal-block">
    <div class="eyebrow" data-i18n="legal.privacy.eyebrow">Privacy Notice</div>
    <h2 data-i18n="legal.privacy.title">How this site handles data.</h2>
    <p class="copy" data-i18n="legal.privacy.body1">This website does not use cookies, analytics, or advertising trackers, and it does not run any forms that collect personal information. Your language choice is stored in your browser only. The only third-party requests made by this site are to Google Fonts, which serves the typefaces used in this design; this may involve your browser making a request to Google's servers for font files. The site is hosted on GitHub Pages, which may log standard technical information such as IP addresses as part of normal web server operation, consistent with GitHub's own privacy practices.</p>
    <p class="copy" data-i18n="legal.privacy.body2">If you contact us by email, we will hold your message and any details you choose to share for as long as reasonably necessary to respond to your enquiry, and will not share them with third parties except where necessary to do the work you have asked us to do, or where required by law.</p>
    <p class="copy" data-i18n="legal.privacy.body3">This notice reflects the site as it stands today. If forms, analytics, or other data collection are added in future, this page will be updated accordingly.</p>
  </div>
  <div class="legal-block">
    <div class="eyebrow" data-i18n="legal.terms.eyebrow">Website Terms of Use</div>
    <h2 data-i18n="legal.terms.title">Using this website.</h2>
    <p class="copy" data-i18n="legal.terms.body">The content on this website is provided for general information about Chase Golden Globe and its activities. While we try to keep it accurate and current, we make no warranty as to its completeness and reserve the right to update it at any time without notice. All logos, text and design elements on this site are the property of Chase Golden Globe Pty Ltd unless otherwise noted, and may not be reproduced without permission.</p>
  </div>
  <div class="legal-block">
    <div class="eyebrow" data-i18n="legal.questions.eyebrow">Questions</div>
    <h2 data-i18n="legal.questions.title">Have a question about this page?</h2>
    <p class="copy" data-i18n="legal.questions.body">If you have any questions about licensing, privacy, or how this site operates, get in touch directly.</p>
    <p class="copy" style="margin-top:14px"><a href="mailto:info@chasegoldenglobe.com.au" style="text-decoration:underline;text-underline-offset:3px">info@chasegoldenglobe.com.au</a></p>
    <p class="legal-updated" data-i18n="legal.updated">Last updated: September 2026</p>
  </div>
</div></section>
</main>
''')

PAGES["404"] = dict(
    slug="404", active=None, noindex=True, minimal=True,
    title="Page Not Found | Chase Golden Globe",
    desc="The page you are looking for may have moved or been renamed.",
    body='''<main id="main">
<section><div class="wrap error-page">
  <div class="panel panel-dark">
    <div class="eyebrow on-dark">404</div>
    <h1 class="h-page" data-i18n="error404.title">This page does not exist.</h1>
    <p style="margin-top:14px" data-i18n="error404.body">The page you are looking for may have moved or been renamed. Start again from the homepage, or go straight to what you need below.</p>
    <div class="btn-row"><a class="btn btn-brass" href="/" data-i18n="error404.home">Return Home</a><a class="btn btn-line-dark" href="/contact.html" data-i18n="home.cta.btn">Contact Us</a></div>
  </div>
</div></section>
</main>
''')

# --------------------------------------------------------------------------
if __name__ == "__main__":
    for slug, p in PAGES.items():
        html = head(p) + "<body>\n" + nav(p.get("active")) + p["body"] + footer(cta=not p.get("no_cta") and not p.get("minimal"), minimal=p.get("minimal", False))
        with open(os.path.join(HERE, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", slug + ".html", len(html) // 1024, "KB")

    import i18n_src, json
    n = i18n_src.emit(os.path.join(HERE, "assets", "i18n.js"))
    print("wrote assets/i18n.js", n // 1024, "KB")
    # verify every data-i18n key used in the pages exists in EN
    used = set()
    for slug in PAGES:
        used |= set(re.findall(r'data-i18n="([^"]+)"', open(os.path.join(HERE, f"{slug}.html"), encoding="utf-8").read()))
    missing = sorted(k for k in used if k not in i18n_src.EN)
    unused = sorted(k for k in i18n_src.EN if k not in used and not k.startswith("pres.c.") and k not in ("nav.close", "contact.copied"))
    print("keys used:", len(used), "| missing from EN:", missing or "none", "| unused:", unused or "none")
