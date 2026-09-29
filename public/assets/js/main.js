/* TRVR GDCHLD Visuals – Seitenlogik
   Liest die Inhalte aus /content/*.json (dort pflegt das CMS die Daten)
   und baut Fotos, Motion-Projekte und Laborkarten auf. */
(function () {
  "use strict";

  var lang = (document.documentElement.lang || "en").slice(0, 2) === "de" ? "de" : "en";
  var L = {
    en: {
      cats: { all: "All", portrait: "Portrait", street: "Street", landscape: "Landscape", product: "Product" },
      noPhotos: "No photos in this category yet.",
      watch: "Watch on YouTube",
      noReel: "The showreel will be available here soon.",
      series: "SERIES", shutter: "SHUTTER · MECH.",
      menuOpen: "Open menu", menuClose: "Close menu"
    },
    de: {
      cats: { all: "Alle", portrait: "Portrait", street: "Street", landscape: "Landschaft", product: "Produkt" },
      noPhotos: "In dieser Kategorie gibt es noch keine Bilder.",
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

  /* Only the home page needs content */
  if (!document.getElementById("photo-grid")) return;

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
      var f = el("iframe", {
        src: "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0",
        title: "Showreel",
        allow: "autoplay; encrypted-media; picture-in-picture; fullscreen",
        allowfullscreen: "",
        referrerpolicy: "strict-origin-when-cross-origin"
      });
      box.appendChild(f);
    });
  }

  /* Photos */
  var grid = document.getElementById("photo-grid");
  var filterBox = document.getElementById("filters");
  getJSON("/content/photos.json").then(function (data) {
    var photos = (data.photos || []);
    grid.textContent = "";
    var cats = ["all"];
    photos.forEach(function (ph, i) {
      if (ph.category && cats.indexOf(ph.category) < 0) cats.push(ph.category);
      var specs = [ph.camera, ph.focal, ph.aperture, ph.shutter, ph.iso].filter(Boolean).join(" · ");
      var fig = el("figure", { class: "tile " + (ph.size && ph.size !== "normal" ? ph.size : ""), "data-cat": ph.category || "" });
      if (ph.image) fig.appendChild(el("img", { src: ph.image, alt: ph.alt || ph.title || "", loading: "lazy", decoding: "async" }));
      else fig.style.background = TILE_COLORS[i % TILE_COLORS.length];
      fig.appendChild(el("figcaption", null, [
        ph.title ? el("b", { text: ph.title }) : null,
        specs ? el("span", { text: specs }) : null
      ]));
      grid.appendChild(fig);
    });
    var empty = el("p", { class: "empty-note", text: L.noPhotos }); empty.hidden = true; grid.appendChild(empty);

    filterBox.textContent = "";
    cats.forEach(function (c) {
      var b = el("button", { type: "button", class: "chip", "aria-pressed": c === "all" ? "true" : "false", text: L.cats[c] || c });
      b.addEventListener("click", function () {
        filterBox.querySelectorAll(".chip").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        var shown = 0;
        grid.querySelectorAll(".tile").forEach(function (t) {
          var on = c === "all" || t.getAttribute("data-cat") === c;
          t.hidden = !on; if (on) shown++;
        });
        empty.hidden = shown > 0;
      });
      filterBox.appendChild(b);
    });
  }).catch(function () {});

  /* Motion projects */
  getJSON("/content/motion.json").then(function (data) {
    var box = document.getElementById("projects");
    box.textContent = "";
    (data.projects || []).forEach(function (pr, i) {
      var thumb = el("div", { class: "thumb" });
      if (pr.image) thumb.appendChild(el("img", { src: pr.image, alt: "", loading: "lazy" }));
      else thumb.style.background = TILE_COLORS[(i + 3) % TILE_COLORS.length];
      var link = safeUrl(pr.youtube_url);
      box.appendChild(el("article", { class: "project" }, [
        thumb,
        pr.tag ? el("div", { class: "tag", text: String(pr.tag).toUpperCase() }) : null,
        el("h3", { text: pick(pr, "title") }),
        pick(pr, "text") ? el("p", { text: pick(pr, "text") }) : null,
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
