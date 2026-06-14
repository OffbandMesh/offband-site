#!/usr/bin/env python3
"""Generate Offband brand SVG assets (mark, lockups, favicon, OG banner).

Reproducible source for the logo. Pure-shape mark + Morse; the wordmark uses
JetBrains Mono via <text> (outline it in a vector editor for non-browser use).
Run: python scripts/gen-logo.py  ->  writes static/img/*.svg
"""
import os

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "static", "img"))
os.makedirs(OUT, exist_ok=True)

GREEN = "#7BEFA8"       # phosphor signal (dark bg)
GREEN_DIM = "#4DC580"   # dimmer signal (arcs)
GREEN_DARK = "#1A7A44"  # signal for light bg
INK = "#EFF3E8"         # light ink (dark bg)
INK_DARK = "#0F1412"    # dark ink (light bg)
BG = "#0F1412"          # warm near-black surface

FONT = "'JetBrains Mono','JetBrains Mono NL',ui-monospace,SFMono-Regular,Menlo,monospace"
FONT_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&amp;display=swap');"

MORSE = {"o": "---", "f": "..-.", "b": "-...", "a": ".-", "n": "-.", "d": "-.."}
WORD = "offband"


def mark(transform, arc, dot, sw="2.4"):
    return (
        f'<g transform="{transform}">'
        f'<path d="M29.5 26.1 A12 12 0 1 0 39.7 35.3" fill="none" stroke="{arc}" stroke-width="{sw}" stroke-linecap="round"/>'
        f'<path d="M30.3 19.1 A19 19 0 1 0 46.5 33.7" fill="none" stroke="{arc}" stroke-width="{sw}" stroke-linecap="round" opacity="0.5"/>'
        f'<circle cx="28" cy="38" r="3.6" fill="{dot}"/>'
        f'<circle cx="46.1" cy="17.9" r="3" fill="{dot}"/>'
        f"</g>"
    )


def morse(x0, y_top, color, dot_w=6, dash_w=14, intra=4, inter=10, h=6):
    x = x0
    parts = []
    for i, ch in enumerate(WORD):
        code = MORSE[ch]
        for j, sym in enumerate(code):
            if sym == ".":
                parts.append(f'<circle cx="{x + dot_w / 2:.1f}" cy="{y_top + h / 2:.1f}" r="{h / 2:.1f}" fill="{color}"/>')
                x += dot_w
            else:
                parts.append(f'<rect x="{x:.1f}" y="{y_top:.1f}" width="{dash_w}" height="{h}" rx="{h / 2:.1f}" fill="{color}"/>')
                x += dash_w
            if j < len(code) - 1:
                x += intra
        if i < len(WORD) - 1:
            x += inter
    return "".join(parts), x


def lockup(ink, arc, dot):
    m = mark("translate(-0.8 -14.15) scale(2.157)", arc, dot)
    word = (
        f'<text x="138" y="82" font-family="{FONT}" font-weight="500" '
        f'font-size="76" letter-spacing="1" fill="{ink}">offband</text>'
    )
    mor, _ = morse(138, 98, ink)
    return m + word + mor


def svg(vb, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Offband">'
        f"{defs}{body}</svg>\n"
    )


def style_defs():
    return f"<defs><style>{FONT_IMPORT}</style></defs>"


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {name}  ({len(content)} bytes)")


print(f"writing to {OUT}")
write("logo-mark.svg", svg("4 11 50 50", mark("translate(0 0)", GREEN_DIM, GREEN, "3")))
write("favicon.svg", svg("0 0 64 64", f'<rect width="64" height="64" rx="14" fill="{BG}"/>' + mark("translate(2.1 -5.1) scale(1.03)", GREEN_DIM, GREEN)))
write("logo-lockup-dark.svg", svg("0 0 500 128", lockup(INK, GREEN_DIM, GREEN), style_defs()))
write("logo-lockup-light.svg", svg("0 0 500 128", lockup(INK_DARK, GREEN_DARK, GREEN_DARK), style_defs()))
write("og-banner.svg", svg("0 0 1200 630", f'<rect width="1200" height="630" fill="{BG}"/><g transform="translate(190.3 207.2) scale(1.7)">' + lockup(INK, GREEN_DIM, GREEN) + "</g>", style_defs()))
print("done")
