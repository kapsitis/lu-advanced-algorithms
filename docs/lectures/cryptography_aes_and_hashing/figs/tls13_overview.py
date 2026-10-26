# -*- coding: utf-8 -*-
"""Ģenerē tls13-overview.svg -- TLS 1.3 rokasspiediens un tajā izmantotie algoritmi.

Kreisajā pusē -- pilnais (1-RTT) rokasspiediens pēc RFC 8446 2. nodaļas; {...} ir
ziņojumi, kas šifrēti ar rokasspiediena atslēgām, [...] -- ar lietotnes datu atslēgām.
Labajā pusē -- algoritmi; numuri pie ziņojumiem rāda, kuri algoritmi tos apstrādā.
Apakšā -- šifru komplekta TLS_AES_128_GCM_SHA256 nosaukuma daļas.

    python tls13_overview.py [--lang lv|en|both]
"""

import svgkit as K
from svgkit import T, txt, rect, arrow, line, badge, path_arrow

ALG = {1: K.PURPLE, 2: K.TEAL, 3: K.ORANGE, 4: K.BLUE, 5: K.RED}
LIGHT = {1: K.L_PURPLE, 2: K.L_TEAL, 3: K.L_ORANGE, 4: K.L_BLUE, 5: K.L_RED}


def alg_box(n, x, y, w, h, head, lines, note=None):
    s = rect(x, y, w, h, LIGHT[n], ALG[n], 1.6, 6)
    s += badge(x + 16, y + 18, n, ALG[n])
    s += txt(x + 32, y + 22, head, 12.5, anchor="start", weight="bold")
    for k, ln in enumerate(lines):
        s += txt(x + 12, y + 42 + 16 * k, ln, 11, K.INK, "start")
    if note:
        s += txt(x + w - 8, y + 22, note, 10, K.GREY, "end", italic=True)
    return s


def build():
    title = T("TLS 1.3 rokasspiediens un algoritmi", "TLS 1.3 handshake and its algorithms")
    W, H = 1040, 500
    s = K.header(W, H, title)
    s += txt(20, 26, title, 15, anchor="start", weight="bold")

    # --- ziņojumu secības diagramma --------------------------------------------
    xc, xs, y0, dy = 60, 400, 92, 37
    s += txt(xc, 58, T("klients", "client"), 13, weight="bold")
    s += txt(xs, 58, T("serveris", "server"), 13, weight="bold")
    msgs = [
        ("ClientHello + key_share", 1, [1]),
        ("ServerHello + key_share", -1, [1, 2]),
        ("{EncryptedExtensions}", -1, [3]),
        ("{Certificate}", -1, [3, 5]),
        ("{CertificateVerify}", -1, [3, 4, 5]),
        ("{Finished}", -1, [3, 4]),
        ("{Finished}", 1, [3, 4]),
        ("[Application Data]", 0, [3]),
    ]
    yend = y0 + dy * len(msgs) - 10
    s += line(xc, 66, xc, yend, "#9aa5b1", 1.4, "4 4")
    s += line(xs, 66, xs, yend, "#9aa5b1", 1.4, "4 4")
    for k, (name, d, algs) in enumerate(msgs):
        y = y0 + dy * k
        if d == 1:
            s += arrow(xc + 4, y, xs - 4, y)
        elif d == -1:
            s += arrow(xs - 4, y, xc + 4, y)
        else:
            s += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#444" stroke-width="1.6" '
                  'marker-start="url(#arw)" marker-end="url(#arw)"/>\n' % (xc + 4, y, xs - 4, y))
        s += txt((xc + xs) / 2, y - 6, name, 12, family=K.MONO)
        for j, n in enumerate(algs):
            s += badge(xs + 22 + 22 * j, y - 2, n, ALG[n])
    s += txt(20, yend + 26, T("{…} šifrēts ar rokasspiediena atslēgām, […] – ar lietotnes datu atslēgām",
                              "{…} encrypted with handshake keys, […] with application traffic keys"),
             11.5, K.GREY, "start")
    s += txt(20, yend + 44, T("1 RTT: klients var sūtīt datus jau pēc pirmās atbildes",
                              "1 RTT: the client can send data after the first reply"),
             11.5, K.GREY, "start")

    # --- algoritmi ------------------------------------------------------------------
    xa, xb, wa, wb = 520, 790, 250, 232
    s += alg_box(1, xa, 52, wa, 92, T("atslēgu vienošanās", "key agreement"),
                 ["ECDHE: X25519, P-256", T("hibrīds: X25519MLKEM768", "hybrid: X25519MLKEM768"),
                  T("→ kopīgais noslēpums", "→ shared secret")], T("12. lekcija", "lecture 12"))
    s += alg_box(2, xa, 178, wa, 92, T("atslēgu grafiks", "key schedule"),
                 ["HKDF-SHA256 (Extract, Expand)", T("→ rokasspiediena atslēgas", "→ handshake keys"),
                  T("→ lietotnes datu atslēgas", "→ application keys")])
    s += alg_box(3, xa, 304, wa, 92, T("ierakstu aizsardzība", "record protection"),
                 ["AEAD: AES-128-GCM", T("(vai ChaCha20-Poly1305)", "(or ChaCha20-Poly1305)"),
                  T("nonce = IV ⊕ kārtas numurs", "nonce = IV ⊕ sequence number")])
    s += alg_box(4, xb, 178, wb, 92, T("hešfunkcija", "hash function"),
                 [T("SHA-256: ziņojumu kopsavilkums", "SHA-256: transcript hash"),
                  T("HMAC-SHA256 → Finished", "HMAC-SHA256 → Finished"),
                  T("(arī HKDF iekšienē)", "(also inside HKDF)")])
    s += alg_box(5, xb, 304, wb, 92, T("autentifikācija", "authentication"),
                 [T("X.509 sertifikātu ķēde", "X.509 certificate chain"),
                  T("paraksts: ECDSA P-256, RSA-PSS", "signature: ECDSA P-256, RSA-PSS"),
                  T("(paraksta kopsavilkumu)", "(signs the transcript hash)")], T("12. lekcija", "lecture 12"))
    s += arrow(xa + wa / 2, 146, xa + wa / 2, 176, ALG[1])
    s += arrow(xa + wa / 2, 272, xa + wa / 2, 302, ALG[2])
    s += arrow(xb - 2, 224, xa + wa + 2, 224, ALG[4])
    s += arrow(xb + wb / 2, 272, xb + wb / 2, 302, ALG[4])

    # --- šifru komplekta nosaukums ---------------------------------------------------
    y = 452
    s += txt(xa, y - 26, T("šifru komplekts:", "cipher suite:"), 12, K.GREY, "start")
    parts = [("TLS_", None, T("protokols", "protocol")), ("AES_128_GCM", 3, "AEAD"),
             ("_", None, ""), ("SHA256", 2, T("HKDF un kopsavilkums", "HKDF and transcript"))]
    x = xa
    for p, n, note in parts:
        w = 10.2 * len(p)
        if n:
            s += rect(x - 2, y - 17, w + 4, 24, LIGHT[n], ALG[n], 1.2, 3)
            s += txt(x + w / 2, y + 24, note, 10.5, ALG[n], weight="bold")
        elif note:
            s += txt(x + w / 2, y + 24, note, 10.5, K.GREY)
        s += txt(x, y, p, 17, anchor="start", family=K.MONO)
        x += w
    return s + "</svg>\n"


if __name__ == "__main__":
    K.main(build, "tls13-overview.svg")
