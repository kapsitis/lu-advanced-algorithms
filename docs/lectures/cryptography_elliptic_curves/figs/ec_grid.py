# -*- coding: utf-8 -*-
"""Ģenerē divus attēlus ar līknes punktiem režģī F_p x F_p:

* ec-f17-multiples.svg -- y^2 = x^3 + 2x + 2 virs F_17, G = (5, 1): katrs līknes punkts
  apvilkts ar aplīti, kurā ierakstīts k (punkts ir kG); bultas rāda ceļu G -> 2G -> 3G -> ...
* ec-f23-grid.svg -- y^2 = x^3 + x + 4 virs F_23, G = (0, 2), kārta n = 29: visi pāri (x, y)
  kā pelēki punkti, līknes punkti -- aplīši ar k; izcelti ECDSA piemēra punkti
  Q = 7G (publiskā atslēga) un R = 11G (kG parakstā).

    python ec_grid.py [--lang lv|en|both]
"""

import figkit as K
from figkit import T, plt
from ecc import E17, G17, E23, G23, O


def grid(E, G, title, highlight=None, path=False, size=7.6):
    p = E.p
    fig, ax = plt.subplots(figsize=(size, size))
    mult, k, R = {}, 1, G
    while R is not O:
        mult[R] = k
        R, k = E.add(R, G), k + 1
    xs = [x for x in range(p) for _ in range(p)]
    ys = [y for _ in range(p) for y in range(p)]
    ax.scatter(xs, ys, s=4, color="#b8bec6", zorder=1)
    ax.axhline(p / 2, color=K.GREY, lw=0.8, ls=(0, (4, 4)))
    ax.text(p - 0.4, p / 2 + 0.35, "$y = p/2$", ha="right", va="bottom", fontsize=9, color=K.GREY)
    if path:
        for k in range(1, len(mult)):
            a = next(P for P, j in mult.items() if j == k)
            b = next(P for P, j in mult.items() if j == k + 1)
            ax.annotate("", xy=b, xytext=a,
                        arrowprops=dict(arrowstyle="-|>", color=K.ORANGE, lw=0.9, alpha=0.55,
                                        shrinkA=10, shrinkB=10, mutation_scale=9))
    highlight = highlight or {}
    for P, k in mult.items():
        col = highlight.get(k, (None,))[0]
        ax.add_patch(plt.Circle(P, 0.42, fc=col or "white", ec=col or K.BLUE, lw=1.5, zorder=3))
        ax.text(P[0], P[1], str(k), ha="center", va="center", fontsize=8.5 if k < 10 else 7.8, zorder=4,
                color="white" if col else "#111", weight="bold" if col else "normal")
    for k, (col, lab) in highlight.items():
        P = next(P for P, j in mult.items() if j == k)
        ax.annotate(lab, P, xytext=(12, 8), textcoords="offset points", fontsize=10.5, color=col,
                    weight="bold", bbox=dict(fc="white", ec="none", alpha=0.85, pad=1), zorder=6)
    ax.set_xlim(-0.8, p - 0.2)
    ax.set_ylim(-0.8, p - 0.2)
    ax.set_xticks(range(p))
    ax.set_yticks(range(p))
    ax.tick_params(labelsize=8)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(title, fontsize=12)
    for s in ax.spines.values():
        s.set_color("#c8ced6")
    return fig


def build_f17():
    return grid(E17, G17, T("$y^2 = x^3 + 2x + 2$ virs $\\mathbf{F}_{17}$: punkts $kG$ apzīmēts ar $k$, "
                            "$G = (5, 1)$, $19G = O$",
                            "$y^2 = x^3 + 2x + 2$ over $\\mathbf{F}_{17}$: point $kG$ is labelled $k$, "
                            "$G = (5, 1)$, $19G = O$"),
                highlight={1: (K.RED, "$G$")}, path=True, size=7.4)


def build_f23():
    return grid(E23, G23, T("$y^2 = x^3 + x + 4$ virs $\\mathbf{F}_{23}$: $G = (0, 2)$, kārta $n = 29$",
                            "$y^2 = x^3 + x + 4$ over $\\mathbf{F}_{23}$: $G = (0, 2)$, order $n = 29$"),
                highlight={1: (K.RED, "$G$"), 7: (K.GREEN, T("$Q = 7G$ (publiskā atslēga)",
                                                             "$Q = 7G$ (public key)")),
                           11: (K.PURPLE, "$R = 11G$ ($k = 11$)")}, size=8.4)


if __name__ == "__main__":
    K.main(build_f17, "ec-f17-multiples.svg")
    K.main(build_f23, "ec-f23-grid.svg")
