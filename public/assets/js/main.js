/* TRVR GDCHLD Visuals – Seitenlogik
   Liest die Inhalte aus /content/*.json (dort pflegt das CMS die Daten)
   und baut Fotos, Motion-Projekte und Testreihen auf. */
(function () {
  "use strict";

  var lang = (document.documentElement.lang || "en").slice(0, 2) === "de" ? "de" : "en";
  var L = {
    en: {
      cats: { all: "All", portrait: "Portrait", street: "Street", landscape: "Landscape", product: "Product", event: "Event & Concert" },
      noPhotos: "No albums in this category yet.",
      photos: "photos", photo: "photo", openAlbum: "Open album", albumMissing: "This album could not be found.",
      emptyAlbum: "Photos for this album are coming soon.",
      playPlaylist: "Load and play playlist", noPlaylist: "This playlist will be available soon.", months: ["January","February","March","April","May","June","July","August","September","October","November","December"],
      watch: "Watch on YouTube",
      noReel: "The showreel will be available here soon.",
      series: "SERIES", photo_ph: "[PHOTO]",
      topics: { shutter: "Shutter speed", aperture: "Aperture", iso: "ISO", wb: "White balance", focal: "Focal length" },
      cmpLabel: "Divider between A and B", cmpHint: "Drag the line or use the arrow keys. Tap a card to change the image.",
      cmpText: function (p) { return p + " % A visible"; },
      pickFor: "Card sets", left: "left", right: "right", histo: "HISTOGRAM",
      evLabel: "Brightness B vs. A", evNone: "no comparison", ref: "Reference", cardLabel: function (v, side) { return v + (side ? " – shown " + side : ""); },
      menuOpen: "Open menu", menuClose: "Close menu",
      themeLight: "Switch to light theme", themeDark: "Switch to dark theme"
    },
    de: {
      cats: { all: "Alle", portrait: "Portrait", street: "Street", landscape: "Landschaft", product: "Produkt", event: "Event & Konzert" },
      noPhotos: "In dieser Kategorie gibt es noch keine Alben.",
      photos: "Fotos", photo: "Foto", openAlbum: "Album öffnen", albumMissing: "Dieses Album wurde nicht gefunden.",
      emptyAlbum: "Die Fotos zu diesem Album folgen bald.",
      playPlaylist: "Playlist laden und abspielen", noPlaylist: "Diese Playlist ist bald verfügbar.", months: ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],
      watch: "Auf YouTube ansehen",
      noReel: "Das Showreel ist hier bald zu sehen.",
      series: "SERIE", photo_ph: "[FOTO]",
      topics: { shutter: "Verschlusszeit", aperture: "Blende", iso: "ISO", wb: "Weißabgleich", focal: "Brennweite" },
      cmpLabel: "Trennlinie zwischen A und B", cmpHint: "Linie ziehen oder Pfeiltasten nutzen. Karte antippen wechselt das Bild.",
      cmpText: function (p) { return p + " % A sichtbar"; },
      pickFor: "Karte setzt", left: "links", right: "rechts", histo: "HISTOGRAMM",
      evLabel: "Helligkeit B zu A", evNone: "kein Vergleich", ref: "Referenz", cardLabel: function (v, side) { return v + (side ? " – angezeigt " + side : ""); },
      menuOpen: "Menü öffnen", menuClose: "Menü schließen",
      themeLight: "Helles Design aktivieren", themeDark: "Dunkles Design aktivieren"
    }
  }[lang];
  var TILE_COLORS = ["#3A2640", "#5A3440", "#6E3F32", "#4A2F45", "#33213A"];

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "text") n.textContent = attrs[k];
      else if (k === "class") n.className = attrs[k];
      else if (attrs[k] !== undefined && attrs[k] !== null) n.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }
  function pick(obj, key) {
    var v = obj[key + "_" + lang];
    if (v === undefined || v === "") v = obj[key + "_" + (lang === "de" ? "en" : "de")];
    if (v === undefined) v = obj[key];
    return v || "";
  }
  function getJSON(path) {
    return fetch(path, { cache: "no-cache" }).then(function (r) { if (!r.ok) throw new Error(path); return r.json(); });
  }
  function youtubeId(v) {
    if (!v) return "";
    var m = String(v).match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([A-Za-z0-9_-]{11})/);
    if (m) return m[1];
    return /^[A-Za-z0-9_-]{11}$/.test(v) ? v : "";
  }
  function safeUrl(u) { return /^https:\/\//i.test(u || "") ? u : ""; }

  /* Theme toggle (dark/light), stored only in this browser */
  var themeBtn = document.querySelector(".theme-btn");
  var themeMeta = document.querySelector('meta[name="theme-color"]');
  function applyTheme(mode, save) {
    var light = mode === "light";
    document.documentElement.dataset.theme = light ? "light" : "dark";
    if (themeMeta) themeMeta.content = light ? "#F6E7D8" : "#1C1220";
    if (themeBtn) {
      var label = light ? L.themeDark : L.themeLight;
      themeBtn.setAttribute("aria-pressed", light ? "true" : "false");
      themeBtn.setAttribute("aria-label", label);
      themeBtn.title = label;
    }
    if (save) { try { localStorage.setItem("theme", light ? "light" : "dark"); } catch (e) {} }
  }
  applyTheme(document.documentElement.dataset.theme === "light" ? "light" : "dark", false);
  if (themeBtn) themeBtn.addEventListener("click", function () {
    applyTheme(document.documentElement.dataset.theme === "light" ? "dark" : "light", true);
  });

  /* Mobile menu */
  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.getElementById("nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.setAttribute("aria-label", open ? L.menuClose : L.menuOpen);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); }
    });
  }

  /* Legal pages: refresh from /content/legal.json (edited in the CMS).
     Must match legal_sections() in tools/build.py. */
  var legalBox = document.querySelector("[data-legal]");
  if (legalBox) {
    getJSON("/content/legal.json").then(function (data) {
      var kind = legalBox.getAttribute("data-legal"), doc = data[kind], op = data.operator || {};
      if (!doc) return;
      var de = /_de$/.test(kind), country = de ? "Deutschland" : "Germany";
      var parts = [];
      function sec(title, text, style, anchor) {
        var s = el("section", { class: style || null, id: anchor || null }, [el("h2", { text: title })]);
        String(text || "").split("\n\n").forEach(function (p) {
          if (p.trim()) s.appendChild(el("p", { class: "lines", text: p.trim() }));
        });
        parts.push(s);
      }
      var list = doc.sections || [];
      if (kind === "impressum_de" || kind === "imprint_en") {
        sec(de ? "Angaben gemäß § 5 DDG" : "Information pursuant to § 5 DDG (German Digital Services Act)",
          [op.name, op.business, op.street, op.city, country].filter(Boolean).join("\n"), "box");
        sec(de ? "Kontakt" : "Contact", (de ? "Telefon: " : "Phone: ") + (op.phone || "") + "\n" + (de ? "E-Mail: " : "Email: ") + (op.email || ""));
        if (op.vat_id) sec(de ? "Umsatzsteuer-ID" : "VAT ID", (de ? "Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: " : "VAT identification number pursuant to § 27a of the German VAT Act (UStG): ") + op.vat_id);
        list.forEach(function (x) { sec(x.title || "", x.text, x.style, x.anchor); });
      } else {
        sec("1. " + (de ? "Verantwortlicher" : "Controller"),
          [op.name, op.business, [op.street, op.city, country].filter(Boolean).join(", "), (de ? "E-Mail: " : "Email: ") + (op.email || "")].filter(Boolean).join("\n"), "box");
        list.forEach(function (x, i) { sec((i + 2) + ". " + (x.title || ""), x.text, x.style, x.anchor); });
      }
      var upd = document.querySelector("[data-legal-updated]");
      if (upd) upd.textContent = doc.updated ? upd.getAttribute("data-prefix") + doc.updated : "";
      var intro = document.querySelector("[data-legal-intro]");
      if (intro) { intro.textContent = doc.intro || ""; intro.hidden = !doc.intro; }
      legalBox.textContent = "";
      parts.forEach(function (n) { legalBox.appendChild(n); });
      if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
    }).catch(function () {});
    return;
  }

  var albumBase = lang === "de" ? "/de/album/" : "/album/";
  function dateLabel(d) {
    var m = /^(\d{4})-(\d{2})/.exec(d || "");
    return m ? L.months[+m[2] - 1] + " " + m[1] : (d || "");
  }
  function specsOf(ph, fallbackCam) {
    return [ph.camera || fallbackCam, ph.focal, ph.aperture, ph.shutter, ph.iso].filter(Boolean).join(" · ");
  }

  /* Album page: /album/?a=slug */
  if (document.querySelector("[data-album-page]")) {
    // keep the album when switching language
    document.querySelectorAll('a[href="/album/"], a[href="/de/album/"]').forEach(function (a) { a.href = a.getAttribute("href") + location.search; });
    var slug = new URLSearchParams(location.search).get("a") || "";
    getJSON("/content/albums.json").then(function (data) {
      var al = (data.albums || []).filter(function (x) { return x.slug === slug; })[0];
      var titleEl = document.getElementById("album-title"), box = document.getElementById("album-photos");
      if (!al) { titleEl.textContent = L.albumMissing; return; }
      var title = pick(al, "title");
      titleEl.textContent = title;
      document.title = title + " – TRVR GDCHLD Visuals";
      var photos = al.photos || [];
      var meta = [L.cats[al.category] || al.category, dateLabel(al.date), al.place, photos.length + " " + (photos.length === 1 ? L.photo : L.photos)].filter(Boolean).join(" · ");
      document.getElementById("album-meta").textContent = meta;
      var txt = document.getElementById("album-text"), t = pick(al, "text");
      if (t) { txt.textContent = t; txt.hidden = false; }
      box.textContent = "";
      if (!photos.length) { box.appendChild(el("p", { class: "empty-note", text: L.emptyAlbum })); return; }
      photos.forEach(function (ph, i) {
        var specs = specsOf(ph, al.camera);
        var btn = el("button", { type: "button", class: "album-photo", "aria-label": (ph.caption || title) + " – " + (i + 1) + "/" + photos.length }, [
          el("img", { src: ph.image, alt: ph.alt || ph.caption || "", loading: i < 4 ? "eager" : "lazy", decoding: "async" })
        ]);
        btn.addEventListener("click", function () { openLightbox(i); });
        box.appendChild(el("figure", { class: "album-item" }, [btn,
          (ph.caption || specs) ? el("figcaption", null, [ph.caption ? el("b", { text: ph.caption }) : null, specs ? el("span", { text: specs }) : null]) : null]));
      });
      // Lightbox
      var lb = document.getElementById("lightbox"), img = lb.querySelector("img"), cap = lb.querySelector("figcaption"), cur = 0, lastFocus = null;
      function show(i) {
        cur = (i + photos.length) % photos.length;
        var ph = photos[cur];
        img.src = ph.image; img.alt = ph.alt || ph.caption || "";
        cap.textContent = [ph.caption, specsOf(ph, al.camera)].filter(Boolean).join("  ·  ");
        var cnt = document.getElementById("lb-count");
        if (cnt) cnt.innerHTML = "<b>" + String(cur + 1).padStart(2, "0") + "</b> / " + String(photos.length).padStart(2, "0");
      }
      function openLightbox(i) { lastFocus = document.activeElement; show(i); lb.hidden = false; document.body.style.overflow = "hidden"; lb.querySelector(".lb-close").focus(); }
      function close() { lb.hidden = true; document.body.style.overflow = ""; if (lastFocus) lastFocus.focus(); }
      lb.querySelector(".lb-close").addEventListener("click", close);
      lb.querySelector(".lb-prev").addEventListener("click", function () { show(cur - 1); });
      lb.querySelector(".lb-next").addEventListener("click", function () { show(cur + 1); });
      lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
      lb.addEventListener("keydown", function (e) {
        if (e.key === "Escape") close();
        else if (e.key === "ArrowLeft") show(cur - 1);
        else if (e.key === "ArrowRight") show(cur + 1);
      });
      var tx = null;
      lb.addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
      lb.addEventListener("touchend", function (e) { if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); tx = null; });
    }).catch(function () {});
    return;
  }

  /* Only the home page needs the rest */
  if (!document.getElementById("album-grid")) return;

  /* Settings */
  getJSON("/content/settings.json").then(function (s) {
    document.querySelectorAll("[data-set]").forEach(function (n) {
      var v = pick(s, n.getAttribute("data-set"));
      if (v) n.textContent = v;
    });
    document.querySelectorAll("[data-hide-empty]").forEach(function (n) {
      n.hidden = !pick(s, n.getAttribute("data-hide-empty"));
    });
    var mail = document.getElementById("mail");
    if (mail && s.email) { mail.href = "mailto:" + s.email; mail.textContent = s.email; }
    ["youtube", "instagram", "pinterest"].forEach(function (k) {
      var a = document.getElementById("s-" + k), url = safeUrl(s[k + "_url"]);
      if (a) { if (url) { a.href = url; a.hidden = false; } else a.hidden = true; }
    });
    var p = document.getElementById("portrait");
    if (p && s.portrait) { p.textContent = ""; p.appendChild(el("img", { src: s.portrait, alt: s.name || "", loading: "lazy" })); }
    setupReel(youtubeId(s.showreel_youtube_id));
  }).catch(function () { setupReel(""); });

  /* Showreel: loads YouTube only after a click (privacy) */
  function setupReel(id) {
    var btn = document.getElementById("reel-play"), box = document.getElementById("reel");
    if (!btn || !box) return;
    btn.addEventListener("click", function () {
      if (!id) { document.getElementById("reel-note").textContent = L.noReel; return; }
      box.appendChild(ytFrame("https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0", "Showreel"));
    });
  }
  function ytFrame(src, title) {
    return el("iframe", {
      src: src, title: title,
      allow: "autoplay; encrypted-media; picture-in-picture; fullscreen",
      allowfullscreen: "", referrerpolicy: "strict-origin-when-cross-origin"
    });
  }
  function playlistId(u) {
    var m = String(u || "").match(/[?&]list=([A-Za-z0-9_-]+)/);
    return m ? m[1] : (/^(PL|UU|OL|FL|LL)[A-Za-z0-9_-]{10,}$/.test(u || "") ? u : "");
  }

  /* Albums */
  var grid = document.getElementById("album-grid");
  var filterBox = document.getElementById("filters");
  getJSON("/content/albums.json").then(function (data) {
    var albums = data.albums || [];
    grid.textContent = "";
    var cats = ["all"];
    albums.forEach(function (al, i) {
      if (al.category && cats.indexOf(al.category) < 0) cats.push(al.category);
      var photos = al.photos || [];
      var cover = al.cover || (photos[0] && photos[0].image) || "";
      var thumb = el("div", { class: "album-cover" });
      if (cover) thumb.appendChild(el("img", { src: cover, alt: "", loading: "lazy", decoding: "async" }));
      else thumb.style.background = TILE_COLORS[i % TILE_COLORS.length];
      var meta = [L.cats[al.category] || al.category, dateLabel(al.date), photos.length + " " + (photos.length === 1 ? L.photo : L.photos)].filter(Boolean).join(" · ");
      grid.appendChild(el("a", { class: "album-card", href: albumBase + "?a=" + encodeURIComponent(al.slug || ""), "data-cat": al.category || "" }, [
        thumb,
        el("div", { class: "album-info" }, [el("span", { class: "album-meta", text: meta }), el("b", { text: pick(al, "title") })])
      ]));
    });
    var empty = el("p", { class: "empty-note", text: L.noPhotos }); empty.hidden = true; grid.appendChild(empty);
    filterBox.textContent = "";
    cats.forEach(function (c) {
      var b = el("button", { type: "button", class: "chip", "aria-pressed": c === "all" ? "true" : "false", text: L.cats[c] || c });
      b.addEventListener("click", function () {
        filterBox.querySelectorAll(".chip").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        var shown = 0;
        grid.querySelectorAll(".album-card").forEach(function (t) {
          var on = c === "all" || t.getAttribute("data-cat") === c;
          t.hidden = !on; if (on) shown++;
        });
        empty.hidden = shown > 0;
      });
      filterBox.appendChild(b);
    });
  }).catch(function () {});

  /* Playlists (YouTube, loaded only after a click) */
  getJSON("/content/playlists.json").then(function (data) {
    var box = document.getElementById("playlists");
    box.textContent = "";
    (data.playlists || []).forEach(function (pl, i) {
      var id = playlistId(pl.playlist_url), title = pick(pl, "title");
      var thumb = el("div", { class: "thumb pl-thumb" });
      if (pl.cover) thumb.appendChild(el("img", { src: pl.cover, alt: "", loading: "lazy" }));
      else thumb.style.background = TILE_COLORS[(i + 3) % TILE_COLORS.length];
      var play = el("button", { type: "button", class: "pl-play", "aria-label": L.playPlaylist + ": " + title }, []);
      play.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5l12 7-12 7z"/></svg>';
      thumb.appendChild(play);
      var note = el("p", { class: "pl-note", text: "" });
      play.addEventListener("click", function () {
        if (!id) { note.textContent = L.noPlaylist; return; }
        thumb.textContent = "";
        thumb.appendChild(ytFrame("https://www.youtube-nocookie.com/embed/videoseries?list=" + id + "&autoplay=1&rel=0", title));
      });
      var link = id ? "https://www.youtube.com/playlist?list=" + id : "";
      box.appendChild(el("article", { class: "project" }, [
        thumb,
        pl.tag ? el("div", { class: "tag", text: String(pl.tag).toUpperCase() }) : null,
        el("h3", { text: title }),
        pick(pl, "text") ? el("p", { text: pick(pl, "text") }) : null,
        note,
        link ? el("a", { href: link, rel: "noopener", target: "_blank", text: L.watch + " →" }) : null
      ]));
    });
  }).catch(function () {});

  /* Lab: test series with A/B comparison (viewfinder layout) */
  var testsBox = document.getElementById("tests");
  if (testsBox) getJSON("/content/lab.json").then(function (data) {
    var series = data.series;
    if (!Array.isArray(series)) {   // old format: { series: "A", cards: [...] }
      series = [{ id: data.series || "A", topic: "shutter", frames: (data.cards || []).map(function (c) {
        return { shutter: c.value, aperture: c.aperture, iso: c.iso, reference: c.highlight };
      }) }];
    }
    series = series.filter(function (sr) { return sr && (sr.frames || []).length; });
    if (!series.length) { testsBox.hidden = true; return; }

    var $ = function (id) { return document.getElementById(id); };
    var cmp = $("cmp"), cards = $("cards"), tabs = $("tests-tabs"), pickBox = $("pick");
    var state = { s: 0, a: 0, b: 1, pos: 50, side: "b" };
    var histCache = {};

    function num(v) { var m = String(v || "").replace(",", ".").match(/\d+(?:\.\d+)?/); return m ? parseFloat(m[0]) : NaN; }
    function secs(v) {
      var t = String(v || "").replace(",", ".").trim(), m = t.match(/^1\s*\/\s*(\d+(?:\.\d+)?)/);
      return m ? 1 / parseFloat(m[1]) : num(t);
    }
    function fAp(v) { var n = num(v); return isNaN(n) ? String(v || "") : "F" + n; }
    function fmt(f, key) {
      var v = f[key];
      if (!v) return "";
      if (key === "aperture") return fAp(v);
      if (key === "iso" && /^\d/.test(String(v))) return "ISO " + v;
      if (key === "focal" && /^\d+$/.test(String(v).trim())) return v + " mm";
      return String(v);
    }
    function big(sr, f) {
      var k = sr.topic || "shutter";
      if (k === "aperture") return f.aperture ? "f/" + num(f.aperture) : "–";
      if (k === "iso") return f.iso ? String(f.iso).replace(/^ISO\s*/i, "ISO ") : "–";
      return fmt(f, k) || "–";
    }
    function stops(a, b, fn, power) {
      var x = fn(a), y = fn(b);
      if (isNaN(x) && isNaN(y)) return 0;
      if (isNaN(x) || isNaN(y) || !x || !y) return NaN;
      return power * Math.log(y / x) / Math.LN2;
    }
    function evDiff(a, b) {
      return stops(a.shutter, b.shutter, secs, 1) + stops(a.iso, b.iso, num, 1) + stops(a.aperture, b.aperture, num, -2);
    }
    function evText(ev) {
      if (isNaN(ev)) return "–";
      var t = Math.round(ev * 3), w = Math.floor(Math.abs(t) / 3), r = Math.abs(t) % 3;
      if (t === 0) return "±0 EV";
      return (t > 0 ? "+" : "−") + (w || r ? (w ? w : "") + (r === 1 ? "⅓" : r === 2 ? "⅔" : "") : "0") + " EV";
    }
    function pad(n) { return String(n).padStart(2, "0"); }

    function media(sr, f, tag) {
      var box = el("div", { class: "cmp-img cmp-" + tag.toLowerCase() });
      if (f.image) {
        var img = el("img", { src: f.image, alt: tag + ": " + [fmt(f, "shutter"), fmt(f, "aperture"), fmt(f, "iso"), fmt(f, "wb"), fmt(f, "focal")].filter(Boolean).join(", "), decoding: "async", draggable: "false" });
        img.addEventListener("load", function () {
          if (tag === "A" && img.naturalWidth) {
            var r = img.naturalWidth / img.naturalHeight, lbl = [["4:3", 4 / 3], ["3:2", 1.5], ["16:9", 16 / 9], ["1:1", 1], ["3:4", 0.75], ["2:3", 2 / 3]]
              .reduce(function (b, x) { return Math.abs(x[1] - r) < Math.abs(b[1] - r) ? x : b; });
            cmp.style.aspectRatio = img.naturalWidth + " / " + img.naturalHeight;
            var rs = document.querySelector("#vf-status .ratio"); if (rs) rs.textContent = lbl[0];
          }
          drawHisto();
        });
        box.appendChild(img);
      } else {
        box.appendChild(el("div", { class: "cmp-ph" }, [el("span", { text: L.photo_ph }), el("b", { text: big(sr, f) })]));
      }
      box.appendChild(el("span", { class: "cmp-tag", text: tag + " · " + big(sr, f) }));
      return box;
    }

    /* Histogram (luminance) from the actual photos, drawn as lines A (faint) and B (accent) */
    function lum(src) {
      if (histCache[src]) return histCache[src];
      var img = cmp.querySelector('img[src="' + src.replace(/"/g, "") + '"]');
      if (!img || !img.complete || !img.naturalWidth) return null;
      try {
        var c = document.createElement("canvas"), w = 160, h = Math.max(1, Math.round(160 * img.naturalHeight / img.naturalWidth));
        c.width = w; c.height = h;
        var ctx = c.getContext("2d"); ctx.drawImage(img, 0, 0, w, h);
        var d = ctx.getImageData(0, 0, w, h).data, bins = new Array(48).fill(0);
        for (var i = 0; i < d.length; i += 4) bins[Math.min(47, Math.floor((0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]) / 256 * 48))]++;
        var sm = bins.map(function (_, i) { var t = 0, n = 0; for (var k = -2; k <= 2; k++) if (bins[i + k] !== undefined) { t += bins[i + k]; n++; } return t / n; });
        var mx = Math.max.apply(null, sm) || 1;
        return (histCache[src] = sm.map(function (v) { return v / mx; }));
      } catch (e) { return null; }
    }
    function line(h, cls) {
      return '<polyline class="' + cls + '" points="' + h.map(function (v, i) { return (12 + i * 216 / 47).toFixed(1) + "," + (104 - v * 80).toFixed(1); }).join(" ") + '"/>';
    }
    function drawHisto() {
      var sr = series[state.s], fa = sr.frames[state.a], fb = sr.frames[state.b];
      var ha = fa.image ? lum(fa.image) : null, hb = fb.image ? lum(fb.image) : null;
      var svg = '<svg viewBox="0 0 240 120" preserveAspectRatio="none" aria-hidden="true"><line class="g" x1="66" y1="16" x2="66" y2="104"/><line class="g" x1="120" y1="16" x2="120" y2="104"/><line class="g" x1="174" y1="16" x2="174" y2="104"/><line class="base" x1="12" y1="104" x2="228" y2="104"/>';
      if (ha) svg += line(ha, "ha");
      if (hb) svg += line(hb, "hb");
      if (!ha && !hb) svg += '<path class="ha" d="M12 103 C 50 103, 60 40, 86 40 S 118 92, 132 92 S 150 62, 160 62 S 176 103, 228 103"/>';
      $("vf-histo").innerHTML = '<span class="vf-histo-l">' + L.histo + '</span><span class="vf-histo-k"><i class="ka"></i>A <i class="kb"></i>B</span>' + svg + "</svg>";
    }

    function setPos(p) {
      state.pos = Math.max(0, Math.min(100, Math.round(p)));
      cmp.style.setProperty("--pos", state.pos + "%");
      var h = cmp.querySelector(".cmp-handle");
      if (h) { h.setAttribute("aria-valuenow", state.pos); h.setAttribute("aria-valuetext", L.cmpText(state.pos)); }
    }

    function renderView() {
      var sr = series[state.s], fa = sr.frames[state.a], fb = sr.frames[state.b], n = sr.frames.length;
      cmp.textContent = "";
      cmp.style.aspectRatio = "";
      cmp.classList.toggle("cmp-empty", !fa.image || !fb.image);
      cmp.appendChild(media(sr, fa, "A"));
      cmp.appendChild(media(sr, fb, "B"));
      cmp.appendChild(el("div", { class: "cmp-af", "aria-hidden": "true" }, [el("i")]));
      cmp.appendChild(el("div", { class: "cmp-handle", role: "slider", tabindex: "0", "aria-label": L.cmpLabel, "aria-valuemin": "0", "aria-valuemax": "100" }, [el("span")]));
      setPos(state.pos);

      $("vf-status").innerHTML = "";
      [["mode", sr.mode || "M"], ["", "L"], ["ratio", "3:2"], ["", "AFS"], ["", fb.wb || "AWB"], ["", "STD."]].forEach(function (x) {
        $("vf-status").appendChild(el("span", { class: x[0], text: x[1] }));
      });
      $("vf-status").appendChild(el("span", { class: "batt" }, [el("i"), el("i"), el("i")]));
      $("vf-status").appendChild(el("span", { text: "98" }));

      $("vf-counter").innerHTML = "<b>" + pad(state.b + 1) + "</b> / " + pad(n);

      var keys = ["shutter", "aperture", "iso", "wb", "focal"];
      $("vf-data").textContent = "";
      [["A", fa], ["B", fb]].forEach(function (x) {
        var row = el("div", { class: "vf-row" }, [el("span", { class: "tag", text: x[0] })]);
        keys.map(function (k) { return fmt(x[1], k); }).filter(Boolean).forEach(function (v, i) {
          if (i) row.appendChild(el("i", { class: "dot", "aria-hidden": "true" }));
          row.appendChild(el("span", { text: v }));
        });
        $("vf-data").appendChild(row);
      });

      var ev = evDiff(fa, fb), x = isNaN(ev) ? null : 20 + (Math.max(-3, Math.min(3, ev)) + 3) / 6 * 560;
      var ticks = "";
      for (var t = -9; t <= 9; t++) {
        var tx = 20 + (t + 9) / 18 * 560, major = t % 3 === 0;
        ticks += '<line x1="' + tx + '" y1="34" x2="' + tx + '" y2="' + (major ? 20 : 27) + '"/>';
        if (major) ticks += '<text x="' + tx + '" y="54">' + (t > 0 ? "+" : t < 0 ? "−" : "") + Math.abs(t / 3) + "</text>";
      }
      $("vf-expo").innerHTML = '<span class="vf-expo-l">' + L.evLabel + ' <b>' + (isNaN(ev) ? L.evNone : evText(ev)) + "</b></span>" +
        '<svg viewBox="0 0 600 60" aria-hidden="true"><line x1="20" y1="34" x2="580" y2="34"/>' + ticks +
        (x === null ? "" : '<path class="mk" d="M' + (x - 7) + " 4 L" + (x + 7) + " 4 L" + x + ' 14 Z"/>') + "</svg>";

      $("vf-info").innerHTML = "";
      $("vf-info").appendChild(el("div", { class: "eyebrow", text: L.series + " " + (sr.id || "") + " · " + (L.topics[sr.topic] || "") }));
      $("vf-info").appendChild(el("h3", { text: pick(sr, "title") || L.topics[sr.topic] || "" }));
      if (pick(sr, "text")) $("vf-info").appendChild(el("p", { text: pick(sr, "text") }));
      $("vf-info").appendChild(el("p", { class: "hint", text: L.cmpHint }));

      var arc = document.getElementById("vf-arc");
      if (arc) arc.setAttribute("href", "/assets/img/deco.svg#" + (sr.topic === "focal" ? "arc-mm" : "arc-f"));

      cards.querySelectorAll(".card").forEach(function (c, i) {
        var side = i === state.a ? "A" : i === state.b ? "B" : "";
        c.setAttribute("data-side", side);
        c.setAttribute("aria-pressed", side ? "true" : "false");
        c.setAttribute("aria-label", L.cardLabel(big(sr, sr.frames[i]), side === "A" ? L.left : side === "B" ? L.right : ""));
      });
      drawHisto();
    }

    function renderSeries() {
      var sr = series[state.s], fr = sr.frames, n = fr.length;
      var ref = fr.findIndex(function (f) { return f.reference; });
      state.a = ref >= 0 ? ref : 0;
      state.b = n > 1 ? (state.a === n - 1 ? 0 : n - 1) : 0;
      cards.textContent = "";
      fr.forEach(function (f, i) {
        var others = ["shutter", "aperture", "iso", "wb", "focal"].filter(function (k) { return k !== (sr.topic || "shutter"); })
          .map(function (k) { return fmt(f, k); }).filter(Boolean);
        var b = el("button", { type: "button", class: "card" + (f.reference ? " hl" : "") }, [
          el("span", { class: "row" }, [el("span", { text: L.series + " " + (sr.id || "") }), el("span", { text: pad(i + 1) + "/" + pad(n) })]),
          el("span", { class: "val", text: big(sr, f) }),
          el("span", { class: "meta" }, [el("span", { text: (L.topics[sr.topic] || "").toUpperCase() }), el("br"), el("span", { text: others.slice(0, 2).join(" · ") })]),
          el("span", { class: "side", "aria-hidden": "true" })
        ]);
        b.addEventListener("click", function () {
          if (state.side === "a") { if (i === state.b) state.b = state.a; state.a = i; }
          else { if (i === state.a) state.a = state.b; state.b = i; }
          renderView();
        });
        cards.appendChild(b);
      });
      tabs.querySelectorAll("[role=tab]").forEach(function (t, i) {
        t.setAttribute("aria-selected", i === state.s ? "true" : "false");
        t.tabIndex = i === state.s ? 0 : -1;
      });
      renderView();
    }

    if (series.length > 1) {
      tabs.hidden = false;
      series.forEach(function (sr, i) {
        var t = el("button", { type: "button", role: "tab", text: (sr.id ? sr.id + " · " : "") + (pick(sr, "title") || L.topics[sr.topic] || "") });
        t.addEventListener("click", function () { state.s = i; renderSeries(); });
        t.addEventListener("keydown", function (e) {
          var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
          if (!d) return;
          e.preventDefault();
          state.s = (state.s + d + series.length) % series.length; renderSeries();
          tabs.querySelectorAll("[role=tab]")[state.s].focus();
        });
        tabs.appendChild(t);
      });
    }

    pickBox.hidden = false;
    pickBox.appendChild(el("span", { text: L.pickFor }));
    [["a", "A"], ["b", "B"]].forEach(function (x) {
      var b = el("button", { type: "button", text: x[1] + " · " + (x[0] === "a" ? L.left : L.right), "aria-pressed": x[0] === state.side ? "true" : "false" });
      b.addEventListener("click", function () {
        state.side = x[0];
        pickBox.querySelectorAll("button").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      });
      pickBox.appendChild(b);
    });

    /* Dragging the divider */
    var drag = false;
    function fromEvent(e) { var r = cmp.getBoundingClientRect(); setPos((e.clientX - r.left) / r.width * 100); }
    cmp.addEventListener("pointerdown", function (e) {
      if (e.button !== undefined && e.button !== 0) return;
      drag = true; try { cmp.setPointerCapture(e.pointerId); } catch (x) {}
      fromEvent(e);
    });
    cmp.addEventListener("pointermove", function (e) { if (drag) fromEvent(e); });
    ["pointerup", "pointercancel"].forEach(function (n) { cmp.addEventListener(n, function () { drag = false; }); });
    cmp.addEventListener("keydown", function (e) {
      if (!e.target.classList.contains("cmp-handle")) return;
      var step = e.shiftKey ? 10 : 2, m = { ArrowLeft: -step, ArrowDown: -step, ArrowRight: step, ArrowUp: step }[e.key];
      if (e.key === "Home") { setPos(0); e.preventDefault(); }
      else if (e.key === "End") { setPos(100); e.preventDefault(); }
      else if (m) { setPos(state.pos + m); e.preventDefault(); }
    });

    renderSeries();
  }).catch(function () {});
})();
