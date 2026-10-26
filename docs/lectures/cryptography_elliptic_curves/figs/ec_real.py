# -*- coding: utf-8 -*-
"""Ģenerē ec-real-addition.svg -- hordas un pieskares konstrukcija uz līknes y^2 = x^3 - 2x + 1.

Kreisajā pusē -- saskaitīšana P + Q: taisne caur P un Q krusto līkni trešajā punktā
-(P + Q), un to atspoguļo pret x asi. Labajā pusē -- dubultošana 2P: tās pašas
konstrukcijas vietā ņem pieskari punktā P. Līkne virs reālajiem skaitļiem ir tikai
ilustrācija; kriptogrāfijā tās pašas formulas lieto laukā F_p.

    python ec_real.py [--lang lv|en|both]
"""

import numpy as np

import figkit as K
from figkit import T, plt

A, B = -2.0, 1.0                       # y^2 = x^3 + A x + B
LBL = dict(fc="white", ec="none", alpha=0.85, pad=1)


def y_of(x, sign=1):
    return sign * np.sqrt(x ** 3 + A * x + B)


def add(P, Q):
    (x1, y1), (x2, y2) = P, Q
    lam = (3 * x1 ** 2 + A) / (2 * y1) if P == Q else (y2 - y1) / (x2 - x1)
    x3 = lam ** 2 - x1 - x2
    return lam, (x3, lam * (x1 - x3) - y1)


def panel(ax, P, Q, title, labels):
    xs = np.linspace(-2.3, 3.2, 600)
    ys = np.linspace(-4, 4, 600)
    X, Y = np.meshgrid(xs, ys)
    ax.contour(X, Y, Y ** 2 - X ** 3 - A * X - B, [0], colors=[K.BLUE], linewidths=2)
    ax.axhline(0, color="#999", lw=0.8)
    ax.axvline(0, color="#999", lw=0.8)
    lam, R = add(P, Q)
    negR = (R[0], -R[1])
    t = np.linspace(-2.3, 3.2, 10)
    ax.plot(t, P[1] + lam * (t - P[0]), color=K.ORANGE, lw=1.5,
            label=T("horda", "chord") if P != Q else T("pieskare", "tangent"))
    ax.plot([R[0], R[0]], [negR[1], R[1]], color=K.GREY, lw=1.2, ls="--")
    for pt, lab, col, dx in [(P, labels[0], "#222", -0.12), (Q, labels[1], "#222", 0.12)]:
        ax.plot(*pt, "o", color=col, ms=7, zorder=5)
        ax.annotate(lab, pt, xytext=(-14 if dx < 0 else 8, 8), textcoords="offset points", fontsize=13,
                    weight="bold")
    ax.plot(*negR, "o", mfc="white", mec=K.RED, ms=8, mew=1.6, zorder=5)
    ax.annotate(labels[2], negR, xytext=(-6, 10), textcoords="offset points", ha="right",
                fontsize=12, color=K.RED, bbox=LBL)
    ax.plot(*R, "o", color=K.RED, ms=8, zorder=5)
    ax.annotate(labels[3], R, xytext=(10, -14), textcoords="offset points", fontsize=13, color=K.RED,
                weight="bold", bbox=LBL)
    ax.set_xlim(-2.3, 3.2)
    ax.set_ylim(-4, 4)
    ax.set_title(title, fontsize=12.5)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.grid(alpha=0.25)


def build():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.2))
    P, Q = (-1.45, float(y_of(-1.45))), (2.05, float(y_of(2.05)))
    panel(a1, P, Q, T("Saskaitīšana: $P + Q$", "Addition: $P + Q$"),
          ["$P$", "$Q$", "$-(P+Q)$", "$P+Q$"])
    P2 = (-1.0, float(y_of(-1.0)))
    panel(a2, P2, P2, T("Dubultošana: $2P = P + P$", "Doubling: $2P = P + P$"),
          ["$P$", "", "$-2P$", "$2P$"])
    fig.suptitle(T("Līkne $y^2 = x^3 - 2x + 1$ virs reālajiem skaitļiem",
                   "The curve $y^2 = x^3 - 2x + 1$ over the reals"), fontsize=13.5)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    K.main(build, "ec-real-addition.svg")
