# Offband Site v1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Offband marketing site (`offband.org`) as a small, static Hugo site and deploy it free on Cloudflare Pages.

**Architecture:** Project-level Hugo (no external theme). A single base template + a content-driven page template, with reusable **shortcodes** (hero, cta, feature grid, roles table, downloads, sponsor) composed inside Markdown content. Brand styling via one CSS file piped/fingerprinted by Hugo. Brand assets (logo/favicon/OG) already exist in `static/img/`.

**Tech Stack:** Hugo Extended (static site generator), HTML templates (Go templates), CSS (hand-written, design tokens from the app's MeshPalette), Cloudflare Pages (hosting), Google Fonts (Inter / JetBrains Mono / Instrument Serif).

**Verification model:** This is a static site, not a unit-tested library. "Tests" here = `hugo` builds cleanly, `grep` confirms expected output in `public/`, and `hugo server` renders locally. Each task ends with a build/verify + commit.

---

## File structure

```
hugo.toml                         site config, params, menus
assets/css/main.css               design tokens + base + components (piped by Hugo)
layouts/_default/baseof.html      HTML skeleton (head + header + main + footer)
layouts/_default/single.html      generic page (renders .Content)
layouts/index.html                home page
layouts/partials/head.html        <head>: meta, SEO/OG, favicon, fonts, css pipe
layouts/partials/header.html      top nav (logo + menu)
layouts/partials/footer.html      footer (links, donate, license, ©)
layouts/shortcodes/hero.html      hero block
layouts/shortcodes/cta.html       two-button call-to-action row
layouts/shortcodes/featuregrid.html  grid of feature cards
layouts/shortcodes/rolestable.html   firmware roles table
layouts/shortcodes/downloads.html    per-platform download buttons (param-driven)
layouts/shortcodes/sponsor.html      GitHub Sponsors button (param-driven)
layouts/404.html                  not-found page
content/_index.md                 home content (composes shortcodes)
content/app.md                    app page
content/firmware.md               firmware page
content/about.md                  about page
content/donate.md                 donate page
static/_headers                   Cloudflare security headers
static/_redirects                 Cloudflare path redirects
static/robots.txt                 robots
static/img/*                      brand assets (already committed)
```

---

## External prerequisite gates (owner input — do NOT block scaffolding)

These are real-world inputs only the owner can provide. The build proceeds without them (params left empty render gracefully); they're filled before launch.

- **G1 — App download channels** (blocks final App downloads): which exist today and their URLs — APK (direct/GitHub release), Google Play, iOS (App Store/TestFlight/none), Windows build. Until provided, `downloads` shortcode hides empty entries.
- **G2 — GitHub Sponsors URL** (blocks Donate button going live): the `https://github.com/sponsors/<...>` URL. Until provided, `sponsor` shortcode shows a disabled "coming soon" button.
- **G3 — Cloudflare Pages + DNS** (blocks Task 11, Tier 2): owner connects the repo to Cloudflare Pages and points `offband.org`. Agent cannot do this (needs Cloudflare access).

---

## Task 0: Install Hugo + scaffold + first build

**Files:**
- Create: `hugo.toml` (minimal, replaced in Task 1)

- [ ] **Step 1: Install Hugo Extended**

Run: `winget install Hugo.Hugo.Extended --accept-source-agreements --accept-package-agreements`
Then open a fresh shell so PATH updates.

- [ ] **Step 2: Verify Hugo**

Run: `hugo version`
Expected: prints `hugo v0.1xx.x ... extended`

- [ ] **Step 3: Minimal config to make the repo a Hugo site**

`hugo.toml`:
```toml
baseURL = "https://offband.org/"
languageCode = "en-us"
title = "Offband"
```

- [ ] **Step 4: Build (empty site)**

Run: `hugo --gc --minify`
Expected: builds with 0 pages error-free, creates `public/`.

- [ ] **Step 5: Commit**

```bash
git add hugo.toml
git commit -m "chore(#1): hugo site skeleton + config"
```

---

## Task 1: Site config (params + menus)

**Files:**
- Modify: `hugo.toml`

- [ ] **Step 1: Full config**

`hugo.toml`:
```toml
baseURL = "https://offband.org/"
languageCode = "en-us"
title = "Offband"
enableRobotsTXT = false   # we ship our own static/robots.txt
disableKinds = ["taxonomy", "term"]

[params]
  description = "Offband — open-source tools for LoRa mesh networking. A MeshCore client app and enhanced firmware."
  tagline = "out-of-band mesh comms"
  ogImage = "/img/og-banner.png"
  githubOrg = "https://github.com/OffbandMesh"
  appRepo = "https://github.com/OffbandMesh/meshcore-client"
  firmwareRepo = "https://github.com/OffbandMesh/meshcore-firmware"
  firmwareReleases = "https://github.com/OffbandMesh/meshcore-firmware/releases"
  docsUrl = "https://docs.offband.org"
  sponsorUrl = ""   # G2 — fill when available

  # G1 — app download channels; empty entries are hidden by the shortcode
  [params.downloads]
    android_apk = ""
    google_play = ""
    ios = ""
    windows = ""
    web = ""

[menu]
  [[menu.main]]
    name = "App"
    pageRef = "/app"
    weight = 10
  [[menu.main]]
    name = "Firmware"
    pageRef = "/firmware"
    weight = 20
  [[menu.main]]
    name = "About"
    pageRef = "/about"
    weight = 30
  [[menu.main]]
    name = "Donate"
    pageRef = "/donate"
    weight = 40

[markup.goldmark.renderer]
  unsafe = true   # allow inline HTML in content where needed
```

- [ ] **Step 2: Build verify**

Run: `hugo --gc --minify`
Expected: builds clean.

- [ ] **Step 3: Commit**

```bash
git add hugo.toml
git commit -m "feat(#1): site params + nav menu"
```

---

## Task 2: Brand CSS (design tokens + base + components)

**Files:**
- Create: `assets/css/main.css`

- [ ] **Step 1: Write the stylesheet**

`assets/css/main.css`:
```css
:root{
  --bg:#0F1412; --bg1:#161C19; --bg2:#1D2521; --bg3:#28322D;
  --line:#232C28; --line2:#34403A; --line3:#48564F;
  --ink:#EFF3E8; --ink2:#BAC4B5; --ink3:#7C8B82;
  --signal:#7BEFA8; --signal-dim:#4DC580; --signal-bg:rgba(123,239,168,.09);
  --warn:#FFA552; --maxw:1080px; --r:12px;
  --sans:'Inter',system-ui,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
  --display:'Instrument Serif',Georgia,serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
a{color:var(--signal);text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3{line-height:1.15;font-weight:600;color:var(--ink);margin:0 0 .4em}
h1{font-size:clamp(34px,6vw,60px);letter-spacing:-.5px}
h2{font-size:clamp(24px,4vw,34px);letter-spacing:-.3px}
h3{font-size:20px}
p{color:var(--ink2);margin:0 0 1em}
code,.mono{font-family:var(--mono)}
section{padding:64px 0}
/* header */
.site-head{position:sticky;top:0;z-index:10;background:rgba(15,20,18,.86);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.site-head .wrap{display:flex;align-items:center;justify-content:space-between;height:64px}
.brand{display:flex;align-items:center;gap:0}
.brand img{height:30px;display:block}
.nav{display:flex;gap:22px;align-items:center}
.nav a{color:var(--ink2);font-size:15px}
.nav a:hover{color:var(--ink);text-decoration:none}
.nav a.donate{color:var(--signal)}
/* buttons */
.btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);
  font-size:15px;font-weight:500;padding:11px 20px;border-radius:10px;
  border:1px solid var(--signal-dim);color:var(--bg);background:var(--signal)}
.btn:hover{text-decoration:none;background:#9af3bd}
.btn.ghost{background:transparent;color:var(--signal);border-color:var(--line3)}
.btn.ghost:hover{background:var(--signal-bg);border-color:var(--signal-dim)}
.btn[aria-disabled="true"]{opacity:.45;pointer-events:none}
/* hero */
.hero{padding:96px 0 72px;text-align:center}
.hero .tagline{font-family:var(--mono);color:var(--signal);font-size:14px;
  letter-spacing:2px;text-transform:lowercase;margin-bottom:18px}
.hero p.lead{font-size:20px;max-width:640px;margin:0 auto 28px}
.cta{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
/* grid + cards */
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.card{background:var(--bg1);border:1px solid var(--line);border-radius:var(--r);padding:22px}
.card h3{margin-bottom:.3em}
.card p{font-size:15px;margin:0}
/* table */
.tbl{width:100%;border-collapse:collapse;font-size:15px}
.tbl th,.tbl td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line)}
.tbl th{color:var(--ink3);font-weight:500;font-family:var(--mono);font-size:13px}
.badge{font-family:var(--mono);font-size:12px;padding:2px 8px;border-radius:6px;
  background:var(--signal-bg);color:var(--signal);border:1px solid var(--line2)}
.badge.soon{background:transparent;color:var(--ink3)}
/* footer */
.site-foot{border-top:1px solid var(--line);padding:40px 0;color:var(--ink3);font-size:14px}
.site-foot .wrap{display:flex;flex-wrap:wrap;gap:18px;justify-content:space-between}
.site-foot a{color:var(--ink2)}
.center{text-align:center}
.muted{color:var(--ink3)}
```

- [ ] **Step 2: Commit** (CSS is wired in Task 3; commit now)

```bash
git add assets/css/main.css
git commit -m "feat(#1): brand stylesheet (MeshPalette tokens + components)"
```

---

## Task 3: Base template + head/header/footer partials

**Files:**
- Create: `layouts/_default/baseof.html`, `layouts/_default/single.html`,
  `layouts/partials/head.html`, `layouts/partials/header.html`, `layouts/partials/footer.html`

- [ ] **Step 1: `layouts/_default/baseof.html`**
```html
<!doctype html>
<html lang="en">
<head>{{ partial "head.html" . }}</head>
<body>
  {{ partial "header.html" . }}
  <main>{{ block "main" . }}{{ end }}</main>
  {{ partial "footer.html" . }}
</body>
</html>
```

- [ ] **Step 2: `layouts/partials/head.html`**
```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ if .IsHome }}{{ site.Title }} — {{ site.Params.tagline }}{{ else }}{{ .Title }} · {{ site.Title }}{{ end }}</title>
<meta name="description" content="{{ with .Description }}{{ . }}{{ else }}{{ site.Params.description }}{{ end }}">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/img/favicon.png" sizes="any">
<meta property="og:title" content="{{ if .IsHome }}{{ site.Title }}{{ else }}{{ .Title }}{{ end }}">
<meta property="og:description" content="{{ with .Description }}{{ . }}{{ else }}{{ site.Params.description }}{{ end }}">
<meta property="og:image" content="{{ site.Params.ogImage | absURL }}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Instrument+Serif&display=swap" rel="stylesheet">
{{ $css := resources.Get "css/main.css" | resources.Minify | fingerprint }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}" integrity="{{ $css.Data.Integrity }}">
```

- [ ] **Step 3: `layouts/partials/header.html`**
```html
<header class="site-head"><div class="wrap">
  <a class="brand" href="/" aria-label="Offband home"><img src="/img/logo-lockup-dark.svg" alt="Offband"></a>
  <nav class="nav">
    {{ range site.Menus.main }}<a href="{{ .PageRef | relURL }}"{{ if eq .Name "Donate" }} class="donate"{{ end }}>{{ .Name }}</a>{{ end }}
    <a href="{{ site.Params.docsUrl }}">Docs ↗</a>
  </nav>
</div></header>
```

- [ ] **Step 4: `layouts/partials/footer.html`**
```html
<footer class="site-foot"><div class="wrap">
  <span>© {{ now.Year }} Offband · MIT licensed · independent open-source</span>
  <span>
    <a href="{{ site.Params.githubOrg }}">GitHub</a> ·
    <a href="/donate">Donate</a> ·
    <a href="{{ site.Params.docsUrl }}">Docs</a>
  </span>
</div></footer>
```

- [ ] **Step 5: `layouts/_default/single.html`**
```html
{{ define "main" }}
<section><div class="wrap">
  <h1>{{ .Title }}</h1>
  {{ .Content }}
</div></section>
{{ end }}
```

- [ ] **Step 6: Build + grep verify**

Run: `hugo --gc --minify`
Then: `grep -r "site-head" public/ | head -1`
Expected: header HTML present in built output.

- [ ] **Step 7: Commit**
```bash
git add layouts/
git commit -m "feat(#1): base template + head/header/footer partials"
```

---

## Task 4: Shortcodes

**Files:**
- Create: `layouts/shortcodes/{hero,cta,featuregrid,rolestable,downloads,sponsor}.html`

- [ ] **Step 1: `hero.html`** (named params: tagline, lead)
```html
<section class="hero"><div class="wrap">
  <div class="tagline">{{ .Get "tagline" | default site.Params.tagline }}</div>
  <h1>{{ .Get "title" }}</h1>
  <p class="lead">{{ .Get "lead" }}</p>
  {{ .Inner }}
</div></section>
```

- [ ] **Step 2: `cta.html`** (paired buttons; inner = two `[label](url)` lines parsed as params)
```html
<div class="cta">
  <a class="btn" href="{{ .Get "href1" }}">{{ .Get "label1" }}</a>
  {{ with .Get "href2" }}<a class="btn ghost" href="{{ . }}">{{ $.Get "label2" }}</a>{{ end }}
</div>
```

- [ ] **Step 3: `featuregrid.html`** (inner = repeated `card` shortcodes OR data param). Simple version reads `.Inner` markdown:
```html
<section><div class="wrap"><div class="grid">{{ .Inner }}</div></div></section>
```
Plus `layouts/shortcodes/card.html`:
```html
<div class="card"><h3>{{ .Get "title" }}</h3><p>{{ .Get "body" }}</p></div>
```

- [ ] **Step 4: `rolestable.html`** (static firmware roles)
```html
<table class="tbl">
  <thead><tr><th>Role</th><th>Status</th><th>What Offband adds</th></tr></thead>
  <tbody>
    <tr><td>Companion / Observer</td><td><span class="badge">active</span></td><td>WiFi + MQTT publishing to public brokers, NimBLE BLE, multi-broker TLS + JWT, GPS→NTP wall clock, <code>_sys</code> config CLI</td></tr>
    <tr><td>Repeater</td><td><span class="badge">active</span></td><td>MQTT telemetry bridging, burst-WiFi telemetry, heap & power tuning</td></tr>
    <tr><td>Room server</td><td><span class="badge soon">planned</span></td><td>—</td></tr>
    <tr><td>Bridge</td><td><span class="badge soon">planned</span></td><td>—</td></tr>
  </tbody>
</table>
```

- [ ] **Step 5: `downloads.html`** (param-driven; hides empty — G1)
```html
<div class="cta">
{{ $d := site.Params.downloads }}
{{ with $d.android_apk }}<a class="btn" href="{{ . }}">Android APK</a>{{ end }}
{{ with $d.google_play }}<a class="btn ghost" href="{{ . }}">Google Play</a>{{ end }}
{{ with $d.ios }}<a class="btn ghost" href="{{ . }}">iOS</a>{{ end }}
{{ with $d.windows }}<a class="btn ghost" href="{{ . }}">Windows</a>{{ end }}
{{ with $d.web }}<a class="btn ghost" href="{{ . }}">Open web app</a>{{ end }}
{{ if not (or $d.android_apk $d.google_play $d.ios $d.windows $d.web) }}<span class="muted mono">Downloads coming soon — see the <a href="{{ site.Params.appRepo }}">app repo</a>.</span>{{ end }}
</div>
```

- [ ] **Step 6: `sponsor.html`** (G2)
```html
{{ with site.Params.sponsorUrl }}
  <a class="btn" href="{{ . }}">♥ Sponsor on GitHub</a>
{{ else }}
  <a class="btn" aria-disabled="true" href="#">♥ Sponsoring coming soon</a>
{{ end }}
```

- [ ] **Step 7: Build verify**

Run: `hugo --gc --minify`
Expected: clean (shortcodes compile; used in Tasks 5-9).

- [ ] **Step 8: Commit**
```bash
git add layouts/shortcodes/
git commit -m "feat(#1): content shortcodes (hero, cta, grid, roles, downloads, sponsor)"
```

---

## Task 5: Home page

**Files:**
- Create: `content/_index.md`, `layouts/index.html`

- [ ] **Step 1: `layouts/index.html`**
```html
{{ define "main" }}{{ .Content }}{{ end }}
```

- [ ] **Step 2: `content/_index.md`**
```markdown
---
title: Offband
---
{{< hero title="Off-band mesh comms" lead="Open-source tools for LoRa mesh networking — a cross-platform MeshCore client and enhanced firmware. Built for the people who run the mesh." >}}
{{< cta href1="/app" label1="Get the app" href2="/firmware" label2="Get the firmware" >}}
{{< /hero >}}

{{< featuregrid >}}
{{< card title="The app" body="Channel & direct chat, on-map node tracking, repeater admin, and offline on-device translation — over BLE, USB, or TCP." >}}
{{< card title="The firmware" body="A MeshCore fork: observer publishing to public brokers, repeater telemetry, NimBLE, and boot-survival diagnostics." >}}
{{< card title="Open & yours" body="MIT-licensed, no accounts, no tracking, no servers you don't control. A personal project, shared." >}}
{{< /featuregrid >}}
```

- [ ] **Step 3: Build + serve verify**

Run: `hugo --gc --minify` then `grep -o "Off-band mesh comms" public/index.html`
Expected: matches (hero rendered). Optionally `hugo server` and view http://localhost:1313.

- [ ] **Step 4: Commit**
```bash
git add content/_index.md layouts/index.html
git commit -m "feat(#1): home page"
```

---

## Task 6: App page  *(content depends on G1 for live download URLs)*

**Files:**
- Create: `content/app.md`

- [ ] **Step 1: `content/app.md`**
```markdown
---
title: The app
description: "Offband Meshcore — a cross-platform MeshCore client for Android, iOS, Windows, and web."
---
Offband Meshcore is a cross-platform client for MeshCore LoRa devices — connect over **BLE, USB serial, or TCP** and get full chat, mapping, and node administration.

{{< downloads >}}

{{< featuregrid >}}
{{< card title="Chat" body="Direct messages and named channels, with delivery tracking and message paths." >}}
{{< card title="Map" body="Live on-map positions for contacts and heard nodes, with hop-path traces." >}}
{{< card title="Repeater admin" body="Status, settings, and a raw CLI for managing repeater nodes." >}}
{{< card title="Offline translation" body="On-device LLM translation of incoming messages — no network needed." >}}
{{< card title="Three transports" body="Bluetooth LE, USB serial, and TCP/IP — one app, any link." >}}
{{< card title="Contacts & channels" body="Groups, favorites, QR sharing, and per-channel settings." >}}
{{< /featuregrid >}}

A fork of [zjs81/meshcore-open](https://github.com/zjs81/meshcore-open) (MIT). Source: [meshcore-client]({{< param appRepo >}}).
```

- [ ] **Step 2: Build + grep**

Run: `hugo --gc --minify` then `grep -o "Three transports" public/app/index.html`
Expected: matches.

- [ ] **Step 3: Commit**
```bash
git add content/app.md
git commit -m "feat(#1): app page"
```

---

## Task 7: Firmware page

**Files:**
- Create: `content/firmware.md`

- [ ] **Step 1: `content/firmware.md`**
```markdown
---
title: Firmware
description: "Offband firmware — a MeshCore fork with cross-role enhancements for ESP32-S3 boards."
---
Offband firmware is a [MeshCore](https://github.com/meshcore-dev/MeshCore) fork focused on **cross-role enhancements and optimization** for memory-constrained ESP32-S3 boards (Heltec LoRa32 V3 / V4, Seeed XIAO ESP32-S3, RAK).

{{< rolestable >}}

## Get it

Builds ship in three channels — **dev** (CI artifacts), **`-rc`** (community testing), and **stable** (the "Latest" release). The gate is real-hardware validation, not just a green build.

{{< cta href1="/firmware-releases-redirect" label1="Releases" >}}

Deep technical docs (observer CLI, SafeBoot, packet format) live at [docs.offband.org]({{< param docsUrl >}}). Source: [meshcore-firmware]({{< param firmwareRepo >}}).
```
> Note: replace `href1` with `{{< param firmwareReleases >}}` value — shortcodes can't take params in attrs directly, so hardcode the release URL `https://github.com/OffbandMesh/meshcore-firmware/releases` in the `cta` `href1`.

- [ ] **Step 2: Build + grep**

Run: `hugo --gc --minify` then `grep -o "Companion / Observer" public/firmware/index.html`
Expected: matches.

- [ ] **Step 3: Commit**
```bash
git add content/firmware.md
git commit -m "feat(#1): firmware page"
```

---

## Task 8: About page

**Files:**
- Create: `content/about.md`

- [ ] **Step 1: `content/about.md`**
```markdown
---
title: About
description: "Offband is a personal, open-source project for LoRa mesh networking."
---
**Offband** is a personal, open-source project for LoRa mesh networking — currently focused on [MeshCore](https://github.com/meshcore-dev/MeshCore). It's two things: a client **app** and enhanced **firmware**. No company, no accounts, no telemetry. Just tools for the mesh, shared under MIT.

## Credits

- The app is a fork of **[zjs81/meshcore-open](https://github.com/zjs81/meshcore-open)** (MIT).
- The firmware builds on **MeshCore** by Scott Powell / rippleradios.com (MIT).
- Offband's additions are released under the same MIT terms.

## Find it on GitHub

- [meshcore-client]({{< param appRepo >}}) — the app
- [meshcore-firmware]({{< param firmwareRepo >}}) — the firmware
- [OffbandMesh]({{< param githubOrg >}}) — the org
```

- [ ] **Step 2: Build + grep**

Run: `hugo --gc --minify` then `grep -o "personal, open-source project" public/about/index.html`
Expected: matches.

- [ ] **Step 3: Commit**
```bash
git add content/about.md
git commit -m "feat(#1): about page"
```

---

## Task 9: Donate page  *(button goes live with G2)*

**Files:**
- Create: `content/donate.md`

- [ ] **Step 1: `content/donate.md`**
```markdown
---
title: Donate
description: "Offband is free and open-source. If it helped you, you can chip in."
---
Offband is a hobby project — free, open-source, and built in spare time. There's nothing to buy and never will be. If it's been useful to you and you'd like to chip in toward hardware and time, that's genuinely appreciated. No pressure.

{{< sponsor >}}
```

- [ ] **Step 2: Build + grep**

Run: `hugo --gc --minify` then `grep -o "hobby project" public/donate/index.html`
Expected: matches.

- [ ] **Step 3: Commit**
```bash
git add content/donate.md
git commit -m "feat(#1): donate page"
```

---

## Task 10: Site meta (404, robots, headers, redirects)

**Files:**
- Create: `layouts/404.html`, `static/robots.txt`, `static/_headers`, `static/_redirects`

- [ ] **Step 1: `layouts/404.html`**
```html
{{ define "main" }}
<section class="hero"><div class="wrap">
  <div class="tagline">404 · off-band</div>
  <h1>Lost the signal</h1>
  <p class="lead">That page isn't on this channel. <a href="/">Head back home.</a></p>
</div></section>
{{ end }}
```

- [ ] **Step 2: `static/robots.txt`**
```
User-agent: *
Allow: /
Sitemap: https://offband.org/sitemap.xml
```

- [ ] **Step 3: `static/_headers`** (Cloudflare Pages security headers)
```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
```

- [ ] **Step 4: `static/_redirects`** (path-level; apex-domain redirect for off-band.com is set in Cloudflare dashboard — Task 11)
```
# placeholder for future path redirects
```

- [ ] **Step 5: Build + verify**

Run: `hugo --gc --minify` then `ls public/_headers public/robots.txt public/404.html`
Expected: all three present in `public/`.

- [ ] **Step 6: Commit**
```bash
git add layouts/404.html static/robots.txt static/_headers static/_redirects
git commit -m "feat(#1): 404, robots, security headers, redirects"
```

---

## Task 11: Cloudflare Pages deploy + DNS  *(GATE G3 — Tier 2, owner-gated)*

This is a **Tier 2** action (state outside the repo, needs Cloudflare access). Agent prepares; owner executes/approves.

- [ ] **Step 1: Confirm build settings for owner**

Cloudflare Pages → Create project → connect `OffbandMesh/offband-site`:
- Framework preset: **Hugo**
- Build command: `hugo --gc --minify`
- Build output directory: `public`
- Environment variable: `HUGO_VERSION` = (the version from Task 0, e.g. `0.1xx.x`)

- [ ] **Step 2: Verify preview deploy**

After first push to the branch, Cloudflare builds a **preview URL**. Owner opens it; confirm pages render, fonts/logo load, nav works.

- [ ] **Step 3: Point the domains (owner, in Cloudflare)**

- `offband.org` → the Pages production deployment (custom domain).
- `off-band.com` → 301 redirect to `https://offband.org` (Cloudflare Redirect Rule).
- (Defer `offband.app` — no web app yet; leave parked or 301 → offband.org per spec.)

- [ ] **Step 4: Verify production**

Run (owner machine or agent): `curl -sI https://offband.org | head -5`
Expected: `HTTP/2 200`. And `curl -sI https://off-band.com | head -5` → `301` to offband.org.

**Rollback:** disconnect the custom domain in Cloudflare Pages (reverts to `*.pages.dev`); delete the Redirect Rule. No repo changes to revert.

---

## Task 12: Epic integration verification

- [ ] **Step 1: Clean full build**

Run: `hugo --gc --minify`
Expected: builds all 5 pages + home + 404, zero errors/warnings.

- [ ] **Step 2: Page presence check**

Run: `for p in index app firmware about donate; do test -f public/$p/index.html 2>/dev/null || test -f public/index.html; done; ls public/{app,firmware,about,donate}/index.html`
Expected: all four section pages + home exist.

- [ ] **Step 3: Asset + meta check**

Run: `grep -l "og-banner.png" public/index.html && grep -l "favicon.svg" public/index.html && grep -o "main.min.*css" public/index.html | head -1`
Expected: OG image, favicon, and fingerprinted CSS all referenced.

- [ ] **Step 4: Local visual pass**

Run: `hugo server --bind 127.0.0.1 --port 1313`
Open http://localhost:1313 — walk all 5 pages: header logo, nav, hero, cards, firmware table, footer, dark theme, fonts. Confirm no broken links/images.

- [ ] **Step 5: Final commit + ready for PR**
```bash
git add -A
git commit -m "feat(#1): v1 integration verification"
```

---

## Self-review notes

- **Spec coverage:** Home/App/Firmware/About/Donate (Tasks 5-9), brand+logo (Tasks 2-3), domains/redirects (Tasks 10-11), donations (Task 9), docs link-out (header/firmware), Hugo→Cloudflare Pages (Tasks 0,11) — all covered.
- **Gates surfaced (not silent):** G1 downloads, G2 sponsor URL, G3 Cloudflare — each renders gracefully empty so the build never blocks.
- **Out of scope (per spec):** blog, changelog automation, git-CMS, Flutter web-app hosting, PNG/.ico were handled under #2.
- **Known nuance:** Hugo shortcodes don't accept `{{< param >}}` inside attribute values — release/repo URLs are hardcoded where a shortcode attr needs them (Task 7 note).
