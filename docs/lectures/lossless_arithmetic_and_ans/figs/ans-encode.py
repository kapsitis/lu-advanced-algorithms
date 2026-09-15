# -*- coding: utf-8 -*-
"""Ģenerē ans-encode.svg -- rANS stāvokļa augšanu, kodējot ziņojumu.

Piemēri:
    python ans-encode.py
    python ans-encode.py -f "A:3,B:1" -m "ABAA" -x 4 -o abaa-encode.svg
"""

import math

import ansfig as A


def build(alpha, message, x0, per_row):
    syms = alpha.split(message)
    states = alpha.encode(message, x0)
    enc_order = list(reversed(syms))          # secība, kādā simbolus apstrādā
    n = len(states)

    BW, BH, AW = 96, 46, 70
    L = 26
    per_row = max(2, min(per_row, n))
    # rindas: katra nākamā sākas ar iepriekšējās pēdējo (atkārtoto) stāvokli
    rows, start = [], 0
    while start < n - 1:
        stop = min(start + per_row - 1, n - 1)
        rows.append((start, stop))
        start = stop
    W = max(L + per_row * BW + (per_row - 1) * AW + 26, 690)
    top = 150
    row_h = 128
    H = top + len(rows) * row_h + 96

    s = A.head(W, H, "rANS: ziņojuma %s iekodēšana" % message)
    s += A.txt(20, 28, "rANS kodēšana: ziņojumu apstrādā no beigām uz sākumu (LIFO)",
               14.5, "#222", "start", weight="bold")
    s += A.txt(20, 50, "x ← %d,   pēc tam katram simbolam s:   x ← C(s, x)" % x0,
               13, "#444", "start")

    # ziņojuma josla
    s += A.txt(20, 96, "ziņojums:", 12.5, "#666", "start")
    for j, ch in enumerate(syms):
        fill, stroke, tcol = alpha.color[ch]
        s += A.rect(96 + j * 32, 80, 28, 22, fill, stroke, rx=3, sw=1.1)
        s += A.txt(110 + j * 32, 97, ch, 14, tcol, weight="bold", family=A.MONO)
    s += A.txt(96 + len(syms) * 32 + 14, 97, "← kodēšanas virziens", 12.5,
               "#B22222", "start")

    for ri, (a, b) in enumerate(rows):
        y = top + ri * row_h
        if ri:
            s += A.txt(L + BW / 2, y - 22, "(turpinājums)", 11.5, "#7b8794")
        for k in range(a, b + 1):
            x = L + (k - a) * (BW + AW)
            v = states[k]
            faded = (k == a and a > 0)
            s += A.rect(x, y, BW, BH, "#eef1f4" if faded else "#f4f6f8",
                        "#9aa7b4" if faded else "#5a6a7a", rx=6)
            s += A.txt(x + BW / 2, y + 30, str(v), 19,
                       "#7b8794" if faded else "#16324f", weight="bold",
                       family=A.MONO)
            bits = math.log2(v) if v > 0 else 0.0
            s += A.txt(x + BW / 2, y + BH + 20,
                       "—" if v == 0 else "log₂x = %.2f" % bits, 11.5, "#555")
            if k < b:
                sym = enc_order[k]
                fill, stroke, tcol = alpha.color[sym]
                ax = x + BW + 6
                s += A.arrow(ax, y + BH / 2, ax + AW - 14, y + BH / 2, stroke)
                s += A.rect(ax + 16, y - 26, 34, 23, fill, stroke, rx=3, sw=1.2)
                s += A.txt(ax + 33, y - 8, sym, 15, tcol, weight="bold",
                           family=A.MONO)
                if states[k + 1] > 0:
                    inc = math.log2(states[k + 1]) - bits
                    s += A.txt(ax + AW / 2 - 4, y + BH + 20, "+%.2f" % inc,
                               11.5, stroke, weight="bold")

    # kopsavilkums
    costs = ["%s → +%.2f" % (sym, math.log2(alpha.M / alpha.freq[sym]))
             for sym in alpha.symbols]
    final = states[-1]
    entropy = sum(math.log2(alpha.M / alpha.freq[sym]) for sym in syms)
    yb = top + len(rows) * row_h + 32
    s += A.txt(20, yb, "Katrs simbols palielina stāvokli aptuveni par "
                       "log₂(1/p(s)) bitiem:  " + "   ".join(costs),
               12.5, "#222", "start")
    s += A.txt(20, yb + 22,
               "Nosūtāmā vērtība:  x = %d = %s₂  (%d biti;  entropija %.2f biti)"
               % (final, format(final, "b"), final.bit_length(), entropy),
               13.5, "#16324f", "start", weight="bold")
    return s


def main():
    ap = A.parser(__file__, "rANS kodēšanas attēls", freq=True, message=True)
    ap.add_argument("-x", "--start", type=int, default=0,
                    help="sākuma stāvoklis x0 (noklusēti 0)")
    ap.add_argument("-p", "--per-row", type=int, default=4,
                    help="cik stāvokļu vienā rindā (noklusēti 4)")
    args = ap.parse_args()
    alpha = A.Alphabet(args.freq)
    A.write(args.out, build(alpha, args.message, args.start, args.per_row))


if __name__ == "__main__":
    main()
