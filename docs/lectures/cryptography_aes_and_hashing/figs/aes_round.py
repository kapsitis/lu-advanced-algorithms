# -*- coding: utf-8 -*-
"""Ģenerē aes-round.svg -- vienas AES-128 kārtas četri soļi ar 4x4 baitu stāvokli.

Skaitļi ir FIPS 197 B pielikuma piemēra 1. kārta (atklātais teksts
3243f6a8 885a308d 313198a2 e0370734, atslēga 2b7e1516 28aed2a6 abf71588 09cf4f3c);
tos aprēķina modulis aes128.py, tāpēc tie vienmēr sakrīt ar standartu.
Krāsas rāda sākotnējās kolonnas: pēc ShiftRows katrā kolonnā ir pa vienam baitam
no katras sākotnējās kolonnas, un MixColumns tos sajauc.

    python aes_round.py [--lang lv|en|both]
"""

import svgkit as K
from svgkit import T, txt, rect, arrow, line, xor
from aes128 import encrypt_trace, hx

COLS = [K.L_BLUE, K.L_ORANGE, K.L_GREEN, K.L_PURPLE]
EDGE = [K.BLUE, K.ORANGE, K.GREEN, K.PURPLE]
CELL = 30


def grid(x, y, state, colour_of, title, sub_title=None, bold_col=None):
    """4x4 stāvoklis; colour_of(r, c) -> sākotnējās kolonnas indekss vai None."""
    s = txt(x + 2 * CELL, y - 26, title, 12.5, weight="bold", raw=True)
    if sub_title:
        s += txt(x + 2 * CELL, y - 10, sub_title, 10.5, K.GREY)
    for c in range(4):
        for r in range(4):
            k = colour_of(r, c)
            fill = COLS[k] if k is not None else "#ffffff"
            s += rect(x + c * CELL, y + r * CELL, CELL, CELL, fill, "#8a96a3", 0.8)
            s += txt(x + c * CELL + CELL / 2, y + r * CELL + CELL / 2 + 4.5, "%02x" % state[r + 4 * c],
                     12, family=K.MONO)
    s += rect(x, y, 4 * CELL, 4 * CELL, "none", "#333", 1.4)
    if bold_col is not None:
        s += rect(x + bold_col * CELL, y, CELL, 4 * CELL, "none", K.RED, 2.6)
    return s


def build():
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    _, tr = encrypt_trace(bytes.fromhex("3243f6a8885a308d313198a2e0370734"), key)
    d = {(n, r): s for n, r, s in tr}
    st, sb, sr, mc, rk, nx = (d[("start", 1)], d[("s_box", 1)], d[("s_row", 1)],
                              d[("m_col", 1)], d[("k_sch", 1)], d[("start", 2)])

    title = T("Viena AES-128 kārta (FIPS 197, B pielikums, 1. kārta)",
              "One AES-128 round (FIPS 197, Appendix B, round 1)")
    W, H = 1060, 440
    s = K.header(W, H, title)
    s += txt(20, 26, title, 15, anchor="start", weight="bold")

    y = 92
    xs = [20, 215, 410, 605, 900]
    same = lambda r, c: c
    shifted = lambda r, c: (c + r) % 4
    s += grid(xs[0], y, st, same, T("stāvoklis", "state"), T("kārtas sākumā", "at the round start"))
    s += grid(xs[1], y, sb, same, "SubBytes", T("katram baitam S-bloks", "S-box on every byte"))
    s += grid(xs[2], y, sr, shifted, "ShiftRows", T("rindas nobīda pa kreisi", "rows rotated left"))
    s += grid(xs[3], y, mc, lambda r, c: None if c else 0, "MixColumns",
              T("kolonna × matrica", "column × matrix"), bold_col=0)
    s += grid(xs[4], y, nx, lambda r, c: None, T("rezultāts", "result"),
              T("nākamās kārtas ieeja", "input of the next round"))

    # bultas starp soļiem
    for a, b in zip(xs[:3], xs[1:4]):
        s += arrow(a + 4 * CELL + 8, y + 2 * CELL, b - 8, y + 2 * CELL)
    # AddRoundKey: XOR ar kārtas atslēgu
    cx = 812
    s += line(xs[3] + 4 * CELL + 6, y + 2 * CELL, cx - 11, y + 2 * CELL)
    s += xor(cx, y + 2 * CELL, 11)
    s += arrow(cx + 11, y + 2 * CELL, xs[4] - 8, y + 2 * CELL)
    s += txt(cx, y - 26, "AddRoundKey", 12.5, weight="bold")

    # kārtas atslēga zem XOR
    ky = 300
    s += grid(cx - 2 * CELL, ky, rk, lambda r, c: None, T("kārtas atslēga K", "round key K") + K.sub("1"))
    s += arrow(cx, ky - 42, cx, y + 2 * CELL + 13)

    # piezīmes zem pirmajiem attēliem
    ny = 252
    s += txt(xs[1] + 2 * CELL, ny, "S(19) = d4", 12, K.INK, family=K.MONO)
    s += txt(xs[2] + 2 * CELL, ny, T("rinda r: nobīde par r", "row r: shift by r"), 11.5, K.GREY)
    s += txt(xs[3] + 2 * CELL, ny, "(d4,bf,5d,30) → (04,66,81,e5)", 11, K.INK, family=K.MONO)
    s += txt(20, 350, T("Krāsas rāda, no kuras sākotnējās kolonnas nāk baits.",
                        "Colours show which original column a byte comes from."), 11.5, K.GREY, "start")
    s += txt(20, 370, T("Pēdējā (10.) kārtā MixColumns neizpilda.",
                        "The last (10th) round skips MixColumns."), 11.5, K.GREY, "start")
    s += txt(20, 390, T("Baiti stāvoklī: s[r, c] = in[r + 4c] (pa kolonnām).",
                        "Bytes in the state: s[r, c] = in[r + 4c] (column by column)."), 11.5, K.GREY,
             "start")
    return s + "</svg>\n"


if __name__ == "__main__":
    K.main(build, "aes-round.svg")
