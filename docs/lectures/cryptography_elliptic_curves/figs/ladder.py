# -*- coding: utf-8 -*-
"""Ģenerē montgomery-ladder.svg -- Montgomerija kāpnes k = 77 = 1001101_2 uz līknes
y^2 = x^3 - 3x + 7 virs F_271 (kārta 269), P = (0, 121).

Katra kolonna ir viens solis (viens atslēgas bits). Augšējā rindā R0 = jP, apakšējā --
R1 = (j + 1)P; aplītī ir j vai j + 1, zem tā -- koordinātes. Zilās bultas ir dubultošana,
oranžās -- saskaitīšana R0 + R1. Katrā solī ir tieši viena dubultošana un viena
saskaitīšana, un invariants R1 - R0 = P saglabājas.

    python ladder.py [--lang lv|en|both] [--k 77]
"""

import sys

import figkit as K
from figkit import T, plt
from ecc import Curve, O, fmt

E, P = Curve(-3, 7, 271), (0, 121)
KVAL = 77
if "--k" in sys.argv:                  # papildu parametrs (pirms argparse figkit.main)
    i = sys.argv.index("--k")
    KVAL = int(sys.argv[i + 1])
    del sys.argv[i:i + 2]


def build():
    bits = bin(KVAL)[2:]
    steps = [("", O, P, 0)] + [(b, r0, r1, None) for b, r0, r1 in E.ladder_trace(KVAL, P)]
    j, mults = 0, [0]
    for b in bits:
        j = 2 * j + int(b)
        mults.append(j)
    n = len(steps)
    fig, ax = plt.subplots(figsize=(1.55 * n + 0.6, 4.4))
    ax.axis("off")
    y0, y1, dx = 2.0, 0.0, 1.55
    ax.text(-0.95, y0, "$R_0$", ha="center", va="center", fontsize=14, weight="bold")
    ax.text(-0.95, y1, "$R_1$", ha="center", va="center", fontsize=14, weight="bold")
    for i, (b, r0, r1, _) in enumerate(steps):
        x = i * dx
        m = mults[i]
        for y, R, mm, col in [(y0, r0, m, K.L_BLUE), (y1, r1, m + 1, K.L_ORANGE)]:
            ax.add_patch(plt.Circle((x, y), 0.36, fc=col, ec="#333", lw=1.2, zorder=3))
            ax.text(x, y, "$%s$" % (("%dP" % mm) if mm > 1 else ("P" if mm == 1 else "O")),
                    ha="center", va="center", fontsize=11.5 if mm < 100 else 9.8, zorder=4)
            ax.text(x, y - 0.55, fmt(R), ha="center", va="center", fontsize=8.8, color="#333")
        lab = T("sākums", "start") if i == 0 else T("bits ", "bit ") + b
        ax.text(x, y0 + 0.75, lab, ha="center", fontsize=11, weight="bold" if i else "normal",
                color=K.RED if b == "1" else "#333")
        if i == 0:
            continue
        xp = x - dx
        arr = dict(arrowstyle="-|>", lw=1.4, shrinkA=13, shrinkB=13, mutation_scale=11)
        if b == "0":                      # R0 <- 2 R0, R1 <- R0 + R1
            ax.annotate("", xy=(x, y0), xytext=(xp, y0), arrowprops=dict(color=K.BLUE, **arr))
            ax.annotate("", xy=(x, y1), xytext=(xp, y0), arrowprops=dict(color=K.ORANGE, **arr))
            ax.annotate("", xy=(x, y1), xytext=(xp, y1), arrowprops=dict(color=K.ORANGE, **arr))
        else:                             # R0 <- R0 + R1, R1 <- 2 R1
            ax.annotate("", xy=(x, y0), xytext=(xp, y0), arrowprops=dict(color=K.ORANGE, **arr))
            ax.annotate("", xy=(x, y0), xytext=(xp, y1), arrowprops=dict(color=K.ORANGE, **arr))
            ax.annotate("", xy=(x, y1), xytext=(xp, y1), arrowprops=dict(color=K.BLUE, **arr))
    ax.plot([], [], color=K.BLUE, lw=2, label=T("dubultošana", "doubling"))
    ax.plot([], [], color=K.ORANGE, lw=2, label=T("saskaitīšana $R_0 + R_1$", "addition $R_0 + R_1$"))
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.02), ncol=2, frameon=False, fontsize=10.5)
    ax.set_xlim(-1.3, (n - 1) * dx + 0.6)
    ax.set_ylim(-0.95, 3.1)
    ax.set_aspect("equal")
    ax.set_title(T("Montgomerija kāpnes: $k = %d = %s_2$, līkne $y^2 = x^3 - 3x + 7$ virs $\\mathbf{F}_{271}$, "
                   "$P = (0, 121)$" % (KVAL, bits),
                   "Montgomery ladder: $k = %d = %s_2$, curve $y^2 = x^3 - 3x + 7$ over $\\mathbf{F}_{271}$, "
                   "$P = (0, 121)$" % (KVAL, bits)), fontsize=12)
    return fig


if __name__ == "__main__":
    K.main(build, "montgomery-ladder.svg" if KVAL == 77 else "montgomery-ladder-%d.svg" % KVAL)
