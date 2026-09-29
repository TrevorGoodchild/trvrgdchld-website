#!/usr/bin/env python3
"""Erzeugt die statischen HTML-Seiten (EN + DE) der Website.

Nur nötig, wenn sich Aufbau, feste Texte, Praxis-Inhalte oder Rechtstexte ändern.
Fotos, Motion-Projekte, Laborkarten und Einstellungen kommen zur Laufzeit aus
/content/*.json und werden im CMS unter /admin gepflegt.

Aufruf:  python3 tools/build.py
"""
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "TRVR GDCHLD Visuals"

# ---------------------------------------------------------------- Rechtliche Angaben
# Hier eintragen und das Skript neu ausführen.
LEGAL = {
    "name": "[Vorname Nachname]",
    "street": "[Straße Hausnummer]",
    "city": "[PLZ Ort]",
    "phone": "[Telefonnummer]",
    "email": "[deine@mail.de]",
    "vat_id": "",  # leer lassen, wenn keine USt-IdNr. vorhanden ist
}

# ---------------------------------------------------------------- Routen
URL = {
    "en": {"home": "/", "guide": "/guide/", "legal": "/legal-notice/", "privacy": "/privacy/"},
    "de": {"home": "/de/", "guide": "/de/praxis/", "legal": "/de/impressum/", "privacy": "/de/datenschutz/"},
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
        "menu": "Open menu",
        "nav": [("#work", "Photography"), ("#motion", "Motion"), ("#lab", "Lab"), ("#about", "About")],
        "guide": "Guide", "cta": "Start a project",
        "legal": "Legal notice", "privacy": "Privacy", "other_lang": "Deutsch", "home": "Back to home",
        "desc": "Photography and motion graphics by TRVR GDCHLD Visuals – from the first test series to the finished clip.",
        "hero_eyebrow": "Photography · Motion graphics · ", "city_key": "city",
        "hero_h1": 'Hold the light.<br>Shape the<br><em>motion.</em>',
        "hero_p": "Stills and motion graphics from a single studio – from the first test series to the finished clip.",
        "view_work": "View work", "est": "EST.", "logo_alt": "TG monogram",
        "specs": [("CAMERA", "LUMIX G70"), ("LENS", "14–42 mm · f/3.5–5.6"), ("MOTION", "DaVinci Resolve · Fusion")],
        "available": "AVAILABLE",
        "work_eyebrow": "01 — Photography", "work_h2": "Selected work", "filter_label": "Filter by category",
        "motion_eyebrow": "02 — Motion graphics", "motion_h2": "Images in motion",
        "motion_p": "Title sequences, UI animations and logo reveals – built in DaVinci Resolve Fusion.",
        "reel_btn": "Load and play showreel",
        "reel_note": 'Clicking loads the video from YouTube, which transfers data to YouTube – see the <a href="/privacy/#youtube">privacy policy</a>.',
        "lab_eyebrow": "03 — Lab", "lab_h2": "Every series starts<br>with a card.",
        "lab_p": "Before every test shot, I hold a card with the settings up to the lens. That way it stays clear what shutter speed, aperture, ISO and white balance do to a subject.",
        "lab_more": "More in the guide:", "lab_links": [("#aperture", "Aperture f/3.5–f/22"), ("#iso", "ISO 200–25600"), ("#wb", "White balance 2500–10000 K")],
        "about_eyebrow": "04 — About", "about_hi": "Hi, I’m ", "portrait": "[Portrait photo]",
        "services": [("Portrait & People", "Photo"), ("Logo animation", "Motion"), ("Product photography", "Photo"), ("Social reels", "Motion"), ("Event & Street", "Photo"), ("UI motion", "Motion")],
        "contact_eyebrow": "05 — Contact", "contact_h2": "Let’s put something<br>in the frame.", "mail_ph": "[your@email]",
    },
    "de": {
        "skip": "Zum Inhalt springen", "nav_label": "Hauptnavigation", "lang_label": "Sprache wählen",
        "menu": "Menü öffnen",
        "nav": [("#arbeiten", "Fotografie"), ("#motion", "Motion"), ("#labor", "Labor"), ("#ueber", "Über")],
        "guide": "Praxis", "cta": "Projekt anfragen",
        "legal": "Impressum", "privacy": "Datenschutz", "other_lang": "English", "home": "Zur Startseite",
        "desc": "Fotografie und Motion Graphics von TRVR GDCHLD Visuals – von der ersten Testreihe bis zum fertigen Clip.",
        "hero_eyebrow": "Fotografie · Motion Graphics · ", "city_key": "city",
        "hero_h1": 'Licht halten.<br>Bewegung<br><em>gestalten.</em>',
        "hero_p": "Stille Bilder und bewegte Grafik aus einer Hand – von der ersten Testreihe bis zum fertigen Motion-Clip.",
        "view_work": "Arbeiten ansehen", "est": "SEIT", "logo_alt": "TG-Monogramm",
        "specs": [("KAMERA", "LUMIX G70"), ("OBJEKTIV", "14–42 mm · f/3.5–5.6"), ("MOTION", "DaVinci Resolve · Fusion")],
        "available": "VERFÜGBAR",
        "work_eyebrow": "01 — Fotografie", "work_h2": "Ausgewählte Bilder", "filter_label": "Nach Kategorie filtern",
        "motion_eyebrow": "02 — Motion Graphics", "motion_h2": "Bilder in Bewegung",
        "motion_p": "Titelsequenzen, UI-Animationen und Logo-Reveals – gebaut in DaVinci Resolve Fusion.",
        "reel_btn": "Showreel laden und abspielen",
        "reel_note": 'Mit dem Klick wird das Video von YouTube geladen. Dabei werden Daten an YouTube übertragen – mehr dazu im <a href="/de/datenschutz/#youtube">Datenschutz</a>.',
        "lab_eyebrow": "03 — Labor", "lab_h2": "Jede Serie beginnt<br>mit einer Karte.",
        "lab_p": "Vor jedem Testbild halte ich eine Karte mit den Einstellungen ins Bild. So bleibt nachvollziehbar, was Verschlusszeit, Blende, ISO und Weißabgleich mit einem Motiv machen.",
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
<a class="brand" href="{home}"><img src="/assets/img/logo.png" alt="" width="58" height="40"><span class="brand-name"><b>TRVR GDCHLD</b><span>VISUALS</span></span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="{t['menu']}">{ICON['menu']}</button>
<nav class="nav" id="nav" aria-label="{t['nav_label']}">
{links}
<a href="{u['guide']}"{guide_cur}>{t['guide']}</a>
<a class="btn btn-primary" href="{pfx}{contact}">{t['cta']}</a>
<div class="lang" role="group" aria-label="{t['lang_label']}"><a href="{en_href}" lang="en"{en_cur}>EN</a><a href="{de_href}" lang="de"{de_cur}>DE</a></div>
</nav>
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


# ---------------------------------------------------------------- Startseite
def home(lang):
    t = T[lang]
    ids = {"en": ("work", "motion", "lab", "about", "contact"), "de": ("arbeiten", "motion", "labor", "ueber", "kontakt")}[lang]
    specs = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in t["specs"])
    services = "".join(f"<li>{esc(a)}<span>{esc(b)}</span></li>" for a, b in t["services"])
    lab_links = "".join(f'<a href="{URL[lang]["guide"]}{h}">{esc(n)}</a>' for h, n in t["lab_links"])
    alt = "home"
    return head(lang, f"{SITE} – {'Photography & Motion' if lang == 'en' else 'Fotografie & Motion'}", t["desc"], "home", alt) + header(lang, "home", alt) + f"""<main id="main">

<section class="hero" id="top">
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
<img src="/assets/img/logo.png" alt="{t['logo_alt']}" width="640" height="442">
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
<div class="photo-grid" id="photo-grid"></div>
</div>
</section>

<section class="panel" id="{ids[1]}">
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
<div class="projects" id="projects"></div>
</div>
</section>

<section class="section" id="{ids[2]}">
<div class="wrap">
<div class="section-head">
<div class="titles"><div class="eyebrow">{t['lab_eyebrow']}</div><h2>{t['lab_h2']}</h2></div>
<p>{t['lab_p']}</p>
</div>
<div class="cards" id="cards"></div>
<div class="lab-more"><span>{t['lab_more']}</span>{lab_links}</div>
</div>
</section>

<section class="section" id="{ids[3]}">
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

<section class="contact" id="{ids[4]}">
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
    svg = "".join(f'<circle cx="{x}" cy="50" r="{r}" fill="none" stroke="#F4B98E" stroke-width="2"/><text x="{x}" y="118" text-anchor="middle" fill="#BFA9B4" font-family="JetBrains Mono, monospace" font-size="13">{l}</text>' for x, r, l in circles)
    cheat_id = "cheatsheet" if lang == "en" else "spickzettel"
    return head(lang, f"{g['title']} – {SITE}", g["desc"], "guide", "guide") + header(lang, "guide", "guide") + f"""<main id="main">

<section class="guide-hero">
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
def lines(*xs):
    return "\n".join(x for x in xs if x)


def legal_page(lang, page, body_html, title, desc):
    t = T[lang]
    return head(lang, f"{title} – {SITE}", desc, page, page) + header(lang, page, page) + f"""<main id="main" class="wrap">
<div class="legal">
{body_html}
</div>
</main>
<div class="plain-footer"><div class="wrap">{footer_links(lang, page, page)}</div></div>
{YEAR_JS}</body>
</html>
"""


def impressum():
    L = LEGAL
    vat = f"""<section><h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: {esc(L['vat_id'])}</p></section>""" if L["vat_id"] else ""
    return f"""<div><div class="eyebrow">Rechtliches</div><h1>Impressum</h1></div>
<section class="box"><h2>Angaben gemäß § 5 DDG</h2><p class="lines">{esc(lines(L['name'], 'TRVR GDCHLD Visuals', L['street'], L['city'], 'Deutschland'))}</p></section>
<section><h2>Kontakt</h2><p class="lines">Telefon: {esc(L['phone'])}
E-Mail: {esc(L['email'])}</p></section>
{vat}
<section><h2>Verbraucherstreitbeilegung</h2><p>Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p></section>
<section><h2>Haftung für Inhalte und Links</h2><p>Die Inhalte dieser Seiten wurden mit Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte kann ich jedoch keine Gewähr übernehmen. Diese Website enthält Links zu externen Websites Dritter, auf deren Inhalte ich keinen Einfluss habe. Für diese fremden Inhalte ist stets der jeweilige Anbieter oder Betreiber verantwortlich. Werden mir Rechtsverletzungen bekannt, entferne ich entsprechende Inhalte oder Links umgehend.</p></section>
<section><h2>Urheberrecht</h2><p>Alle Fotografien, Videos, Animationen, Grafiken und Texte auf dieser Website sind urheberrechtlich geschützt. Jede Vervielfältigung, Bearbeitung, Verbreitung oder sonstige Verwertung außerhalb der Grenzen des Urheberrechts bedarf meiner vorherigen schriftlichen Zustimmung. Anfragen zur Lizenzierung richten Sie bitte an die oben genannte E-Mail-Adresse.</p></section>"""


def imprint():
    L = LEGAL
    vat = f"""<section><h2>VAT ID</h2><p>VAT identification number pursuant to § 27a of the German VAT Act (UStG): {esc(L['vat_id'])}</p></section>""" if L["vat_id"] else ""
    return f"""<div><div class="eyebrow">Legal</div><h1>Legal Notice</h1><p class="note">This is an English translation of the German <a href="/de/impressum/" lang="de">Impressum</a>. In case of any discrepancy, the German version prevails.</p></div>
<section class="box"><h2>Information pursuant to § 5 DDG (German Digital Services Act)</h2><p class="lines">{esc(lines(L['name'], 'TRVR GDCHLD Visuals', L['street'], L['city'], 'Germany'))}</p></section>
<section><h2>Contact</h2><p class="lines">Phone: {esc(L['phone'])}
Email: {esc(L['email'])}</p></section>
{vat}
<section><h2>Consumer dispute resolution</h2><p>I am neither willing nor obliged to take part in dispute resolution proceedings before a consumer arbitration board.</p></section>
<section><h2>Liability for content and links</h2><p>The content of these pages has been created with care. However, I cannot guarantee that it is accurate, complete or up to date. This website contains links to external third-party websites whose content I have no control over. The respective provider or operator is always responsible for that content. If I become aware of any legal violations, I will remove the content or links concerned immediately.</p></section>
<section><h2>Copyright</h2><p>All photographs, videos, animations, graphics and texts on this website are protected by copyright. Any reproduction, editing, distribution or other use beyond the limits of copyright law requires my prior written consent. Please send licensing requests to the email address above.</p></section>"""


def datenschutz():
    L = LEGAL
    return f"""<div><div class="eyebrow">Rechtliches · Stand September 2026</div><h1>Datenschutz</h1>
<p class="lead">Diese Website ist bewusst schlank gebaut: keine Cookies, keine Analyse- oder Tracking-Tools, keine Werbung. Personenbezogene Daten werden nur verarbeitet, soweit das für den Betrieb der Seite technisch nötig ist oder Sie mich von sich aus kontaktieren.</p></div>
<section class="box"><h2>1. Verantwortlicher</h2><p class="lines">{esc(lines(L['name'], 'TRVR GDCHLD Visuals', L['street'] + ', ' + L['city'] + ', Deutschland', 'E-Mail: ' + L['email']))}</p></section>
<section><h2>2. Hosting und Server-Logfiles</h2><p>Diese Website wird bei Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA gehostet und über deren Netzwerk ausgeliefert. Beim Aufruf der Seite werden automatisch technische Daten verarbeitet, die Ihr Browser übermittelt: IP-Adresse, Datum und Uhrzeit des Zugriffs, aufgerufene Seite, zuvor besuchte Seite (Referrer) sowie Browsertyp und Betriebssystem.</p>
<p>Diese Daten sind nötig, um die Website auszuliefern und vor Angriffen zu schützen. Rechtsgrundlage ist mein berechtigtes Interesse an einem sicheren und stabilen Betrieb (Art. 6 Abs. 1 lit. f DSGVO). Mit Cloudflare besteht ein Vertrag zur Auftragsverarbeitung. Cloudflare ist unter dem EU-US Data Privacy Framework zertifiziert; die Übermittlung in die USA stützt sich auf den Angemessenheitsbeschluss der EU-Kommission (Art. 45 DSGVO). Weitere Informationen: cloudflare.com/privacypolicy.</p></section>
<section><h2>3. Verschlüsselung</h2><p>Diese Seite nutzt aus Sicherheitsgründen eine SSL- bzw. TLS-Verschlüsselung. Eine verschlüsselte Verbindung erkennen Sie an „https://“ und dem Schloss-Symbol in der Adresszeile Ihres Browsers.</p></section>
<section><h2>4. Schriftarten</h2><p>Die auf dieser Website verwendeten Schriftarten sind lokal auf dem Server eingebunden. Beim Laden der Seite wird keine Verbindung zu Servern von Google oder anderen Schriftanbietern hergestellt.</p></section>
<section><h2>5. Kontakt per E-Mail</h2><p>Wenn Sie mir eine E-Mail schreiben, verarbeite ich die darin enthaltenen Angaben (z. B. Name, E-Mail-Adresse, Inhalt Ihrer Anfrage), um Ihr Anliegen zu bearbeiten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, wenn Ihre Anfrage mit einem Auftrag zusammenhängt, ansonsten mein berechtigtes Interesse an der Beantwortung (Art. 6 Abs. 1 lit. f DSGVO). Ihre Daten werden gelöscht, sobald Ihre Anfrage erledigt ist, sofern keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p></section>
<section id="youtube"><h2>6. Eingebettete Videos (YouTube)</h2><p>Für mein Showreel binde ich Videos der Plattform YouTube ein. Anbieter ist die Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland. Ich nutze dabei den erweiterten Datenschutzmodus (youtube-nocookie.com). Die Videos werden erst geladen, wenn Sie aktiv auf das Video klicken. Vorher werden keine Daten an YouTube übertragen.</p>
<p>Nach Ihrem Klick wird eine Verbindung zu den Servern von YouTube hergestellt. Dabei werden unter anderem Ihre IP-Adresse und Informationen zu Ihrem Gerät übermittelt, und YouTube kann Cookies oder vergleichbare Technologien einsetzen. Eine Übermittlung an die Google LLC in den USA ist möglich; Google LLC ist unter dem EU-US Data Privacy Framework zertifiziert. Rechtsgrundlage ist Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG), die Sie jederzeit mit Wirkung für die Zukunft widerrufen können. Weitere Informationen: policies.google.com/privacy.</p></section>
<section><h2>7. Links zu sozialen Netzwerken</h2><p>Auf dieser Website befinden sich einfache Links zu meinen Profilen bei YouTube, Instagram und Pinterest. Es handelt sich nicht um eingebettete Plugins: Solange Sie einen Link nicht anklicken, werden keine Daten an die jeweilige Plattform übertragen. Nach dem Klick gilt die Datenschutzerklärung des jeweiligen Anbieters:</p>
<p class="lines">YouTube: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland
Instagram: Meta Platforms Ireland Limited, Merrion Road, Dublin 4, D04 X2K5, Irland
Pinterest: Pinterest Europe Ltd., Palmerston House, 2nd Floor, Fenian Street, Dublin 2, Irland</p></section>
<section><h2>8. Ihre Rechte</h2><p>Sie haben jederzeit das Recht auf Auskunft über Ihre gespeicherten Daten (Art. 15 DSGVO), auf Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18) und Datenübertragbarkeit (Art. 20). Eine erteilte Einwilligung können Sie jederzeit widerrufen (Art. 7 Abs. 3 DSGVO). Wenden Sie sich dafür einfach per E-Mail an mich.</p>
<p>Außerdem haben Sie das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren (Art. 77 DSGVO), insbesondere in dem Bundesland oder EU-Staat Ihres Aufenthaltsorts.</p></section>
<section class="outline"><h2>9. Widerspruchsrecht</h2><p>Soweit ich Daten auf Grundlage meines berechtigten Interesses (Art. 6 Abs. 1 lit. f DSGVO) verarbeite, können Sie aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit Widerspruch gegen diese Verarbeitung einlegen (Art. 21 DSGVO).</p></section>"""


def privacy():
    L = LEGAL
    return f"""<div><div class="eyebrow">Legal · As of September 2026</div><h1>Privacy Policy</h1>
<p class="lead">This website is deliberately lean: no cookies, no analytics or tracking tools, no advertising. Personal data is only processed where this is technically necessary to run the site or when you contact me yourself.</p>
<p class="note">This is an English translation of the German <a href="/de/datenschutz/" lang="de">Datenschutzerklärung</a>. In case of any discrepancy, the German version prevails.</p></div>
<section class="box"><h2>1. Controller</h2><p class="lines">{esc(lines(L['name'], 'TRVR GDCHLD Visuals', L['street'] + ', ' + L['city'] + ', Germany', 'Email: ' + L['email']))}</p></section>
<section><h2>2. Hosting and server log files</h2><p>This website is hosted by Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA, and delivered through its network. When you visit the site, technical data sent by your browser is processed automatically: IP address, date and time of access, the page requested, the previously visited page (referrer), and browser type and operating system.</p>
<p>This data is needed to deliver the website and protect it against attacks. The legal basis is my legitimate interest in secure and stable operation (Art. 6(1)(f) GDPR). A data processing agreement is in place with Cloudflare. Cloudflare is certified under the EU-U.S. Data Privacy Framework; transfers to the USA are based on the European Commission’s adequacy decision (Art. 45 GDPR). More information: cloudflare.com/privacypolicy.</p></section>
<section><h2>3. Encryption</h2><p>For security reasons, this site uses SSL/TLS encryption. You can recognise an encrypted connection by “https://” and the padlock symbol in your browser’s address bar.</p></section>
<section><h2>4. Fonts</h2><p>The fonts used on this website are hosted locally on the server. No connection to Google or any other font provider is made when the page loads.</p></section>
<section><h2>5. Contact by email</h2><p>If you email me, I process the information it contains (e.g. name, email address, content of your enquiry) to handle your request. The legal basis is Art. 6(1)(b) GDPR where your enquiry relates to a commission, and otherwise my legitimate interest in replying (Art. 6(1)(f) GDPR). Your data is deleted once your enquiry has been dealt with, unless statutory retention obligations apply.</p></section>
<section id="youtube"><h2>6. Embedded videos (YouTube)</h2><p>For my showreel I embed videos from YouTube. The provider is Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Ireland. I use YouTube’s privacy-enhanced mode (youtube-nocookie.com). Videos are only loaded once you actively click on them. Before that, no data is transferred to YouTube.</p>
<p>After your click, a connection to YouTube’s servers is established. Among other things, your IP address and information about your device are transmitted, and YouTube may use cookies or similar technologies. Data may be transferred to Google LLC in the USA; Google LLC is certified under the EU-U.S. Data Privacy Framework. The legal basis is your consent (Art. 6(1)(a) GDPR, § 25(1) TDDDG), which you can withdraw at any time with effect for the future. More information: policies.google.com/privacy.</p></section>
<section><h2>7. Links to social networks</h2><p>This website contains simple links to my profiles on YouTube, Instagram and Pinterest. These are not embedded plugins: as long as you do not click a link, no data is transferred to the respective platform. After clicking, the privacy policy of the respective provider applies:</p>
<p class="lines">YouTube: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Ireland
Instagram: Meta Platforms Ireland Limited, Merrion Road, Dublin 4, D04 X2K5, Ireland
Pinterest: Pinterest Europe Ltd., Palmerston House, 2nd Floor, Fenian Street, Dublin 2, Ireland</p></section>
<section><h2>8. Your rights</h2><p>You have the right at any time to access your stored data (Art. 15 GDPR), and to rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18) and data portability (Art. 20). You can withdraw any consent you have given at any time (Art. 7(3) GDPR). Simply contact me by email.</p>
<p>You also have the right to lodge a complaint with a data protection supervisory authority (Art. 77 GDPR), in particular in the EU member state or German federal state where you live.</p></section>
<section class="outline"><h2>9. Right to object</h2><p>Where I process data on the basis of my legitimate interest (Art. 6(1)(f) GDPR), you may object to this processing at any time on grounds relating to your particular situation (Art. 21 GDPR).</p></section>"""


def not_found():
    return head("en", f"Page not found – {SITE}", "Page not found", "home", "home") + header("en", "404", "home") + f"""<main id="main" class="wrap">
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
    write("/guide/", guide("en"))
    write("/de/praxis/", guide("de"))
    write("/legal-notice/", legal_page("en", "legal", imprint(), "Legal Notice", "Legal notice of TRVR GDCHLD Visuals."))
    write("/privacy/", legal_page("en", "privacy", privacy(), "Privacy Policy", "Privacy policy of TRVR GDCHLD Visuals."))
    write("/de/impressum/", legal_page("de", "legal", impressum(), "Impressum", "Impressum von TRVR GDCHLD Visuals."))
    write("/de/datenschutz/", legal_page("de", "privacy", datenschutz(), "Datenschutz", "Datenschutzerklärung von TRVR GDCHLD Visuals."))
    (ROOT / "404.html").write_text(not_found(), encoding="utf-8")
    print("   404.html\nFertig.")
