# TRVR GDCHLD Visuals – Website

Portfolio für Fotografie und Motion Graphics. Englisch ist die Standardsprache (`/`), Deutsch liegt unter `/de/`.

- Keine Cookies, kein Tracking, Schriften lokal eingebunden
- YouTube-Showreel lädt erst nach Klick (erweiterter Datenschutzmodus)
- Inhalte pflegst du über die Verwaltungsoberfläche unter **`/admin`**

---

## 1. Online (Cloudflare Worker, kostenlos)

Die Seite läuft als Cloudflare Worker mit Git-Anbindung:
**https://trvrgdchld-website.trevorgoodchild1979.workers.dev**

Jede Änderung im Repository (auch aus dem CMS) wird automatisch neu veröffentlicht.
Die Einstellungen dafür stehen in `wrangler.jsonc`; in Cloudflare bleibt der Deploy-Befehl `npx wrangler deploy`.

## 2. Verwaltungsoberfläche `/admin` freischalten (einmalig)

Der Login läuft über dein GitHub-Konto. Dafür braucht es eine „OAuth App“:

1. Auf GitHub: **Settings → Developer settings → OAuth Apps → New OAuth App**
   (direkt: https://github.com/settings/applications/new)
2. Ausfüllen:
   - **Application name:** `TRVR GDCHLD CMS`
   - **Homepage URL:** `https://trvrgdchld-website.trevorgoodchild1979.workers.dev`
   - **Authorization callback URL:** `https://trvrgdchld-website.trevorgoodchild1979.workers.dev/api/callback`
3. **Register application** → auf der nächsten Seite **Generate a new client secret**.
   Client ID und Client secret gleich in Cloudflare eintragen (das Secret wird nur einmal angezeigt).
4. In Cloudflare: **Workers & Pages → trvrgdchld-website → Settings → Variables and Secrets → Add**:
   - `GITHUB_CLIENT_ID` = Client ID
   - `GITHUB_CLIENT_SECRET` = Client secret (Typ **Secret**)
   → **Deploy** bzw. Speichern.
5. `…workers.dev/admin` öffnen → **Mit GitHub anmelden**.

> Wenn später eine eigene Domain dazukommt (z. B. `trvrgdchld.de`), in der OAuth App Homepage- und Callback-URL auf die neue Domain ändern.

## 3. Inhalte pflegen

Unter `/admin` gibt es diese Bereiche:

| Bereich | Was du dort änderst |
|---|---|
| **Foto-Alben** | Alben anlegen (Titel DE/EN, Kurzname für die Adresse, Kategorie, Datum, Ort, Titelbild, Beschreibung, Kamera) und darin Fotos mit Bildunterschrift und Aufnahmedaten |
| **Motion-Playlists** | YouTube-Playlists mit Titel, Text und eigenem Vorschaubild |
| **Labor** | Die Vorhaltekarten der aktuellen Testreihe |
| **Rechtliches** | Deine Angaben fürs Impressum, weitere Impressum-Abschnitte, Datenschutzerklärung (DE/EN) |
| **Einstellungen** | Name, E-Mail, Ort, „Verfügbar ab“, Portraitfoto, Über-mich-Text (EN/DE), Showreel, Social-Media-Links |

Jedes Album hat eine eigene Seite: `/album/?a=<kurzname>` (Deutsch: `/de/album/?a=<kurzname>`).

Nach dem **Veröffentlichen** im CMS ist die Änderung nach ca. einer Minute live.

**Bilder:** am besten JPG oder WebP mit ca. 2000 px an der langen Kante und unter 500 KB – so lädt die Seite schnell.

## 4. Was nicht im CMS steht

Feste Texte der Seiten und die Praxis-/Guide-Seite werden aus `tools/build.py` erzeugt.
Nach einer Änderung: `python3 tools/build.py` ausführen – die Seiten landen in `public/` – und hochladen.

Impressum und Datenschutz stehen in `public/content/legal.json` und werden im CMS unter **Rechtliches** gepflegt.
Die Seiten laden die Texte beim Aufruf von dort; `tools/build.py` erzeugt zusätzlich eine statische Fassung.

## Aufbau

```
public/                      alles, was online sichtbar ist
  index.html, de/, guide/, … fertige Seiten (von tools/build.py erzeugt)
  content/*.json             Inhalte, die das CMS bearbeitet
  assets/                    CSS, JavaScript, Schriften, Bilder, Uploads
  admin/                     Decap CMS (Verwaltungsoberfläche)
src/worker.js                Cloudflare Worker: liefert public/ aus + CMS-Login (/api/…)
wrangler.jsonc               Cloudflare-Einstellungen
tools/build.py               erzeugt die HTML-Seiten
```

Schriften: Syne, DM Sans und JetBrains Mono unter der SIL Open Font License (siehe `assets/fonts/OFL-*.txt`).
