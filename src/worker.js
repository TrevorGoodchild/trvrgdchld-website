// Cloudflare Worker für TRVR GDCHLD Visuals
// - Liefert die fertige Website aus dem Ordner public/ aus (static assets)
// - /api/auth und /api/callback: GitHub-Login für das CMS unter /admin
//
// Benötigt in Cloudflare (Worker → Settings → Variables and Secrets):
//   GITHUB_CLIENT_ID      Client ID der GitHub OAuth App
//   GITHUB_CLIENT_SECRET  Client secret der GitHub OAuth App (als Secret)

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/auth") return auth(url, env);
    if (url.pathname === "/api/callback") return callback(request, url, env);
    return env.ASSETS.fetch(request);
  },
};

function auth(url, env) {
  if (!env.GITHUB_CLIENT_ID) {
    return new Response("GITHUB_CLIENT_ID fehlt in den Cloudflare-Einstellungen.", { status: 500 });
  }
  const state = crypto.randomUUID();
  const authorize = new URL("https://github.com/login/oauth/authorize");
  authorize.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
  authorize.searchParams.set("redirect_uri", `${url.origin}/api/callback`);
  authorize.searchParams.set("scope", "repo");
  authorize.searchParams.set("state", state);
  return new Response(null, {
    status: 302,
    headers: {
      Location: authorize.toString(),
      "Set-Cookie": `decap_oauth_state=${state}; Path=/api; HttpOnly; Secure; SameSite=Lax; Max-Age=600`,
      "Cache-Control": "no-store",
    },
  });
}

async function callback(request, url, env) {
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

// Übergibt das Ergebnis per postMessage an das CMS-Fenster (Decap-Protokoll).
function page(status, content, origin) {
  const msg = `authorization:github:${status}:${JSON.stringify(content)}`;
  const html = `<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Anmeldung</title></head>
<body style="font-family:system-ui;background:#1C1220;color:#F5EBE0;padding:40px">
<p>${status === "success" ? "Angemeldet – dieses Fenster schließt sich gleich." : "Anmeldung fehlgeschlagen."}</p>
<script>
(function () {
  var origin = ${JSON.stringify(origin)};
  var msg = ${JSON.stringify(msg).replace(/</g, "\\u003c")};
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
