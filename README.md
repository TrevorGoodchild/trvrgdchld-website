# TRVR GDCHLD Visuals – Website

Portfolio für Fotografie und Motion Graphics. Englisch ist die Standardsprache (`/`), Deutsch liegt unter `/de/`.

- Keine Cookies, kein Tracking, Schriften lokal eingebunden
- YouTube-Showreel lädt erst nach Klick (erweiterter Datenschutzmodus)
- Inhalte pflegst du über die Verwaltungsoberfläche unter **`/admin`**

---

## 1. Online stellen mit Cloudflare Pages (kostenlos)

1. Bei [dash.cloudflare.com](https://dash.cloudflare.com) anmelden → links **Workers & Pages** → **Create** (bzw. „Anwendung erstellen“).
2. Den Reiter bzw. Link **Pages** wählen (nicht „Workers“) → **Import an existing Git repository** / „Mit Git verbinden“.
3. GitHub verbinden und das Repository **trvrgdchld-website** auswählen.
4. Einstellungen für den Build:
   - **Production branch:** `main`
   - **Framework preset:** `None`
   - **Build command:** leer lassen
   - **Build output directory:** leer lassen (bzw. `/`)
5. **Save and Deploy**. Nach ca. einer Minute ist die Seite unter `https://<projektname>.pages.dev` erreichbar.

Jede Änderung im Repository (auch aus dem CMS) wird danach automatisch veröffentlicht.

## 2. Verwaltungsoberfläche `/admin` freischalten (einmalig)

Der Login läuft über dein GitHub-Konto. Dafür braucht es eine „OAuth App“:

1. Auf GitHub: **Settings → Developer settings → OAuth Apps → New OAuth App**
   (direkt: https://github.com/settings/applications/new)
2. Ausfüllen:
   - **Application name:** `TRVR GDCHLD CMS`
   - **Homepage URL:** `https://<projektname>.pages.dev`
   - **Authorization callback URL:** `https://<projektname>.pages.dev/api/callback`
3. **Register application** → auf der nächsten Seite **Generate a new client secret**.
   Die **Client ID** und das **Client secret** gleich in Cloudflare eintragen (das Secret wird nur einmal angezeigt).
4. In Cloudflare: dein Pages-Projekt → **Settings → Variables and Secrets** (Umgebungsvariablen, Production) → hinzufügen:
   - `GITHUB_CLIENT_ID` = Client ID
   - `GITHUB_CLIENT_SECRET` = Client secret (als **Secret**/verschlüsselt)
5. Unter **Deployments** das letzte Deployment erneut ausführen (**Retry deployment**), damit die Variablen greifen.
6. `https://<projektname>.pages.dev/admin` öffnen → **Mit GitHub anmelden**.

> Wenn später eine eigene Domain dazukommt (z. B. `trvrgdchld.de`), in der OAuth App Homepage- und Callback-URL auf die neue Domain ändern.

## 3. Inhalte pflegen

Unter `/admin` gibt es vier Bereiche:

| Bereich | Was du dort änderst |
|---|---|
| **Fotos** | Bilder hochladen, Titel, Kategorie, Kachelgröße, Aufnahmedaten (Brennweite, Blende, Zeit, ISO) |
| **Motion-Projekte** | Titel und Texte (EN/DE), Vorschaubild, YouTube-Link |
| **Labor** | Die Vorhaltekarten der aktuellen Testreihe |
| **Einstellungen** | Name, E-Mail, Ort, „Verfügbar ab“, Portraitfoto, Über-mich-Text (EN/DE), Showreel, Social-Media-Links |

Nach dem **Veröffentlichen** im CMS ist die Änderung nach ca. einer Minute live.

**Bilder:** am besten JPG oder WebP mit ca. 2000 px an der langen Kante und unter 500 KB – so lädt die Seite schnell.

## 4. Was nicht im CMS steht

Feste Texte, die Praxis-/Guide-Seite sowie **Impressum und Datenschutz** werden aus `tools/build.py` erzeugt.
Die Angaben fürs Impressum (Name, Anschrift, Telefon, E-Mail, ggf. USt-IdNr.) stehen oben in dieser Datei unter `LEGAL`.
Nach einer Änderung: `python3 tools/build.py` ausführen und die erzeugten Dateien hochladen.

## Aufbau

```
index.html, de/, guide/, …   fertige Seiten (von tools/build.py erzeugt)
content/*.json               Inhalte, die das CMS bearbeitet
assets/                      CSS, JavaScript, Schriften, Bilder, Uploads
admin/                       Decap CMS (Verwaltungsoberfläche)
functions/api/               Login für das CMS (Cloudflare Pages Functions)
_headers, robots.txt         Einstellungen für Cloudflare / Suchmaschinen
```

Schriften: Syne, DM Sans und JetBrains Mono unter der SIL Open Font License (siehe `assets/fonts/OFL-*.txt`).
