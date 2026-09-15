# -*- coding: utf-8 -*-
"""Ģenerē ans-renorm.svg -- straumējošā rANS stāvokļa logu un renormalizāciju.

Šis ir statisks shēmas attēls; vienīgā komandrindas iespēja ir izvades fails.

    python ans-renorm.py
"""

import ansfig as A


def build():
    W, H = 800, 296
    s = A.head(W, H, "Straumējošs rANS: stāvokļa renormalizācija")
    s += A.txt(20, 28, "Kāpēc praksē x neaug bez gala: renormalizācija", 14.5,
               "#222", "start", weight="bold")
    s += A.txt(20, 50, "Stāvokli visu laiku tur šaurā „logā“;  liekos zemos "
                       "bitus izraksta baitu straumē.", 13, "#444", "start")

    bx, by, bw, bh = 70, 96, 660, 46
    s += A.rect(bx, by, bw, bh, "#eef3f8", "#5a6a7a", rx=6)
    s += A.rect(bx, by, 140, bh, "#f7d9d9", "#b23b3b", rx=6, sw=1.2)
    s += A.rect(bx + bw - 140, by, 140, bh, "#f7d9d9", "#b23b3b", rx=6, sw=1.2)
    s += A.txt(bx + 70, by + 28, "par mazs", 12.5, "#7a1f1f")
    s += A.txt(bx + bw - 70, by + 28, "par liels", 12.5, "#7a1f1f")
    s += A.txt(bx + bw / 2, by + 28, "derīgais logs   L ≤ x < 2ᵇ · L", 14.5,
               "#16324f", weight="bold")
    s += A.txt(bx, by - 10, "L", 13, "#333", family=A.MONO)
    s += A.txt(bx + bw, by - 10, "2ᵇ · L", 13, "#333", family=A.MONO)

    # atkodētājs (pa kreisi): lasa bitus, lai audzētu x
    s += A.arrow(bx + 70, by + bh + 40, bx + 70, by + bh + 6, "#2a6b2a")
    s += A.txt(bx + 70, by + bh + 58, "ATKODĒTĀJS", 12.5, "#1f5a1f", weight="bold")
    s += A.txt(bx + 70, by + bh + 76, "kamēr x < L:  ielasa b bitus,", 12.5, "#1f5a1f")
    s += A.txt(bx + 70, by + bh + 93, "x ← x · 2ᵇ + biti", 12.5, "#1f5a1f")

    # kodētājs (pa labi): izvada bitus, lai samazinātu x
    s += A.arrow(bx + bw - 70, by + bh + 40, bx + bw - 70, by + bh + 6, "#b23b3b")
    s += A.txt(bx + bw - 70, by + bh + 58, "KODĒTĀJS", 12.5, "#7a1f1f", weight="bold")
    s += A.txt(bx + bw - 70, by + bh + 76,
               "kamēr x ≥ 2ᵇ·L:  izvada b zemos bitus,", 12.5, "#7a1f1f")
    s += A.txt(bx + bw - 70, by + bh + 93, "x ← ⌊x / 2ᵇ⌋", 12.5, "#7a1f1f")

    s += A.txt(20, 278, "Tāpēc rANS pietiek ar fiksēta platuma veseliem skaitļiem "
                        "(32 vai 64 biti) — bez lielo skaitļu aritmētikas.",
               12.5, "#444", "start")
    return s


def main():
    args = A.parser(__file__, "Renormalizācijas shēma").parse_args()
    A.write(args.out, build())


if __name__ == "__main__":
    main()
