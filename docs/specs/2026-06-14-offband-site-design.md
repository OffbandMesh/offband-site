# Offband Site v1 — Design Spec

- **Date:** 2026-06-14
- **Tracking:** OffbandMesh/offband-site#1
- **Status:** Draft for review

## 1. Goal

A lean, static marketing/landing site for the **Offband** project — the front door
for both the **app** (Offband Meshcore client) and the **firmware** (a MeshCore
fork). Cheap to host, near-zero attack surface, expandable later without standing
up a server.

## 2. Constraints

- No new spend; no self-managed/runtime server.
- Low attack surface — no application runtime to exploit.
- Domains already managed via Cloudflare.
- Personal open-source; never commercial; donations welcome.

## 3. Stack & hosting

- **Hugo** — static site generator. Content in Markdown; a small custom theme
  rather than a heavy third-party one. Single Go binary, no `node_modules`
  (smaller build-time supply-chain surface than JS generators).
- **Cloudflare Pages** — free static hosting + global CDN, no server. Every git
  push builds a unique **preview URL**; the production branch serves the live
  domain. Redirects handled by Cloudflare rules.
- **Rationale:** satisfies every constraint; static output has no runtime to attack
  and nothing to patch.

## 4. Domains

| Domain | Serves |
|---|---|
| `offband.org` | this site (canonical home) |
| `offband.app` | Flutter app static web build (separate task, app repo) |
| `off-band.com` | 301 → `offband.org` |
| `docs.offband.org` | firmware deep docs (existing mkdocs site, separate repo) |

Marketing pages live on **one** canonical domain (`offband.org`) — serving the same
pages on multiple domains would split SEO (duplicate content).

## 5. Site structure (v1 — slots, not copy)

```
offband.org
├─ Header nav ──────  Home · App · Firmware · About · Donate · ↗ Docs
├─ /            Home
│   ├─ Hero               (tagline + one-liner)
│   ├─ Two-path CTA       [ Get the App ]  [ Get the Firmware ]
│   ├─ What-is-Offband
│   ├─ Highlights         (feature-teaser grid)
│   └─ Footer CTA         (repo / donate)
├─ /app         The App
│   ├─ Intro              (what it is + platforms)
│   ├─ Feature grid       (chat · map · repeater admin · translate · BLE/USB/TCP)
│   ├─ Screenshots
│   └─ Downloads          (per-platform buttons)
├─ /firmware    Firmware
│   ├─ Intro              (what the fork adds)
│   ├─ Roles table        (Companion/Observer · Repeater · Room/Bridge: planned)
│   ├─ Supported boards   (Heltec V3/V4 · XIAO · RAK)
│   ├─ Get it / flash     (release channels + flashing link)
│   └─ ↗ Deep docs        (link to docs.offband.org)
├─ /about       About     (personal OSS · credits/license · GitHub links)
├─ /donate      Donate    (honest ask · GitHub Sponsors button)
└─ Footer ──────  brand · nav · GitHub · donate · license · ©
```

## 6. Brand

- Reuse the app's design tokens: warm near-black surfaces, **phosphor-green** signal
  (`#7BEFA8`), ember/coral accents.
- Fonts: Inter (sans), JetBrains Mono (mono), Instrument Serif (display).
- **Logo + banner: NEEDED** — vector wordmark + mark, plus an OG/social banner.
  Tracked as a **separate task**; the site can launch type-only.

## 7. Content sourcing

- **App** — features/screenshots from the app repo (owner supplies final captures).
- **Firmware** — roles, boards, and release channels from the `meshcore-firmware`
  README; deep technical docs link out to `docs.offband.org` (not duplicated here).
- **Download channels** — *open item:* confirm which exist today (APK / Play Store /
  iOS / Windows) before wiring the Downloads slot.

## 8. Donations

- **GitHub Sponsors** (primary) — button on `/donate` and in the footer. No infra,
  no attack surface. (Ko-fi / Liberapay / Buy Me a Coffee are possible fallbacks.)

## 9. Out of scope (v1)

Blog, changelog automation, git-based CMS, logo/banner *design* (separate task),
Flutter web-app hosting (app repo), any per-user/interactive features.

## 10. Expansion path (later — no migration, no server)

- **Build-time dynamic:** blog (Markdown posts), changelog (pull GitHub releases at
  build). Hugo handles both natively.
- **Request-time dynamic (only if ever needed):** Cloudflare Pages Functions /
  Workers + D1 / KV / R2, bolted on per-feature. Never requires a VPS.

## 11. Delivery workflow

1. Scaffold Hugo + small custom theme + the 5 pages (per implementation plan).
2. Connect the repo to Cloudflare Pages → preview URL on every push.
3. Iterate on preview URLs (owner reviews in browser — cheap feedback loop).
4. On approval, point `offband.org` at the production deployment; set `off-band.com`
   301 → `offband.org`.

## 12. Open items / decisions still needed

- Which app **download channels** actually exist today.
- **Logo + banner** (separate task — blocks final visual polish, not scaffolding).
- **Cloudflare Pages** connection + DNS pointing — owner-gated (needs Cloudflare
  access); a Tier 2 step taken only with explicit approval.
