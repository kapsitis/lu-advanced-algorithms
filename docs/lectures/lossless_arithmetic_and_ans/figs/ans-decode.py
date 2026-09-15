# -*- coding: utf-8 -*-
"""Ģenerē ans-decode.svg -- rANS atkodēšanas soļu tabulu.

Piemēri:
    python ans-decode.py
    python ans-decode.py -f "A:3,B:1" -m "ABAA" -x 4 -o abaa-decode.svg
"""

import ansfig as A


def build(alpha, message, x0):
    syms = alpha.split(message)
    x = alpha.encode(message, x0)[-1]

    steps = []
    for _ in syms:
        r = x % alpha.M
        sym, nx = alpha.D(x)
        steps.append((x, r, sym, nx))
        x = nx

    M = alpha.M
    RH, T = 34, 100
    col_x = [80, 200, 303, 366]
    exprs = ["%d·%d + %d − %d  =  %d"
             % (alpha.freq[s], xv // M, r, alpha.cum[s], nx)
             for xv, r, s, nx in steps]
    tw = col_x[3] + max(A.mono_width(e, 13.5) for e in exprs) + 24
    W = int(max(tw, 664))
    H = T + (len(steps) + 1) * RH + 58

    s = A.head(W, H, "rANS: atkodēšana")
    s += A.txt(20, 28, "rANS atkodēšana: simboli iznāk pareizā "
                       "(sākuma → beigu) secībā", 14.5, "#222", "start",
               weight="bold")
    s += A.txt(20, 50, "D(x) = (s, x′),  kur simbolu s nosaka atlikums  x mod %d"
               % M, 13, "#444", "start")
    s += A.txt(col_x[0], T - 12, "x  (stāvoklis)", 11.5, "#666")
    s += A.txt(col_x[1], T - 12, "x mod %d" % M, 11.5, "#666")
    s += A.txt(col_x[2], T - 12, "simbols", 11.5, "#666")
    s += A.txt(col_x[3], T - 12,
               "jaunais  x′ = f(s)·⌊x/%d⌋ + (x mod %d) − c(s)" % (M, M),
               11.5, "#666", "start")

    for i, ((xv, r, sym, nx), expr) in enumerate(zip(steps, exprs)):
        y = T + i * RH
        fill, stroke, tcol = alpha.color[sym]
        s += A.rect(20, y, W - 40, RH - 4,
                    "#fbfcfd" if i % 2 == 0 else "#f2f5f8", "#dde3e9", rx=3, sw=1)
        s += A.txt(col_x[0], y + 22, str(xv), 15, "#16324f", weight="bold",
                   family=A.MONO)
        s += A.txt(col_x[1], y + 22, str(r), 15, "#333", family=A.MONO)
        s += A.rect(col_x[2] - 17, y + 4, 34, RH - 12, fill, stroke, rx=3, sw=1.2)
        s += A.txt(col_x[2], y + 22, sym, 15, tcol, weight="bold", family=A.MONO)
        s += A.txt(col_x[3], y + 22, expr, 13.5, "#333", "start",
                   family=A.MONO, pre=True)

    y = T + len(steps) * RH
    s += A.txt(20, y + 22,
               "x = %d  →  viss ziņojums atkodēts, stāvoklis atgriezies sākumā."
               % x0, 13, "#B22222", "start")
    s += A.txt(20, y + 48, "Atkodētais ziņojums:  " + " ".join(syms),
               14.5, "#16324f", "start", weight="bold")
    return s


def main():
    ap = A.parser(__file__, "rANS atkodēšanas attēls", freq=True, message=True)
    ap.add_argument("-x", "--start", type=int, default=0,
                    help="sākuma stāvoklis x0 (noklusēti 0)")
    args = ap.parse_args()
    alpha = A.Alphabet(args.freq)
    A.write(args.out, build(alpha, args.message, args.start))


if __name__ == "__main__":
    main()
