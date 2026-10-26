# -*- coding: utf-8 -*-
"""Kopīgas SVG palīgfunkcijas šīs lekcijas attēlu skriptiem.

Katrs attēlu skripts izsauc main(build, "vards.svg"); uzrakstu valodu izvēlas
komandrindā (kā lossy_hamming/figs/sha256_diagram.py):

    python aes_round.py              # abas valodas: aes-round.svg un aes-round.en.svg
    python aes_round.py --lang en    # tikai angļu: aes-round.en.svg
    python aes_round.py --lang lv    # tikai latviešu: aes-round.svg
"""

import argparse
import os

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Consolas, Menlo, monospace"
INK, GREY = "#222", "#555"
BLUE, ORANGE, GREEN, PURPLE, RED, TEAL = "#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756", "#72B7B2"
# gaišie fona toņi tām pašām krāsām
L_BLUE, L_ORANGE, L_GREEN, L_PURPLE, L_RED, L_TEAL, L_GREY = (
    "#dbe6f3", "#fde5cc", "#dcecd8", "#ecdcea", "#f9dcdc", "#dcefee", "#f4f6f8")

LANG = "lv"                            # uzrakstu valoda: "lv" vai "en" (sk. main)


def T(lv, en):
    """Uzraksts izvēlētajā valodā LANG."""
    return en if LANG == "en" else lv


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal", family=FONT, raw=False,
        italic=False):
    st = ' font-style="italic"' if italic else ""
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s"%s>%s</text>\n'
            % (x, y, family, size, fill, anchor, weight, st, s if raw else esc(s)))


def sub(s):
    return '<tspan baseline-shift="sub" font-size="75%%">%s</tspan>' % s


def sup(s):
    return '<tspan baseline-shift="super" font-size="75%%">%s</tspan>' % s


def rect(x, y, w, h, fill, stroke, sw=1.4, rx=0, extra=""):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
            'stroke="%s" stroke-width="%g"%s/>\n' % (x, y, w, h, rx, fill, stroke, sw, extra))


def line(x1, y1, x2, y2, col="#444", sw=1.6, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"%s/>\n'
            % (x1, y1, x2, y2, col, sw, d))


def arrow(x1, y1, x2, y2, col="#444", sw=1.6, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"%s '
            'marker-end="url(#arw)"/>\n' % (x1, y1, x2, y2, col, sw, d))


def path_arrow(d, col="#444", sw=1.6, dash=None):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%g"%s marker-end="url(#arw)"/>\n'
            % (d, col, sw, ds))


def xor(cx, cy, r=10, col=INK):
    """Simbols ⊕ (XOR)."""
    return ('<circle cx="%g" cy="%g" r="%g" fill="#fff" stroke="%s" stroke-width="1.5"/>\n'
            % (cx, cy, r, col) + line(cx - r, cy, cx + r, cy, col, 1.5)
            + line(cx, cy - r, cx, cy + r, col, 1.5))


def mul(cx, cy, r=10, col=INK):
    """Simbols ⊗ (reizināšana laukā)."""
    k = r * 0.7071
    return ('<circle cx="%g" cy="%g" r="%g" fill="#fff" stroke="%s" stroke-width="1.5"/>\n'
            % (cx, cy, r, col) + line(cx - k, cy - k, cx + k, cy + k, col, 1.5)
            + line(cx - k, cy + k, cx + k, cy - k, col, 1.5))


def badge(x, y, n, col=BLUE):
    return ('<circle cx="%g" cy="%g" r="10" fill="%s"/>\n' % (x, y, col)
            + txt(x, y + 4.3, str(n), 12, "#fff", weight="bold"))


def header(W, H, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">\n'
            '<title>%s</title>\n'
            '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
            '<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
            'fill="#444"/></marker></defs>\n' % (W, H, W, H, esc(title), esc(title), W, H))


def svg_name(name):
    """Faila nosaukums izvēlētajā valodā: x.svg (latviski) vai x.en.svg (angliski)."""
    return name[:-4] + ".en.svg" if LANG == "en" else name


def main(build, name):
    """Komandrindas apstrāde: --lang lv|en|both; SVG ieraksta blakus skriptam."""
    global LANG
    ap = argparse.ArgumentParser(description="Ģenerē %s (uzraksti latviski un/vai angliski)." % name)
    ap.add_argument("--lang", choices=["lv", "en", "both"], default="both",
                    help="uzrakstu valoda (noklusējums: abas)")
    ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)),
                    help="direktorija, kur ierakstīt SVG (noklusējums: blakus skriptam)")
    args = ap.parse_args()
    for lang in (["lv", "en"] if args.lang == "both" else [args.lang]):
        LANG = lang
        out = os.path.join(args.outdir, svg_name(name))
        with open(out, "w", encoding="utf-8") as f:
            f.write(build())
        print("->", out)
