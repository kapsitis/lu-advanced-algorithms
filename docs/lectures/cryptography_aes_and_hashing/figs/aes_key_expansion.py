# -*- coding: utf-8 -*-
"""Ģenerē aes-key-expansion.svg -- AES-128 atslēgu izvēršanas pirmais solis (w4..w7).

Atslēga ir FIPS 197 A.1 pielikuma piemērs 2b7e1516 28aed2a6 abf71588 09cf4f3c;
vērtības aprēķina modulis aes128.py.

    w[i] = w[i-4] XOR SubWord(RotWord(w[i-1])) XOR Rcon[i/4],   ja i dalās ar 4,
    w[i] = w[i-4] XOR w[i-1]                                     citādi.

    python aes_key_expansion.py [--lang lv|en|both]
"""

import svgkit as K
from svgkit import T, txt, rect, arrow, xor, path_arrow, sub
from aes128 import key_expansion, rot_word, sub_word, hx


def word(x, y, w, label, fill, edge, wbox=96, h=30):
    s = rect(x, y, wbox, h, fill, edge, 1.4, 4)
    s += txt(x + wbox / 2, y + h / 2 + 4.5, hx(w, ""), 12.5, family=K.MONO)
    if label:
        s += txt(x + wbox / 2, y - 7, label, 12, weight="bold", raw=True)
    return s


def build():
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    w = key_expansion(key)
    rw = rot_word(w[3])
    sw = sub_word(rw)
    rc = [sw[0] ^ 0x01] + sw[1:]

    title = T("AES-128 atslēgu izvēršana: no K₀ = (w₀, w₁, w₂, w₃) iegūst K₁ = (w₄, w₅, w₆, w₇)",
              "AES-128 key expansion: from K₀ = (w₀, w₁, w₂, w₃) to K₁ = (w₄, w₅, w₆, w₇)")
    W, H = 980, 420
    s = K.header(W, H, title)
    s += txt(20, 26, title, 15, anchor="start", weight="bold")

    # augšējā rinda: w0..w3 (atslēga K)
    y0, xw = 70, [40, 190, 340, 490]
    for i in range(4):
        s += word(xw[i], y0, w[i], "w" + sub(str(i)), K.L_BLUE, K.BLUE)

    # funkcija g: RotWord, SubWord, XOR Rcon
    gx, gy = 690, 128
    s += rect(gx - 16, gy - 20, 290, 168, "none", "#9aa5b1", 1.2, 8, ' stroke-dasharray="5 4"')
    s += txt(gx + 260, gy + 140, T("funkcija g (tikai w₄, w₈, …)", "function g (only w₄, w₈, …)"),
             11.5, K.GREY, "end")
    s += path_arrow("M %g %g L %g %g L %g %g" % (xw[3] + 100, y0 + 15, gx + 48, y0 + 15, gx + 48, gy - 2))
    steps = [("RotWord", rw, T("cikliska nobīde par 1 baitu", "rotate left by 1 byte")),
             ("SubWord", sw, T("S-bloks katram baitam", "S-box on each byte")),
             ("⊕ Rcon" + sub("1"), rc, "Rcon" + sub("1") + " = 01 00 00 00")]
    for k, (lab, val, note) in enumerate(steps):
        y = gy + 45 * k
        s += word(gx, y, val, "", K.L_ORANGE, K.ORANGE)
        s += txt(gx + 108, y + 13, lab, 12, weight="bold", anchor="start", raw=True)
        s += txt(gx + 108, y + 28, note, 10.5, K.GREY, anchor="start", raw=True)
        if k < 2:
            s += arrow(gx + 48, y + 30, gx + 48, y + 44)

    # XOR rinda un rezultāts w4..w7
    yx, yb = 305, 340
    gout = gy + 90 + 30
    s += path_arrow("M %g %g L %g %g L %g %g L %g %g" % (gx + 48, gout, gx + 48, 278, xw[0] + 78, 278,
                                                        xw[0] + 78, yx), col=K.ORANGE)
    s += arrow(xw[0] + 78, yx, xw[0] + 60, yx, K.ORANGE)
    for i in range(4):
        cx = xw[i] + 48
        s += arrow(cx, y0 + 32, cx, yx - 12)
        s += xor(cx, yx, 10)
        s += arrow(cx, yx + 10, cx, yb - 2)
        s += word(xw[i], yb, w[4 + i], "", K.L_GREEN, K.GREEN)
        s += txt(cx, yb + 50, "w" + sub(str(4 + i)), 12, weight="bold", raw=True)
        if i:
            s += path_arrow("M %g %g L %g %g L %g %g" % (xw[i - 1] + 98, yb + 15, xw[i - 1] + 118, yb + 15,
                                                         cx - 11, yx + 3))
    s += txt(gx - 16, yb + 20, T("w₄ = w₀ ⊕ g(w₃),  w₅ = w₁ ⊕ w₄,", "w₄ = w₀ ⊕ g(w₃),  w₅ = w₁ ⊕ w₄,"),
             12, K.INK, "start")
    s += txt(gx - 16, yb + 40, T("w₆ = w₂ ⊕ w₅,  w₇ = w₃ ⊕ w₆", "w₆ = w₂ ⊕ w₅,  w₇ = w₃ ⊕ w₆"),
             12, K.INK, "start")
    return s + "</svg>\n"


if __name__ == "__main__":
    K.main(build, "aes-key-expansion.svg")
