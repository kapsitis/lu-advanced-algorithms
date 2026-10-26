# -*- coding: utf-8 -*-
"""Ģenerē gcm-mode.svg -- AES-GCM shēma diviem atklātā teksta blokiem (NIST SP 800-38D).

Augšā -- CTR šifrēšana: skaitītāja bloki N || 00000002, N || 00000003 (N ir 96 bitu
nonce), E_K un XOR ar atklāto tekstu. Apakšā -- GHASH: Hornera shēma laukā GF(2^128),
kas novērtē polinomu punktā H = E_K(0^128); rezultātu S pieskaita E_K(N || 00000001),
un iegūst autentifikācijas tagu T.

    python gcm_mode.py [--lang lv|en|both]
"""

import svgkit as K
from svgkit import T, txt, rect, arrow, line, xor, mul, sub, sup, path_arrow


def box(cx, y, w, h, label, fill, edge, size=12, family=K.FONT, raw=False, weight="normal"):
    return (rect(cx - w / 2, y, w, h, fill, edge, 1.4, 4)
            + txt(cx, y + h / 2 + 4.5, label, size, family=family, raw=raw, weight=weight))


def build():
    title = T("AES-GCM: CTR šifrēšana un GHASH autentifikācija",
              "AES-GCM: CTR encryption and GHASH authentication")
    W, H = 1000, 470
    s = K.header(W, H, title)
    s += txt(20, 26, title, 15, anchor="start", weight="bold")

    c1, c2, cl, cj = 330, 560, 760, 920
    yc, ye, yx, yo, yg = 62, 116, 196, 232, 350

    # skaitītāju bloki un E_K
    for cx, ctr, lab in [(c1, "00000002", "J" + sub("0") + " + 1"),
                         (c2, "00000003", "J" + sub("0") + " + 2"),
                         (cj, "00000001", "J" + sub("0"))]:
        s += txt(cx, yc - 8, lab, 12, weight="bold", raw=True)
        s += box(cx, yc, 140, 28, "N ‖ " + ctr, K.L_GREY, "#5a6a7a", 12, K.MONO)
        s += arrow(cx, yc + 28, cx, ye - 2)
        s += box(cx, ye, 64, 34, "E" + sub("K"), K.L_ORANGE, K.ORANGE, 14, raw=True, weight="bold")
    s += txt(cj + 8, ye + 60, T("tagam", "for the tag"), 10.5, K.GREY, "start")

    # XOR ar atklāto tekstu -> šifrteksts
    for cx, i in [(c1, "1"), (c2, "2")]:
        s += arrow(cx, ye + 34, cx, yx - 11)
        s += box(cx - 100, yx - 15, 52, 30, "P" + sub(i), K.L_BLUE, K.BLUE, 13, raw=True, weight="bold")
        s += arrow(cx - 74, yx, cx - 12, yx)
        s += xor(cx, yx, 10)
        s += arrow(cx, yx + 10, cx, yo - 2)
        s += box(cx, yo, 52, 30, "C" + sub(i), K.L_GREEN, K.GREEN, 13, raw=True, weight="bold")
        s += arrow(cx, yo + 30, cx, yg - 12)
    s += txt(c1 - 150, yx + 4, "CTR", 13, K.GREY, weight="bold")

    # garumu bloks
    s += box(cl, yo, 150, 30, "len(A) ‖ len(C)", K.L_GREY, "#5a6a7a", 12, K.MONO)
    s += txt(cl, yo - 10, T("garumi bitos, 2 × 64 biti", "lengths in bits, 2 × 64 bits"), 10.5, K.GREY)
    s += arrow(cl, yo + 30, cl, yg - 12)

    # GHASH ķēde
    s += rect(20, yg - 42, 870, 92, "none", "#9aa5b1", 1.2, 8, ' stroke-dasharray="5 4"')
    s += txt(30, yg + 40, "GHASH" + sub("H") + "(A, C)", 12, K.GREY, "start", raw=True)
    s += box(70, yg - 15, 90, 30, T("A (AAD)", "A (AAD)"), K.L_PURPLE, K.PURPLE, 12, weight="bold")
    chain = [("m", 200), ("x", c1), ("m", 445), ("x", c2), ("m", 660), ("x", cl), ("m", 840)]
    prev = 115
    for kind, x in chain:
        s += arrow(prev + 2, yg, x - 12, yg)
        if kind == "m":
            s += mul(x, yg, 10)
            s += txt(x, yg + 28, "· H", 12, weight="bold")
        else:
            s += xor(x, yg, 10)
        prev = x + 10
    s += txt(865, yg - 8, "S", 13, weight="bold")
    s += arrow(prev + 2, yg, cj - 12, yg)
    # E_K(J0) uz leju līdz taga XOR
    s += arrow(cj, ye + 34, cj, yg - 12)
    s += xor(cj, yg, 10)
    s += arrow(cj, yg + 10, cj, yg + 44)
    s += box(cj, yg + 46, 120, 32, T("tags T (128 b.)", "tag T (128 b.)"), K.L_RED, K.RED, 12, weight="bold")

    # formulas apakšā
    fy = 452
    s += txt(20, fy - 20, "H = E" + sub("K") + "(0" + sup("128") + "),   S = A·H" + sup("4") + " ⊕ C" + sub("1")
             + "·H" + sup("3") + " ⊕ C" + sub("2") + "·H" + sup("2") + " ⊕ L·H,   T = S ⊕ E" + sub("K")
             + "(J" + sub("0") + ")", 12.5, K.INK, "start", raw=True)
    s += txt(20, fy, T("Reizināšana · H notiek laukā GF(2", "Multiplication · H is done in GF(2")
             + sup("128") + T(") pēc moduļa x", ") modulo x") + sup("128") + " + x" + sup("7") + " + x"
             + sup("2") + " + x + 1;  L = len(A) ‖ len(C).", 12, K.GREY, "start", raw=True)
    return s + "</svg>\n"


if __name__ == "__main__":
    K.main(build, "gcm-mode.svg")
