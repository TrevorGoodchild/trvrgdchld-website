// Cloudflare Pages Function: nimmt die Antwort von GitHub entgegen und gibt
// den Zugang an das CMS-Fenster weiter. Benötigt GITHUB_CLIENT_ID und
// GITHUB_CLIENT_SECRET als Umgebungsvariablen in Cloudflare.
export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const cookie = request.headers.get("Cookie") || "";
  const saved = (cookie.match(/(?:^|;\s*)decap_oauth_state=([^;]+)/) || [])[1];

  if (!code || !state || state !== saved) {
    return page("error", { message: "Anmeldung abgebrochen oder abgelaufen. Bitte erneut versuchen." }, url.origin);
  }

  try {
    const res = await fetch("https://github.com/login/oauth/access_token", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json", "User-Agent": "trvrgdchld-cms" },
      body: JSON.stringify({
        client_id: env.GITHUB_CLIENT_ID,
        client_secret: env.GITHUB_CLIENT_SECRET,
        code,
        redirect_uri: `${url.origin}/api/callback`,
      }),
    });
    const data = await res.json();
    if (!data.access_token) {
      return page("error", { message: data.error_description || "Kein Zugang von GitHub erhalten." }, url.origin);
    }
    return page("success", { token: data.access_token, provider: "github" }, url.origin);
  } catch (e) {
    return page("error", { message: "Verbindung zu GitHub fehlgeschlagen." }, url.origin);
  }
}

function page(status, content, origin) {
  const msg = `authorization:github:${status}:${JSON.stringify(content)}`;
  const html = `<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Anmeldung</title></head>
<body style="font-family:system-ui;background:#1C1220;color:#F5EBE0;padding:40px">
<p>${status === "success" ? "Angemeldet – dieses Fenster schließt sich gleich." : "Anmeldung fehlgeschlagen."}</p>
<script>
(function () {
  var origin = ${JSON.stringify(origin)};
  var msg = ${JSON.stringify(msg)};
  function receive(e) {
    if (e.origin !== origin) return;
    window.opener.postMessage(msg, origin);
    window.removeEventListener("message", receive, false);
  }
  if (window.opener) {
    window.addEventListener("message", receive, false);
    window.opener.postMessage("authorizing:github", origin);
  }
})();
</script></body></html>`;
  return new Response(html, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-store",
      "Set-Cookie": "decap_oauth_state=; Path=/api; HttpOnly; Secure; SameSite=Lax; Max-Age=0",
    },
  });
}
