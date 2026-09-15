# -*- coding: utf-8 -*-
"""Ģenerē ans-slots.svg -- dabisko skaitļu sadalījumu starp alfabēta simboliem.

Piemēri:
    python ans-slots.py
    python ans-slots.py -f "A:3,B:1" -c 24 -p 12 -o binary-slots.svg
"""

import ansfig as A


def build(alpha, count, per_row):
    CW, CH = 44, 40
    L, T = 138, 96
    rows = (count + per_row - 1) // per_row
    gap = 84
    W = L + per_row * CW + 24
    H = T + rows * (CH + gap) + 42
    s = A.head(W, H, "ANS: dabisko skaitlu sadalijums starp simboliem")
    s += A.txt(18, 28, "Asimetriskā skaitīšanas sistēma: katram simbolam ir sava "
                       "apakšvirkne dabiskajos skaitļos",
               14, "#222", "start", weight="bold")
    spraugas = "   ".join(
        "%s → {%s}" % (sym, ",".join(str(r) for r in range(
            alpha.cum[sym], alpha.cum[sym] + alpha.freq[sym])))
        for sym in alpha.symbols)
    s += A.txt(18, 50, "M = %d spraugas:   %s" % (alpha.M, spraugas),
               13, "#444", "start")
    s += A.txt(18, 70, "Iekodēt s uz stāvokļa x nozīmē: paņem x-to (skaitot no 0) "
                       "spraugu, kas pieder simbolam s.", 12.5, "#555", "start")

    for row in range(rows):
        y = T + row * (CH + gap)
        s += A.txt(L - 12, y - 10, "dabiskais skaitlis  y :", 11.5, "#666", "end")
        s += A.txt(L - 12, y + 26, "īpašnieks (simbols) :", 11.5, "#666", "end")
        s += A.txt(L - 12, y + CH + 21, "kārtas nr. simbolā  x :", 11.5, "#666", "end")
        for i in range(per_row):
            yv = row * per_row + i
            if yv >= count:
                break
            sym, rk = alpha.rank(yv)
            fill, stroke, tcol = alpha.color[sym]
            x = L + i * CW
            s += A.txt(x + CW / 2, y - 10, str(yv), 12, "#666")
            s += A.rect(x + 2, y, CW - 4, CH, fill, stroke)
            s += A.txt(x + CW / 2, y + 27, sym, 19, tcol, weight="bold",
                       family=A.MONO)
            s += A.txt(x + CW / 2, y + CH + 21, str(rk), 13, stroke,
                       weight="bold", family=A.MONO)

    yf = T + rows * (CH + gap) - 30
    s += A.txt(18, yf, "C(s, x) = M·⌊x / f(s)⌋ + (x mod f(s)) + c(s)", 14,
               "#16324f", "start", weight="bold")
    # divi konkrēti piemēri: pirmais un pēdējais alfabēta simbols
    for k, (sym, xv) in enumerate([(alpha.symbols[len(alpha.symbols) // 2], 3),
                                   (alpha.symbols[-1], 0)]):
        f, c = alpha.freq[sym], alpha.cum[sym]
        s += A.txt(18, yf + 20 + 18 * k,
                   "C(%s, %d) = %d·⌊%d/%d⌋ + (%d mod %d) + %d = %d"
                   % (sym, xv, alpha.M, xv, f, xv, f, c, alpha.C(sym, xv)),
                   12.5, alpha.color[sym][2], "start", family=A.MONO)
    return s


def main():
    ap = A.parser(__file__, "ANS spraugu sadalījuma attēls", freq=True)
    ap.add_argument("-c", "--count", type=int, default=30,
                    help="cik dabiskos skaitļus attēlot (noklusēti 30)")
    ap.add_argument("-p", "--per-row", type=int, default=15,
                    help="cik skaitļu vienā rindā (noklusēti 15)")
    args = ap.parse_args()
    alpha = A.Alphabet(args.freq)
    A.write(args.out, build(alpha, args.count, args.per_row))


if __name__ == "__main__":
    main()
