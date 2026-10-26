# -*- coding: utf-8 -*-
"""Ģenerē dh-cycle-z23.svg -- ģeneratora g = 5 pakāpes grupā Z_23^* kā "ciparnīca".

Atlikumi 0, 1, ..., 22 ir regulāra 23-stūra virsotnēs (ārpusē -- pats atlikums).
Lauztā līnija iet pa 5^0 = 1, 5^1 = 5, 5^2 = 2, ..., 5^21 = 14 un atgriežas 1;
aplītī pie katra atlikuma v ir tā diskrētais logaritms log_5 v. Atlikums 0 grupā
nepieder. Izceltas Difija-Helmana piemēra vērtības A = 8, B = 19 un noslēpums 2.

    python dh_cycle.py [--lang lv|en|both]
"""

import math

import figkit as K
from figkit import T, plt

P, G = 23, 5


def build():
    fig, ax = plt.subplots(figsize=(7.2, 7.4))
    ax.set_aspect("equal")
    ax.axis("off")

    def pos(v, r=1.0):
        t = math.pi / 2 - 2 * math.pi * v / P          # 0 augšā, pulksteņrādītāja virzienā
        return r * math.cos(t), r * math.sin(t)

    log = {pow(G, e, P): e for e in range(P - 1)}
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, ec="#c8ced6", lw=1, ls=(0, (3, 3))))

    # lauztā līnija 1 -> 5 -> 2 -> ... (krāsa mainās ar pakāpi)
    cmap = plt.get_cmap("viridis")
    for e in range(P - 1):
        a, b = pow(G, e, P), pow(G, e + 1, P)
        (x1, y1), (x2, y2) = pos(a, 0.94), pos(b, 0.94)
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=cmap(e / (P - 1)), lw=1.3,
                                    shrinkA=9, shrinkB=9, mutation_scale=9, alpha=0.85))

    special = {8: (K.BLUE, "A"), 19: (K.ORANGE, "B"), 2: (K.RED, T("noslēpums", "secret"))}
    for v in range(P):
        x, y = pos(v, 0.94)
        xo, yo = pos(v, 1.13)
        ax.text(xo, yo, str(v), ha="center", va="center", fontsize=12, weight="bold",
                color="#333" if v else K.GREY)
        if v == 0:
            ax.add_patch(plt.Rectangle((x - 0.045, y - 0.045), 0.09, 0.09, fc="white", ec=K.GREY,
                                       lw=1.2, ls=(0, (2, 2)), zorder=3))
            ax.text(0, 1.22, T("(nav grupā)", "(not in group)"), ha="center", va="bottom", fontsize=8.5,
                    color=K.GREY)
            continue
        col, _ = special.get(v, (None, None))
        ax.add_patch(plt.Circle((x, y), 0.052, fc=col or "white", ec=col or "#333", lw=1.4, zorder=3))
        ax.text(x, y, str(log[v]), ha="center", va="center", fontsize=9.5, zorder=4,
                color="white" if col else "#111", weight="bold" if col else "normal")
        if col:
            xl, yl = pos(v, 1.27)
            ax.text(xl, yl, special[v][1], ha="center", va="center", fontsize=10.5, color=col,
                    weight="bold")

    box = dict(boxstyle="round,pad=0.35", fc="white", ec="#c8ced6", alpha=0.95)
    ax.text(0, 0, r"$\mathbb{Z}_{23}^{*}$,  $g = 5$", ha="center", va="center", fontsize=15, bbox=box,
            zorder=5)
    ax.text(-1.32, -1.42, T("ārpusē: atlikums $v$;  aplītī: kāpinātājs $\\log_5 v$, t.i. $5^{\\log_5 v} = v$",
                            "outside: residue $v$;  in the circle: exponent $\\log_5 v$, i.e. $5^{\\log_5 v} = v$"),
            ha="left", fontsize=10.5, color="#333")
    ax.text(-1.32, -1.56, T("Difijs-Helmans: $A = 5^{6} = 8$,  $B = 5^{15} = 19$,  ",
                            "Diffie-Hellman: $A = 5^{6} = 8$,  $B = 5^{15} = 19$,  ")
            + r"$5^{6\cdot 15} = 5^{90\ \mathrm{mod}\ 22} = 5^{2} = 2$", ha="left", fontsize=10.5)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.62, 1.35)
    ax.set_title(T("Ģeneratora $g = 5$ pakāpes pēc moduļa 23", "Powers of the generator $g = 5$ modulo 23"),
                 fontsize=13)
    return fig


if __name__ == "__main__":
    K.main(build, "dh-cycle-z23.svg")
