#!/usr/bin/env python3
"""Erzeugt die statischen HTML-Seiten (EN + DE) der Website.

Nur nötig, wenn sich Aufbau, feste Texte, Praxis-Inhalte oder Rechtstexte ändern.
Fotos, Motion-Projekte, Laborkarten und Einstellungen kommen zur Laufzeit aus
/content/*.json und werden im CMS unter /admin gepflegt.

Aufruf:  python3 tools/build.py
"""
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "public"
SITE = "TRVR GDCHLD Visuals"

# ---------------------------------------------------------------- Rechtliche Angaben
# Impressum und Datenschutz stehen in public/content/legal.json (im CMS unter
# "Rechtliches" bearbeitbar). Die Seiten werden hier vorab erzeugt und im
# Browser zusätzlich aus legal.json aktualisiert (assets/js/main.js).
import json
LEGAL_FILE = ROOT / "content" / "legal.json"

# ---------------------------------------------------------------- Routen
URL = {
    "en": {"home": "/", "guide": "/guide/", "legal": "/legal-notice/", "privacy": "/privacy/", "album": "/album/"},
    "de": {"home": "/de/", "guide": "/de/praxis/", "legal": "/de/impressum/", "privacy": "/de/datenschutz/", "album": "/de/album/"},
}

# ---------------------------------------------------------------- Icons
ICON = {
    "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5l12 7-12 7z"/></svg>',
    "play_line": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "back": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 8h16M4 16h16"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10 9.3l5 2.7-5 2.7z" fill="currentColor"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></svg>',
    "pinterest": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M11.2 12.2c-.9-.7-1.1-2-.5-3 .7-1.2 2.3-1.7 3.6-1.1 1.4.7 1.9 2.3 1.3 3.8-.6 1.6-2.1 2.6-3.4 2.1"/><path d="M12.4 10.5l-2.6 10"/></svg>',
}

# ---------------------------------------------------------------- Texte
T = {
    "en": {
        "skip": "Skip to content", "nav_label": "Main navigation", "lang_label": "Choose language",
        "menu": "Open menu", "theme_light": "Switch to light theme",
        "nav": [("#work", "Photography"), ("#motion", "Motion"), ("#lab", "Lab"), ("#about", "About")],
        "guide": "Guide", "cta": "Start a project",
        "legal": "Legal notice", "privacy": "Privacy", "other_lang": "Deutsch", "home": "Back to home",
        "desc": "Photography and motion graphics by TRVR GDCHLD Visuals – from the first test series to the finished clip.",
        "hero_eyebrow": "Photography · Motion graphics · ", "city_key": "city",
        "hero_h1": 'Hold the light.<br>Shape the<br><em>motion.</em>',
        "hero_p": "Stills and motion graphics from a single studio – from the first test series to the finished clip.",
        "view_work": "View work", "est": "EST.", "logo_alt": "TRVR GDCHLD Visuals logo",
        "specs": [("CAMERA", "LUMIX G70"), ("LENS", "14–42 mm · f/3.5–5.6"), ("MOTION", "DaVinci Resolve · Fusion")],
        "available": "AVAILABLE",
        "work_eyebrow": "01 — Photography", "work_h2": "Albums", "filter_label": "Filter by category",
        "motion_eyebrow": "02 — Motion graphics", "motion_h2": "Images in motion",
        "motion_p": "Title sequences, UI animations and logo reveals – built in DaVinci Resolve Fusion.",
        "reel_btn": "Load and play showreel",
        "reel_note": 'Clicking loads the video from YouTube, which transfers data to YouTube – see the <a href="/privacy/#youtube">privacy policy</a>.',
        "playlists_h3": "Playlists",
        "album_full": "Open photo full screen", "album_strip": "All photos in this album",
        "album_back": "All albums", "album_photos": "photos", "album_label": "Album",
        "lab_eyebrow": "03 — Lab", "lab_h2": "Every series starts<br>with a card.",
        "lab_p": "Before every test shot, I hold a card with the settings up to the lens. That way it stays clear what shutter speed, aperture, ISO and white balance do to a subject.",
        "tests_label": "Test series", "pick_label": "Which side a card sets",
        "lab_more": "More in the guide:", "lab_links": [("#aperture", "Aperture f/3.5–f/22"), ("#iso", "ISO 200–25600"), ("#wb", "White balance 2500–10000 K")],
        "about_eyebrow": "04 — About", "about_hi": "Hi, I’m ", "portrait": "[Portrait photo]",
        "services": [("Portrait & People", "Photo"), ("Logo animation", "Motion"), ("Product photography", "Photo"), ("Social reels", "Motion"), ("Event & Street", "Photo"), ("UI motion", "Motion")],
        "contact_eyebrow": "05 — Contact", "contact_h2": "Let’s put something<br>in the frame.", "mail_ph": "[your@email]",
    },
    "de": {
        "skip": "Zum Inhalt springen", "nav_label": "Hauptnavigation", "lang_label": "Sprache wählen",
        "menu": "Menü öffnen", "theme_light": "Helles Design aktivieren",
        "nav": [("#arbeiten", "Fotografie"), ("#motion", "Motion"), ("#labor", "Labor"), ("#ueber", "Über")],
        "guide": "Praxis", "cta": "Projekt anfragen",
        "legal": "Impressum", "privacy": "Datenschutz", "other_lang": "English", "home": "Zur Startseite",
        "desc": "Fotografie und Motion Graphics von TRVR GDCHLD Visuals – von der ersten Testreihe bis zum fertigen Clip.",
        "hero_eyebrow": "Fotografie · Motion Graphics · ", "city_key": "city",
        "hero_h1": 'Licht halten.<br>Bewegung<br><em>gestalten.</em>',
        "hero_p": "Stille Bilder und bewegte Grafik aus einer Hand – von der ersten Testreihe bis zum fertigen Motion-Clip.",
        "view_work": "Arbeiten ansehen", "est": "SEIT", "logo_alt": "Logo TRVR GDCHLD Visuals",
        "specs": [("KAMERA", "LUMIX G70"), ("OBJEKTIV", "14–42 mm · f/3.5–5.6"), ("MOTION", "DaVinci Resolve · Fusion")],
        "available": "VERFÜGBAR",
        "work_eyebrow": "01 — Fotografie", "work_h2": "Alben", "filter_label": "Nach Kategorie filtern",
        "motion_eyebrow": "02 — Motion Graphics", "motion_h2": "Bilder in Bewegung",
        "motion_p": "Titelsequenzen, UI-Animationen und Logo-Reveals – gebaut in DaVinci Resolve Fusion.",
        "reel_btn": "Showreel laden und abspielen",
        "reel_note": 'Mit dem Klick wird das Video von YouTube geladen. Dabei werden Daten an YouTube übertragen – mehr dazu im <a href="/de/datenschutz/#youtube">Datenschutz</a>.',
        "playlists_h3": "Playlists",
        "album_full": "Foto im Vollbild öffnen", "album_strip": "Alle Fotos dieses Albums",
        "album_back": "Alle Alben", "album_photos": "Fotos", "album_label": "Album",
        "lab_eyebrow": "03 — Labor", "lab_h2": "Jede Serie beginnt<br>mit einer Karte.",
        "lab_p": "Vor jedem Testbild halte ich eine Karte mit den Einstellungen ins Bild. So bleibt nachvollziehbar, was Verschlusszeit, Blende, ISO und Weißabgleich mit einem Motiv machen.",
        "tests_label": "Testreihen", "pick_label": "Welche Seite eine Karte setzt",
        "lab_more": "Mehr in der Praxis:", "lab_links": [("#blende", "Blende f/3.5–f/22"), ("#iso", "ISO 200–25600"), ("#weiss", "Weißabgleich 2500–10000 K")],
        "about_eyebrow": "04 — Über mich", "about_hi": "Hi, ich bin ", "portrait": "[Portraitfoto]",
        "services": [("Portrait & People", "Foto"), ("Logo-Animation", "Motion"), ("Produktfotografie", "Foto"), ("Social-Reels", "Motion"), ("Event & Street", "Foto"), ("UI-Motion", "Motion")],
        "contact_eyebrow": "05 — Kontakt", "contact_h2": "Lass uns etwas<br>ins Bild setzen.", "mail_ph": "[deine@mail.de]",
    },
}


# ---------------------------------------------------------------- Bausteine
def head(lang, title, desc, page, alt_page):
    other = "de" if lang == "en" else "en"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#1C1220">
<script>try{{var m=localStorage.getItem("theme");if(m==="light"||m==="dark"){{document.documentElement.dataset.theme=m;}}if(m==="light")document.querySelector('meta[name="theme-color"]').content="#F6E7D8";}}catch(e){{}}</script>
<link rel="alternate" hreflang="{lang}" href="{URL[lang].get(page, '/')}">
<link rel="alternate" hreflang="{other}" href="{URL[other].get(alt_page, '/')}">
<link rel="alternate" hreflang="x-default" href="{URL['en'].get(alt_page if lang == 'de' else page, '/')}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/syne-var.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="/assets/img/icon-512.png">
<script src="/assets/js/main.js" defer></script>
</head>
<body>
"""


def header(lang, page, alt_page):
    t, u = T[lang], URL[lang]
    other = "de" if lang == "en" else "en"
    home = u["home"]
    pfx = "" if page == "home" else home
    links = "".join(f'<a href="{pfx}{h}">{esc(n)}</a>' for h, n in t["nav"])
    guide_cur = ' aria-current="page"' if page == "guide" else ""
    en_cur = ' aria-current="true"' if lang == "en" else ""
    de_cur = ' aria-current="true"' if lang == "de" else ""
    en_href = URL["en"].get(page if lang == "en" else alt_page, "/")
    de_href = URL["de"].get(page if lang == "de" else alt_page, "/de/")
    contact = "#contact" if lang == "en" else "#kontakt"
    return f"""<a class="skip" href="#main">{t['skip']}</a>
<header class="site-header">
<div class="wrap">
<a class="brand" href="{home}"><span class="brand-plate"><img class="logo-dark" src="/assets/img/logo-mark-dark.png" alt="" width="120" height="96"><img class="logo-light" src="/assets/img/logo-mark-light.png" alt="" width="120" height="96"></span><span class="brand-name"><b>TRVR GDCHLD</b><span>VISUALS</span></span></a>
<nav class="nav" id="nav" aria-label="{t['nav_label']}">
{links}
<a href="{u['guide']}"{guide_cur}>{t['guide']}</a>
<a class="btn btn-primary" href="{pfx}{contact}">{t['cta']}</a>
<div class="lang" role="group" aria-label="{t['lang_label']}"><a href="{en_href}" lang="en"{en_cur}>EN</a><a href="{de_href}" lang="de"{de_cur}>DE</a></div>
</nav>
<div class="header-tools">
<button class="theme-btn" type="button" aria-pressed="false" aria-label="{t['theme_light']}" title="{t['theme_light']}"><svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg><svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></svg></button>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="{t['menu']}">{ICON['menu']}</button>
</div>
</div>
</header>
"""


def footer_links(lang, page, alt_page, dark=True):
    t, u = T[lang], URL[lang]
    other = "de" if lang == "en" else "en"
    cur = lambda p: ' aria-current="page"' if p == page else ""
    return f"""<footer class="site-footer">
<span>© <span id="year">2026</span> TRVR GDCHLD Visuals</span>
<nav aria-label="Footer">
<a href="{u['guide']}"{cur('guide')}>{t['guide']}</a>
<a href="{u['legal']}"{cur('legal')}>{t['legal']}</a>
<a href="{u['privacy']}"{cur('privacy')}>{t['privacy']}</a>
<a href="{URL[other][alt_page]}" lang="{other}">{t['other_lang']}</a>
</nav>
</footer>"""


YEAR_JS = '<script>document.getElementById("year").textContent=new Date().getFullYear();</script>\n'


def write(path, html):
    p = ROOT / path.lstrip("/")
    if path.endswith("/"):
        p = p / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    print("  ", p.relative_to(ROOT))


# ---------------------------------------------------------------- Design-Elemente
DECO_VB = {"af": "0 0 260 200", "cross": "0 0 200 200", "expo": "0 0 1000 120", "tilt": "0 0 110 560",
           "scale-h": "0 0 1600 60", "scale-v": "0 0 60 1600", "arc-mm": "0 0 800 800", "arc-f": "0 0 800 800",
           "arc-m": "0 0 800 800", "ring": "0 0 700 700", "histo": "0 0 420 240"}


def deco(name, cls, use_id=None):
    """Dezentes Kamera-Element aus assets/img/deco.svg (Farbe kommt aus CSS)."""
    uid = f' id="{use_id}"' if use_id else ""
    return (f'<svg class="deco {cls}" viewBox="{DECO_VB[name]}" aria-hidden="true" focusable="false">'
            f'<use{uid} href="/assets/img/deco.svg#{name}" width="100%" height="100%"/></svg>')


# ---------------------------------------------------------------- Startseite
def home(lang):
    t = T[lang]
    ids = {"en": ("work", "motion", "lab", "about", "contact"), "de": ("arbeiten", "motion", "labor", "ueber", "kontakt")}[lang]
    specs = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in t["specs"])
    services = "".join(f"<li>{esc(a)}<span>{esc(b)}</span></li>" for a, b in t["services"])
    lab_links = "".join(f'<a href="{URL[lang]["guide"]}{h}">{esc(n)}</a>' for h, n in t["lab_links"])
    alt = "home"
    return head(lang, f"{SITE} – {'Photography & Motion' if lang == 'en' else 'Fotografie & Motion'}", t["desc"], "home", alt) + header(lang, "home", alt) + f"""<main id="main">

<section class="hero has-deco" id="top">
{deco('scale-v', 'd-edge-l')}
<div class="wrap hero-grid">
<div class="hero-text">
<div class="eyebrow">{t['hero_eyebrow']}<span data-set="city"></span></div>
<h1>{t['hero_h1']}</h1>
<p>{t['hero_p']}</p>
<div class="hero-actions">
<a class="btn btn-primary" href="#{ids[0]}">{t['view_work']}</a>
<a class="btn btn-ghost" href="#{ids[1]}">{ICON['play_line']}Showreel</a>
</div>
</div>
<div class="hero-mark">
{deco('ring', 'd-hero-ring')}
<div class="logo-plate"><img class="logo-dark" src="/assets/img/logo-full-dark.png" alt="{t['logo_alt']}" width="800" height="757"><img class="logo-light" src="/assets/img/logo-full-light.png" alt="{t['logo_alt']}" width="800" height="757"></div>
<span data-hide-empty="established">{t['est']} <span data-set="established"></span></span>
</div>
</div>
<div class="wrap"><dl class="specs">{specs}<div><dt>{t['available']}</dt><dd class="hl" data-set="available"></dd></div></dl></div>
</section>

<section class="section" id="{ids[0]}">
<div class="wrap">
<div class="section-head">
<div class="titles"><div class="eyebrow">{t['work_eyebrow']}</div><h2>{t['work_h2']}</h2></div>
<div class="filters" id="filters" role="group" aria-label="{t['filter_label']}"></div>
</div>
<div class="album-grid" id="album-grid"></div>
</div>
</section>

<section class="panel has-deco" id="{ids[1]}">
{deco('histo', 'd-motion-histo')}{deco('tilt', 'd-motion-tilt')}
<div class="wrap">
<div class="section-head">
<div class="titles"><div class="eyebrow">{t['motion_eyebrow']}</div><h2>{t['motion_h2']}</h2></div>
<p>{t['motion_p']}</p>
</div>
<div class="reel" id="reel">
<div class="reel-top"><span>SHOWREEL</span><span>16:9</span></div>
<button class="reel-play" id="reel-play" type="button" aria-label="{t['reel_btn']}">{ICON['play']}</button>
<p class="reel-note" id="reel-note">{t['reel_note']}</p>
</div>
<h3 class="sub-h">{t['playlists_h3']}</h3>
<div class="projects" id="playlists"></div>
</div>
</section>

<section class="section has-deco" id="{ids[2]}">
{deco('ring', 'd-lab-ring')}{deco('arc-f', 'd-lab-arc', 'vf-arc')}{deco('scale-v', 'd-edge-l')}
<div class="wrap">
<div class="section-head">
<div class="titles"><div class="eyebrow">{t['lab_eyebrow']}</div><h2>{t['lab_h2']}</h2></div>
<p>{t['lab_p']}</p>
</div>
<div class="tests" id="tests">
<div class="tests-tabs" id="tests-tabs" role="tablist" aria-label="{t['tests_label']}" hidden></div>
<div class="vf">
<div class="vf-status" id="vf-status" aria-hidden="true"></div>
<div class="vf-counter" id="vf-counter" aria-hidden="true"></div>
<div class="vf-frame"><i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i><div class="cmp" id="cmp"></div></div>
<div class="vf-data" id="vf-data"></div>
<div class="vf-expo" id="vf-expo"></div>
<div class="vf-side"><div class="vf-histo" id="vf-histo" aria-hidden="true"></div><div class="vf-info" id="vf-info" aria-live="polite"></div></div>
</div>
<div class="pick" id="pick" role="group" aria-label="{t['pick_label']}" hidden></div>
<div class="cards" id="cards"></div>
</div>
<div class="lab-more"><span>{t['lab_more']}</span>{lab_links}</div>
</div>
</section>

<section class="section has-deco" id="{ids[3]}">
{deco('arc-m', 'd-about-arc')}
<div class="wrap about">
<div class="portrait" id="portrait">{t['portrait']}</div>
<div class="about-text">
<div class="eyebrow">{t['about_eyebrow']}</div>
<h2>{t['about_hi']}<span data-set="name"></span>.</h2>
<p data-set="about"></p>
<ul class="services">{services}</ul>
</div>
</div>
</section>

<section class="contact has-deco" id="{ids[4]}">
{deco('arc-f', 'd-contact-arc')}
<div class="wrap">
<div class="contact-top">
<div><div class="eyebrow">{t['contact_eyebrow']}</div><h2>{t['contact_h2']}</h2></div>
<div class="contact-side">
<a class="btn btn-dark" id="mail" href="mailto:">{t['mail_ph']}</a>
<div class="socials">
<a id="s-youtube" href="#" aria-label="YouTube" rel="noopener" target="_blank" hidden>{ICON['youtube']}</a>
<a id="s-instagram" href="#" aria-label="Instagram" rel="noopener" target="_blank" hidden>{ICON['instagram']}</a>
<a id="s-pinterest" href="#" aria-label="Pinterest" rel="noopener" target="_blank" hidden>{ICON['pinterest']}</a>
</div>
</div>
</div>
{footer_links(lang, 'home', alt)}
</div>
</section>

</main>
{YEAR_JS}</body>
</html>
"""


# ---------------------------------------------------------------- Albumseite
def album(lang):
    t = T[lang]
    work = "#work" if lang == "en" else "#arbeiten"
    back = URL[lang]["home"] + work
    return head(lang, f"{t['album_label']} – {SITE}", t["desc"], "album", "album") + header(lang, "album", "album") + f"""<main id="main" data-album-page>

<section class="album-hero has-deco">
{deco('scale-v', 'd-edge-l')}{deco('af', 'd-album-af')}
<div class="wrap">
<a class="back" href="{back}">{ICON['back']}{t['album_back']}</a>
<div class="eyebrow" id="album-meta">{t['album_label']}</div>
<h1 id="album-title">{t['album_label']}</h1>
<p id="album-text" hidden></p>
</div>
</section>

<section class="section album-body has-deco">
{deco('ring', 'd-alb-ring')}{deco('arc-f', 'd-alb-arc')}{deco('scale-v', 'd-edge-l')}
<div class="wrap">
<div class="av" id="av" hidden>
<div class="vf-counter av-counter" id="av-counter" aria-hidden="true"></div>
<div class="av-frame vf-frame"><i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i>
<button class="av-photo" id="av-photo" type="button" aria-label="{t['album_full']}"><img id="av-img" alt=""></button>
<button class="av-nav av-prev" type="button" aria-label="{'Previous photo' if lang == 'en' else 'Vorheriges Foto'}">‹</button>
<button class="av-nav av-next" type="button" aria-label="{'Next photo' if lang == 'en' else 'Nächstes Foto'}">›</button>
</div>
<div class="av-info"><div class="vf-row" id="av-data"></div><p class="av-cap" id="av-cap" aria-live="polite"></p></div>
</div>
<div class="strip" id="album-photos" aria-label="{t['album_strip']}"></div>
</div>
</section>

<section class="contact">
<div class="wrap">
<div class="contact-top">
<h2>{t['contact_h2']}</h2>
<a class="btn btn-dark" href="{URL[lang]['home']}{'#contact' if lang == 'en' else '#kontakt'}">{t['cta']} {ICON['arrow']}</a>
</div>
{footer_links(lang, 'album', 'album')}
</div>
</section>

<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="{t['album_label']}">
{deco('tilt', 'd-lb-tilt')}{deco('arc-mm', 'd-lb-arc')}
<div class="vf-status lb-status" id="lb-status" aria-hidden="true"></div>
<div class="lb-stage"><figure><span class="lb-shot"><img alt=""><span class="cmp-af lb-af" aria-hidden="true"><i></i></span></span><figcaption></figcaption></figure></div>
<div class="vf-expo lb-expo" id="lb-expo" aria-hidden="true"></div>
<div class="lb-side"><div class="vf-histo" id="lb-histo" aria-hidden="true"></div></div>
<button class="lb-close" type="button" aria-label="{'Close' if lang == 'en' else 'Schließen'}">×</button>
<button class="lb-prev" type="button" aria-label="{'Previous photo' if lang == 'en' else 'Vorheriges Foto'}">‹</button>
<button class="lb-next" type="button" aria-label="{'Next photo' if lang == 'en' else 'Nächstes Foto'}">›</button>
</div>

</main>
{YEAR_JS}</body>
</html>
"""


# ---------------------------------------------------------------- Praxis / Guide
GUIDE = {
    "en": {
        "title": "Guide", "eyebrow": "Guide · In practice", "h1": "Know your<br><em>settings.</em>",
        "p": "Short explanations and tips from my test series – worked through with the LUMIX G70 and the 14–42 mm kit lens. The values under each card match exactly this gear.",
        "toc_label": "Topics", "cheat_link": "Cheat sheet",
        "tri_eyebrow": "The basics", "tri_h2": "The exposure triangle",
        "tri_p": "Three controls set the brightness. Each one adds light – and each one has a side effect. Change one, and you balance it with another.",
        "tri": [("Aperture", "f/8 → f/3.5 = more light", "Side effect: less depth of field – the background goes soft."),
                ("Shutter speed", "1/500 s → 1/60 s = more light", "Side effect: motion blur and camera shake."),
                ("ISO", "ISO 200 → ISO 1600 = more light", "Side effect: more noise, less detail in highlights and shadows.")],
        "ap_label": "Aperture openings from f/3.5 to f/22 compared by size",
        "ap_p": "The higher the f-number, the smaller the opening. Every full stop (f/5.6 → f/8) halves the light – balance it with twice the exposure time or twice the ISO.",
        "tip": "TIP",
        "topics": [
            ("aperture", "EXPOSURE", "Aperture", "The aperture is the opening in the lens. A small f-number (f/3.5) means a wide opening: more light, shallow depth of field, soft background. A large f-number (f/11) means a small opening: less light, more of the scene in focus.",
             "The kit lens is sharpest between f/4 and f/6. From around f/11, diffraction softens the image again – use f/22 only when you really need maximum depth of field.", "G70 · f/3.5 (14 mm) – f/5.6 (42 mm) · smallest aperture f/22"),
            ("focal", "LENS", "Focal length", "Focal length sets the angle of view. Wide angle shows a lot of the surroundings and stresses closeness and depth. Telephoto brings things closer and seems to pull the background towards your subject.",
             "Think full frame: on the G70’s Micro Four Thirds sensor, 14–42 mm looks like 28–84 mm. 25 mm is roughly the classic 50 mm “normal” lens – perfect for practice.", "G70 · markings 14 · 18 · 25 · 35 · 42 mm (FF 28–84 mm)"),
            ("zoom", "LENS", "Zoom", "Standing still and zooming only crops tighter. Perspective changes when you move: close up at 14 mm or far away at 42 mm gives two completely different pictures of the same subject.",
             "Zooming in makes the widest opening smaller. Choose your position and focal length first, then adjust shutter speed or ISO for exposure.", "G70 · 14 → 42 mm · widest aperture f/3.5 → f/5.6"),
            ("iso", "EXPOSURE", "ISO", "ISO amplifies the sensor’s signal. Higher values make the image brighter but add visible noise and lose detail in bright and dark areas.",
             "Stay at ISO 200 whenever you can. Auto ISO helps when the light changes quickly – on the G70 the automatic mode goes no higher than ISO 3200.", "G70 · ISO 200–25600 · extended from 100 · Auto ISO up to 3200"),
            ("shutter", "EXPOSURE", "Shutter speed", "Shutter speed decides how motion looks: fast speeds freeze it, slow speeds blur it – lovely for flowing water, light trails or panning shots.",
             "Handheld rule of thumb: 1/(2 × focal length), so about 1/100 s at 42 mm. The stabiliser buys you margin but won’t stop subject movement. Use the mechanical shutter for moving subjects.", "G70 · mechanical 60 s – 1/4000 s · electronic 1 s – 1/16000 s"),
            ("wb", "COLOUR", "White balance", "White balance defines what counts as neutral. Set a low Kelvin value and the image turns cooler; a high value makes it warmer.",
             "For a series, fix the white balance instead of AWB – otherwise colours drift from frame to frame. Shooting RAW gives you full freedom later in editing.", "G70 · AWB · Daylight · Cloudy · Shade · Incandescent · Flash · 2500–10000 K"),
            ("composition", "DESIGN", "Composition", "Good pictures guide the eye. The rule of thirds, leading lines, a clear foreground and deliberate empty space give an image structure and calm.",
             "Before you press the shutter, trace the edges: what pokes into the frame, what gets cut off? Keep the horizon straight – and when in doubt, take one step closer.", "Exercise · shoot only at 25 mm for one week"),
            ("landscape", "GENRE", "Landscape", "Lots of depth of field, a steady camera and good light. The time just after sunrise and before sunset gives soft, warm side light.",
             "14–18 mm, f/5.6 to f/8, ISO 200 and a tripod. Bring something interesting into the foreground – it adds depth. A polariser deepens the sky and cuts reflections.", "G70 · 14 mm · f/8 · ISO 200 · AFS · 46 mm filter thread"),
            ("portrait", "GENRE", "Portrait", "A calm background draws the eye to the face. You get there with a long focal length, a wide aperture and as much distance as possible between person and background.",
             "42 mm at f/5.6, close to the person, background far away. Focus on the nearest eye. Soft light – shade, clouds, a window – is kinder than harsh sun.", "G70 · 42 mm (FF 84 mm) · f/5.6 · 1/250 s · AFS"),
            ("closeup", "GENRE", "Close-up", "The kit lens isn’t a macro, but it gets surprisingly close. Leaves, textures or products work well when you use the shortest focusing distance.",
             "At 42 mm and 0.3 m from the sensor you get the largest reproduction ratio. Depth of field gets very thin – use f/5.6 to f/8 and fine-tune focus manually.", "G70 · minimum focus 0.2 m (14 mm) / 0.3 m (42 mm) · max. 0.17x · MF"),
        ],
        "cheat_eyebrow": "Cheat sheet", "cheat_h2": "Starting values by situation",
        "cheat_p": "Starting points, not rules. Fine-tune from here with exposure compensation and a look at the histogram.",
        "cols": ["SITUATION", "FOCAL LENGTH", "APERTURE", "SHUTTER", "ISO", "FOCUS"],
        "rows": [("Landscape", "14–18 mm", "f/5.6–f/8", "1/125 s or tripod", "200", "AFS"),
                 ("Portrait", "42 mm", "f/5.6", "1/250 s", "200–800", "AFS"),
                 ("Street", "18–25 mm", "f/5.6", "1/500 s", "Auto (≤ 3200)", "AFF"),
                 ("Sport & motion", "35–42 mm", "f/5.6", "1/1000 s", "Auto (≤ 3200)", "AFC"),
                 ("Panning", "25–42 mm", "f/8", "1/30 s", "200", "AFC"),
                 ("Night on a tripod", "14 mm", "f/5.6", "2–30 s", "200", "MF"),
                 ("Close-up", "42 mm", "f/5.6–f/8", "1/250 s", "200–800", "MF")],
        "cta_h2": "Theory is good.<br>Test series are better.", "cta_btn": "Visit the Lab", "cta_href": "/#lab",
        "desc": "Aperture, focal length, ISO, composition and more – explained with the LUMIX G70 and the 14–42 mm kit lens.",
    },
    "de": {
        "title": "Praxis", "eyebrow": "Praxis · Anwendung", "h1": "Einstellungen<br><em>verstehen.</em>",
        "p": "Kurze Erklärungen und Tipps aus meinen Testreihen – durchgespielt mit der LUMIX G70 und dem Kit-Objektiv 14–42 mm. Die Werte unter jeder Karte passen genau zu dieser Ausrüstung.",
        "toc_label": "Themen", "cheat_link": "Spickzettel",
        "tri_eyebrow": "Grundlage", "tri_h2": "Das Belichtungsdreieck",
        "tri_p": "Drei Regler bestimmen die Helligkeit. Jeder bringt Licht – und jeder hat eine Nebenwirkung. Wer einen Regler verstellt, gleicht mit einem anderen aus.",
        "tri": [("Blende", "f/8 → f/3.5 = mehr Licht", "Nebenwirkung: weniger Schärfentiefe – der Hintergrund wird unscharf."),
                ("Verschlusszeit", "1/500 s → 1/60 s = mehr Licht", "Nebenwirkung: Bewegungs- und Verwacklungsunschärfe."),
                ("ISO", "ISO 200 → ISO 1600 = mehr Licht", "Nebenwirkung: mehr Bildrauschen, weniger Details in Lichtern und Schatten.")],
        "ap_label": "Blendenöffnungen von f/3.5 bis f/22 im Größenvergleich",
        "ap_p": "Je größer die Blendenzahl, desto kleiner die Öffnung. Jede ganze Blendenstufe (f/5.6 → f/8) halbiert das Licht – das gleichst du mit doppelter Belichtungszeit oder doppeltem ISO aus.",
        "tip": "TIPP",
        "topics": [
            ("blende", "BELICHTUNG", "Blende", "Die Blende ist die Öffnung im Objektiv. Kleine Blendenzahl (f/3.5) heißt große Öffnung: mehr Licht, wenig Schärfentiefe, weicher Hintergrund. Große Blendenzahl (f/11) heißt kleine Öffnung: weniger Licht, mehr Bereich scharf.",
             "Am schärfsten zeichnet das Kit-Objektiv zwischen f/4 und f/6. Ab etwa f/11 macht Beugung das Bild wieder weicher – f/22 nur, wenn du wirklich maximale Schärfentiefe brauchst.", "G70 · f/3.5 (14 mm) – f/5.6 (42 mm) · kleinste Blende f/22"),
            ("brennweite", "OBJEKTIV", "Brennweite", "Die Brennweite bestimmt den Bildwinkel. Weitwinkel zeigt viel Umgebung und betont Nähe und Tiefe. Tele holt heran und lässt den Hintergrund scheinbar näher an das Motiv rücken.",
             "Denk in Kleinbild: Am Micro-Four-Thirds-Sensor der G70 wirken 14–42 mm wie 28–84 mm. 25 mm entspricht ungefähr dem klassischen 50-mm-Normalobjektiv – ideal zum Üben.", "G70 · Markierungen 14 · 18 · 25 · 35 · 42 mm (KB 28–84 mm)"),
            ("zoom", "OBJEKTIV", "Zoom", "Wer stehen bleibt und zoomt, schneidet nur enger zu. Die Perspektive ändert sich erst, wenn du dich bewegst: nah ran mit 14 mm oder weit weg mit 42 mm ergibt bei gleichem Motiv zwei völlig verschiedene Bilder.",
             "Beim Heranzoomen wird die größte Öffnung kleiner. Erst Standpunkt und Brennweite wählen, dann Zeit oder ISO für die Belichtung nachziehen.", "G70 · 14 → 42 mm · Offenblende f/3.5 → f/5.6"),
            ("iso", "BELICHTUNG", "ISO", "ISO verstärkt das Signal des Sensors. Höhere Werte machen das Bild heller, bringen aber sichtbares Rauschen und weniger Zeichnung in hellen und dunklen Bereichen.",
             "So oft wie möglich bei ISO 200 bleiben. Auto-ISO ist praktisch, wenn das Licht schnell wechselt – die Automatik der G70 geht höchstens bis ISO 3200.", "G70 · ISO 200–25600 · erweitert ab 100 · Auto-ISO bis 3200"),
            ("zeit", "BELICHTUNG", "Verschlusszeit", "Die Verschlusszeit entscheidet über Bewegung: Kurze Zeiten frieren ein, lange Zeiten lassen verwischen – schön für fließendes Wasser, Lichtspuren oder Mitzieher.",
             "Aus der Hand gilt als Faustregel 1/(2 × Brennweite), bei 42 mm also etwa 1/100 s. Der Bildstabilisator gibt Reserven, stoppt aber keine Motivbewegung. Bei bewegten Motiven den mechanischen Verschluss nutzen.", "G70 · mechanisch 60 s – 1/4000 s · elektronisch 1 s – 1/16000 s"),
            ("weiss", "FARBE", "Weißabgleich", "Der Weißabgleich legt fest, was als neutral gilt. Stellst du einen niedrigen Kelvinwert ein, wird das Bild kühler; ein hoher Wert macht es wärmer.",
             "Für Serien den Weißabgleich fest einstellen statt AWB – sonst schwanken die Farben von Bild zu Bild. In RAW hast du später in der Bearbeitung volle Freiheit.", "G70 · AWB · Tageslicht · Bewölkt · Schatten · Glühlampe · Blitz · 2500–10000 K"),
            ("komposition", "GESTALTUNG", "Komposition", "Gute Bilder führen den Blick. Drittelregel, führende Linien, ein klarer Vordergrund und bewusst freie Fläche geben dem Bild Struktur und Ruhe.",
             "Vor dem Auslösen einmal die Ränder abfahren: Was ragt ins Bild, was wird angeschnitten? Horizont gerade halten und im Zweifel einen Schritt näher gehen.", "Übung · eine Woche nur mit 25 mm fotografieren"),
            ("landschaft", "GENRE", "Landschaft", "Viel Schärfentiefe, eine ruhige Kamera und gutes Licht. Die Zeit kurz nach Sonnenaufgang und vor Sonnenuntergang gibt weiches, warmes Seitenlicht.",
             "14–18 mm, f/5.6 bis f/8, ISO 200 und ein Stativ. Hol etwas Interessantes in den Vordergrund – das gibt Tiefe. Ein Polfilter macht den Himmel satter und nimmt Spiegelungen.", "G70 · 14 mm · f/8 · ISO 200 · AFS · Filtergewinde 46 mm"),
            ("portrait", "GENRE", "Portrait", "Ein ruhiger Hintergrund lenkt den Blick aufs Gesicht. Das schaffst du mit langer Brennweite, offener Blende und möglichst viel Abstand zwischen Person und Hintergrund.",
             "42 mm bei f/5.6, nah an die Person, Hintergrund weit weg. Scharfstellen auf das vordere Auge. Weiches Licht – Schatten, Wolken, ein Fenster – schmeichelt mehr als pralle Sonne.", "G70 · 42 mm (KB 84 mm) · f/5.6 · 1/250 s · AFS"),
            ("nah", "GENRE", "Nahaufnahme", "Das Kit-Objektiv ist kein Makro, kommt aber erstaunlich nah heran. Blätter, Texturen oder Produkte funktionieren gut, wenn du den kürzesten Abstand ausnutzt.",
             "Bei 42 mm und 0,3 m Abstand zum Sensor bekommst du den größten Abbildungsmaßstab. Die Schärfentiefe ist dann sehr knapp – lieber f/5.6 bis f/8 und manuell feinfokussieren.", "G70 · Naheinstellgrenze 0,2 m (14 mm) / 0,3 m (42 mm) · max. 0,17x · MF"),
        ],
        "cheat_eyebrow": "Spickzettel", "cheat_h2": "Startwerte nach Situation",
        "cheat_p": "Ausgangspunkte, keine Gesetze. Von hier aus mit der Belichtungskorrektur und einem Blick aufs Histogramm feinjustieren.",
        "cols": ["SITUATION", "BRENNWEITE", "BLENDE", "ZEIT", "ISO", "FOKUS"],
        "rows": [("Landschaft", "14–18 mm", "f/5.6–f/8", "1/125 s oder Stativ", "200", "AFS"),
                 ("Portrait", "42 mm", "f/5.6", "1/250 s", "200–800", "AFS"),
                 ("Street", "18–25 mm", "f/5.6", "1/500 s", "Auto (≤ 3200)", "AFF"),
                 ("Sport & Bewegung", "35–42 mm", "f/5.6", "1/1000 s", "Auto (≤ 3200)", "AFC"),
                 ("Mitzieher", "25–42 mm", "f/8", "1/30 s", "200", "AFC"),
                 ("Nacht mit Stativ", "14 mm", "f/5.6", "2–30 s", "200", "MF"),
                 ("Nahaufnahme", "42 mm", "f/5.6–f/8", "1/250 s", "200–800", "MF")],
        "cta_h2": "Theorie ist gut.<br>Testreihen sind besser.", "cta_btn": "Zum Labor", "cta_href": "/de/#labor",
        "desc": "Blende, Brennweite, ISO, Komposition und mehr – erklärt mit der LUMIX G70 und dem Kit-Objektiv 14–42 mm.",
    },
}


def guide(lang):
    g, t = GUIDE[lang], T[lang]
    toc = "".join(f'<a href="#{tid}">{esc(title)}</a>' for tid, _, title, *_ in g["topics"])
    tri = "".join(f'<div class="tri"><h3>{a}</h3><div class="mono">{b}</div><p>{c}</p></div>' for a, b, c in g["tri"])
    topics = ""
    for i, (tid, cat, title, text, tip, gear) in enumerate(g["topics"], 1):
        topics += f"""<article class="topic" id="{tid}">
<div class="row"><span>{i:02d}</span><span>{cat}</span></div>
<h3>{esc(title)}</h3>
<p>{esc(text)}</p>
<div class="tip"><b>{g['tip']}</b><p>{esc(tip)}</p></div>
<div class="gear">{esc(gear)}</div>
</article>
"""
    head_cols = "".join(f'<th scope="col">{c}</th>' for c in g["cols"])
    rows = "".join("<tr><th scope=\"row\">" + esc(r[0]) + "</th>" + "".join(f"<td>{esc(c)}</td>" for c in r[1:]) + "</tr>" for r in g["rows"])
    circles = [(60, 40, "f/3.5"), (190, 25, "f/5.6"), (310, 17.5, "f/8"), (425, 12.7, "f/11"), (545, 6.4, "f/22")]
    svg = "".join(f'<circle cx="{x}" cy="50" r="{r}" fill="none" stroke-width="2"/><text x="{x}" y="118" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="13">{l}</text>' for x, r, l in circles)
    cheat_id = "cheatsheet" if lang == "en" else "spickzettel"
    return head(lang, f"{g['title']} – {SITE}", g["desc"], "guide", "guide") + header(lang, "guide", "guide") + f"""<main id="main">

<section class="guide-hero has-deco">
{deco('scale-v', 'd-edge-l')}{deco('arc-f', 'd-guide-arc')}
<div class="wrap">
<div class="top">
<div><div class="eyebrow">{g['eyebrow']}</div><h1>{g['h1']}</h1></div>
<p>{g['p']}</p>
</div>
<nav class="toc" aria-label="{g['toc_label']}">{toc}<a class="solid" href="#{cheat_id}">{g['cheat_link']}</a></nav>
</div>
</section>

<section class="panel">
<div class="wrap">
<div class="section-head">
<div class="titles"><div class="eyebrow">{g['tri_eyebrow']}</div><h2>{g['tri_h2']}</h2></div>
<p>{g['tri_p']}</p>
</div>
<div class="triangle">{tri}</div>
<div class="apertures">
<svg viewBox="0 0 620 130" role="img" aria-label="{g['ap_label']}">{svg}</svg>
<p>{g['ap_p']}</p>
</div>
</div>
</section>

<section class="section">
<div class="wrap topics">
{topics}</div>
</section>

<section class="section" id="{cheat_id}">
<div class="wrap">
<div class="section-head">
<div class="titles"><div class="eyebrow">{g['cheat_eyebrow']}</div><h2>{g['cheat_h2']}</h2></div>
<p>{g['cheat_p']}</p>
</div>
<div class="table-wrap"><table class="cheat"><thead><tr>{head_cols}</tr></thead><tbody>{rows}</tbody></table></div>
</div>
</section>

<section class="contact">
<div class="wrap">
<div class="contact-top">
<h2>{g['cta_h2']}</h2>
<a class="btn btn-dark" href="{g['cta_href']}">{g['cta_btn']} {ICON['arrow']}</a>
</div>
{footer_links(lang, 'guide', 'guide')}
</div>
</section>

</main>
{YEAR_JS}</body>
</html>
"""


# ---------------------------------------------------------------- Rechtstexte
LEGAL_META = {
    "impressum_de": {"lang": "de", "eyebrow": "Rechtliches", "h1": "Impressum", "numbered": False,
                     "note": ""},
    "imprint_en": {"lang": "en", "eyebrow": "Legal", "h1": "Legal Notice", "numbered": False,
                   "note": 'This is an English translation of the German <a href="/de/impressum/" lang="de">Impressum</a>. In case of any discrepancy, the German version prevails.'},
    "datenschutz_de": {"lang": "de", "eyebrow": "Rechtliches", "h1": "Datenschutz", "numbered": True, "note": ""},
    "privacy_en": {"lang": "en", "eyebrow": "Legal", "h1": "Privacy Policy", "numbered": True,
                   "note": 'This is an English translation of the German <a href="/de/datenschutz/" lang="de">Datenschutzerklärung</a>. In case of any discrepancy, the German version prevails.'},
}


def legal_sections(kind, data):
    """Erzeugt die Abschnitte – muss zu renderLegal() in main.js passen."""
    op = data["operator"]
    de = kind.endswith("_de")
    doc = data[kind]
    country = "Deutschland" if de else "Germany"
    addr = "\n".join(x for x in [op.get("name"), op.get("business"), op.get("street"), op.get("city"), country] if x)
    out = []

    def sec(title, text, style="", anchor=""):
        paras = "".join(f'<p class="lines">{esc(p.strip())}</p>' for p in str(text or "").split("\n\n") if p.strip())
        cls = f' class="{esc(style)}"' if style else ""
        aid = f' id="{esc(anchor)}"' if anchor else ""
        out.append(f"<section{cls}{aid}><h2>{esc(title)}</h2>{paras}</section>")

    if kind in ("impressum_de", "imprint_en"):
        sec("Angaben gemäß § 5 DDG" if de else "Information pursuant to § 5 DDG (German Digital Services Act)", addr, "box")
        sec("Kontakt" if de else "Contact",
            ("Telefon: " if de else "Phone: ") + (op.get("phone") or "") + "\n" + ("E-Mail: " if de else "Email: ") + (op.get("email") or ""))
        if op.get("vat_id"):
            sec("Umsatzsteuer-ID" if de else "VAT ID",
                ("Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: " if de else "VAT identification number pursuant to § 27a of the German VAT Act (UStG): ") + op["vat_id"])
        for x in doc.get("sections", []):
            sec(x.get("title", ""), x.get("text", ""), x.get("style", ""), x.get("anchor", ""))
    else:
        resp = "\n".join(x for x in [op.get("name"), op.get("business"), ", ".join(y for y in [op.get("street"), op.get("city"), country] if y), ("E-Mail: " if de else "Email: ") + (op.get("email") or "")] if x)
        sec("1. " + ("Verantwortlicher" if de else "Controller"), resp, "box")
        for n, x in enumerate(doc.get("sections", []), 2):
            sec(f"{n}. {x.get('title', '')}", x.get("text", ""), x.get("style", ""), x.get("anchor", ""))
    return "\n".join(out)


def legal_body(kind):
    data = json.loads(LEGAL_FILE.read_text(encoding="utf-8"))
    m, doc = LEGAL_META[kind], data[kind]
    de = m["lang"] == "de"
    updated = doc.get("updated")
    upd = f" · {'Stand' if de else 'As of'} {esc(updated)}" if updated else ""
    eyebrow = f'{m["eyebrow"]}<span data-legal-updated data-prefix=" · {"Stand" if de else "As of"} ">{upd}</span>'
    hidden = "" if doc.get("intro") else " hidden"
    intro = f'<p class="lead" data-legal-intro{hidden}>{esc(doc.get("intro", ""))}</p>'
    note = f'<p class="note">{m["note"]}</p>' if m["note"] else ""
    return f"""<div><div class="eyebrow">{eyebrow}</div><h1>{m['h1']}</h1>{intro}{note}</div>
<div class="legal-body" data-legal="{kind}">
{legal_sections(kind, data)}
</div>"""


def legal_page(lang, page, kind, title, desc):
    return head(lang, f"{title} – {SITE}", desc, page, page) + header(lang, page, page) + f"""<main id="main" class="wrap">
<div class="legal">
{legal_body(kind)}
</div>
</main>
<div class="plain-footer"><div class="wrap">{footer_links(lang, page, page)}</div></div>
{YEAR_JS}</body>
</html>
"""


def not_found():
    return head("en", f"Page not found – {SITE}", "Page not found", "home", "home") + header("en", "404", "home") + f"""<main id="main" class="wrap nf">
{deco('cross', 'd-nf-cross')}
<div class="legal">
<div><div class="eyebrow">404</div><h1>Out of frame.</h1>
<p class="lead">This page doesn’t exist (anymore). · Diese Seite gibt es nicht (mehr).</p></div>
<div class="hero-actions"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-ghost" href="/de/">Startseite</a></div>
</div>
</main>
</body>
</html>
"""


if __name__ == "__main__":
    print("Erzeuge Seiten:")
    write("/", home("en"))
    write("/de/", home("de"))
    write("/album/", album("en"))
    write("/de/album/", album("de"))
    write("/guide/", guide("en"))
    write("/de/praxis/", guide("de"))
    write("/legal-notice/", legal_page("en", "legal", "imprint_en", "Legal Notice", "Legal notice of TRVR GDCHLD Visuals."))
    write("/privacy/", legal_page("en", "privacy", "privacy_en", "Privacy Policy", "Privacy policy of TRVR GDCHLD Visuals."))
    write("/de/impressum/", legal_page("de", "legal", "impressum_de", "Impressum", "Impressum von TRVR GDCHLD Visuals."))
    write("/de/datenschutz/", legal_page("de", "privacy", "datenschutz_de", "Datenschutz", "Datenschutzerklärung von TRVR GDCHLD Visuals."))
    (ROOT / "404.html").write_text(not_found(), encoding="utf-8")
    print("   404.html\nFertig.")
