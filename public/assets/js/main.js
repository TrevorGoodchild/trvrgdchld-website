/* TRVR GDCHLD Visuals – Seitenlogik
   Liest die Inhalte aus /content/*.json (dort pflegt das CMS die Daten)
   und baut Fotos, Motion-Projekte und Laborkarten auf. */
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
      series: "SERIES", shutter: "SHUTTER · MECH.",
      menuOpen: "Open menu", menuClose: "Close menu"
    },
    de: {
      cats: { all: "Alle", portrait: "Portrait", street: "Street", landscape: "Landschaft", product: "Produkt", event: "Event & Konzert" },
      noPhotos: "In dieser Kategorie gibt es noch keine Alben.",
      photos: "Fotos", photo: "Foto", openAlbum: "Album öffnen", albumMissing: "Dieses Album wurde nicht gefunden.",
      emptyAlbum: "Die Fotos zu diesem Album folgen bald.",
      playPlaylist: "Playlist laden und abspielen", noPlaylist: "Diese Playlist ist bald verfügbar.", months: ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],
      watch: "Auf YouTube ansehen",
      noReel: "Das Showreel ist hier bald zu sehen.",
      series: "SERIE", shutter: "VERSCHLUSS · MECH.",
      menuOpen: "Menü öffnen", menuClose: "Menü schließen"
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
        cap.textContent = [ph.caption, specsOf(ph, al.camera), (cur + 1) + " / " + photos.length].filter(Boolean).join("  ·  ");
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

  /* Lab cards */
  getJSON("/content/lab.json").then(function (data) {
    var box = document.getElementById("cards");
    var cards = data.cards || [];
    box.textContent = "";
    cards.forEach(function (c, i) {
      var n = String(i + 1).padStart(2, "0") + "/" + String(cards.length).padStart(2, "0");
      box.appendChild(el("div", { class: "card" + (c.highlight ? " hl" : "") }, [
        el("div", { class: "row" }, [el("span", { text: L.series + " " + (data.series || "") }), el("span", { text: n })]),
        el("div", { class: "val", text: c.value || "" }),
        el("div", { class: "meta" }, [el("span", { text: L.shutter }), el("br"), el("span", { text: [c.aperture, c.iso].filter(Boolean).join(" · ") })])
      ]));
    });
  }).catch(function () {});
})();
