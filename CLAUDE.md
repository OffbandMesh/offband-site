# Offband — Website (`offband-site`)

Source for **offband.org** — the static marketing/landing site for **Offband**, a
personal open-source project around LoRa mesh networking (currently MeshCore).

> Offband has two products, each in its own repo under the OffbandMesh org:
> the **app** (Offband Meshcore client) and the **firmware** (a MeshCore fork).
> This repo is just the website that introduces them.

## Stack

- **Hugo** — static site generator. Content in Markdown, a small custom theme
  (no heavy third-party theme). Single Go binary, no `node_modules`.
- **Cloudflare Pages** — free static hosting + CDN, no server. Each push builds a
  preview URL; the production branch serves the live domain.

## Structure (v1)

| Path | Page |
|------|------|
| `/` | Home |
| `/app` | The App |
| `/firmware` | Firmware |
| `/about` | About |
| `/donate` | Donate |

Planned later: blog, changelog. Deep firmware docs live separately (mkdocs).

## Build / run (once scaffolded)

```bash
hugo server   # local dev preview at http://localhost:1313
hugo          # build static site into ./public
```

## Brand

Phosphor-green on warm dark, mirroring the app's palette. Fonts: Inter (sans),
JetBrains Mono (mono), Instrument Serif (display).

## License

MIT — see [LICENSE](LICENSE). Offband is an independent project; the app and
firmware are MIT forks crediting upstream MeshCore (Scott Powell / rippleradios.com)
and, for the app, zjs81/meshcore-open.
