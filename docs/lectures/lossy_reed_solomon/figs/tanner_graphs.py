# -*- coding: utf-8 -*-
"""Ģenerē Tanera grafus tādā pašā stilā kā ldpc-tanner.svg:

* hamming-tanner.svg      -- Heminga kods [7,4,1]:
                               y1 = x1+x2+x3, y2 = x1+x2+x4, y3 = x1+x3+x4;
* erasure-problem.svg     -- 8.5. uzdevuma kods:
                               y1 = x1+x2+x3, y2 = x1+x4+x5,
                               y3 = x2+x4+x6, y4 = x3+x5+x6
  (saskaitīšana pēc moduļa 2, t.i., XOR).

Ziņojuma biti x_j ir aplīši apakšējā rindā, kontrolbiti (pārbaudes) y_i --
kvadrātiņi augšējā rindā; šķautne savieno y_i ar katru x_j, kas ietilpst y_i
formulā.  Zīmēšanas funkcijas un krāsas ņemtas no ldpc_toy.py.


Uzraksti ir latviski (hamming-tanner.svg, erasure-problem.svg) un angliski (hamming-tanner.en.svg, erasure-problem.en.svg):

    python tanner_graphs.py              # abas valodas
    python tanner_graphs.py --lang en    # tikai angļu
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ldpc_toy as L  # noqa: E402

# nosaukums: ((virsraksts latviski, angliski), bitu skaits, pārbaudes)
GRAPHS = {
    "hamming-tanner.svg": (
        ("Heminga koda [7,4,1] Tanera grafs", "Tanner graph of the Hamming code [7,4,1]"), 4,
        [[1, 2, 3], [1, 2, 4], [1, 3, 4]]),
    "erasure-problem.svg": (
        ("Tanera grafs 8.5. uzdevumam", "Tanner graph for Problem 8.5"), 6,
        [[1, 2, 3], [1, 4, 5], [2, 4, 6], [3, 5, 6]]),
}


LANG = "lv"                           # uzrakstu valoda: "lv" vai "en" (sk. main)


def T(lv, en):
    """Uzraksts izvēlētajā valodā LANG."""
    return en if LANG == "en" else lv


def svg_name(name):
    """Faila nosaukums izvēlētajā valodā: x.svg (latviski) vai x.en.svg (angliski)."""
    return name[:-4] + ".en.svg" if LANG == "en" else name


def label(x, y, letter, index, size=13):
    """Burts ar apakšindeksu, piemēram, x₁ (SVG tspan)."""
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="middle" font-weight="bold">%s<tspan baseline-shift="sub" '
            'font-size="75%%">%d</tspan></text>\n'
            % (x, y, L.FONT, size, L.INK, letter, index))


def tanner_svg(title, n_bits, checks):
    step = 64
    W = max(n_bits, len(checks)) * step + 60
    Ht = 230
    ycheck, ybit = 50, 180
    s = L.svg_head(W, Ht, title)
    xb = [W / 2 + (j - (n_bits - 1) / 2) * step for j in range(n_bits)]
    xc = [W / 2 + (i - (len(checks) - 1) / 2) * step for i in range(len(checks))]
    for i, bits in enumerate(checks):
        for j in bits:
            s += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#5a6a7a" '
                  'stroke-width="1.3" stroke-opacity="0.75"/>\n'
                  % (xc[i], ycheck + 15, xb[j - 1], ybit - 16))
    for i in range(len(checks)):
        s += L.rect(xc[i] - 16, ycheck - 16, 32, 32, "#fde5cc", L.ORANGE, 1.6, 3)
        s += label(xc[i], ycheck + 5, "y", i + 1)
    for j in range(n_bits):
        s += ('<circle cx="%g" cy="%g" r="16" fill="#dbe6f3" stroke="%s" '
              'stroke-width="1.6"/>\n' % (xb[j], ybit, L.BLUE))
        s += label(xb[j], ybit + 5, "x", j + 1)
    s += L.txt(W / 2, Ht - 12, T("katrs y ir ar to savienoto x XOR", "each y is the XOR of the x connected to it"), 11, "#555")
    s += "</svg>\n"
    return s


def main():
    global LANG
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lang", choices=["lv", "en", "all"], default="all",
                    help="uzrakstu valoda (noklusēti abas)")
    langs = {"lv": ["lv"], "en": ["en"], "all": ["lv", "en"]}[ap.parse_args().lang]
    for LANG in langs:
        for name, (title, n_bits, checks) in GRAPHS.items():
            with open(os.path.join(HERE, svg_name(name)), "w", encoding="utf-8", newline="\n") as f:
                f.write(tanner_svg(T(*title), n_bits, checks))
            print("Wrote", svg_name(name))


if __name__ == "__main__":
    main()
