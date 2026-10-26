# -*- coding: utf-8 -*-
"""Ģenerē tls13-key-schedule.svg -- vienkāršots TLS 1.3 atslēgu grafiks (RFC 8446, 7.1).

Vidū -- trīs noslēpumi (Early, Handshake, Master Secret), ko savieno HKDF-Extract
un Derive-Secret(., "derived", ""). Pa labi -- no tiem atvasinātie satiksmes
noslēpumi; Derive-Secret konteksts ir rokasspiediena ziņojumu kopsavilkums
(CH = ClientHello, SH = ServerHello, Fin = Finished). Numuri rāda secību, kādā
tos aprēķina klients pilnā rokasspiedienā.

    python tls13_key_schedule.py [--lang lv|en|both]
"""

import svgkit as K
from svgkit import T, txt, rect, arrow, line, badge, path_arrow


def secret(cx, y, label, w=170, h=34):
    return (rect(cx - w / 2, y, w, h, K.L_PURPLE, K.PURPLE, 1.6, 6)
            + txt(cx, y + h / 2 + 5, label, 13, weight="bold"))


def extract(cx, y, w=130, h=28):
    return (rect(cx - w / 2, y, w, h, K.L_TEAL, K.TEAL, 1.4, 14)
            + txt(cx, y + h / 2 + 4.5, "HKDF-Extract", 12))


def traffic(x, y, label, name, w=250, h=38, fill=K.L_ORANGE, edge=K.ORANGE):
    return (rect(x, y, w, h, fill, edge, 1.4, 5)
            + txt(x + 10, y + 16, '"%s"' % label, 12, anchor="start", family=K.MONO, weight="bold")
            + txt(x + 10, y + 31, name, 10.5, K.GREY, "start"))


def build():
    title = T("TLS 1.3 atslēgu grafiks (vienkāršots, RFC 8446, 7.1. nodaļa)",
              "TLS 1.3 key schedule (simplified, RFC 8446, Section 7.1)")
    W, H = 1000, 640
    s = K.header(W, H, title)
    s += txt(20, 26, title, 15, anchor="start", weight="bold")

    cx, xr = 290, 520
    rows = [(70, T("PSK vai 0", "PSK or 0"), "Early Secret"),
            (250, "(EC)DHE", "Handshake Secret"),
            (430, "0", "Master Secret")]
    for k, (y, ikm, name) in enumerate(rows):
        s += extract(cx, y)
        s += rect(40, y, 100, 28, K.L_GREY, "#5a6a7a", 1.2, 4)
        s += txt(90, y + 18.5, ikm, 12, weight="bold")
        s += arrow(142, y + 14, cx - 67, y + 14)
        s += txt(cx - 120, y - 6, "IKM", 10.5, K.GREY)
        s += arrow(cx, y + 28, cx, y + 50)
        s += secret(cx, y + 52, name)
        if k < 2:
            s += arrow(cx, y + 86, cx, y + 178)
            s += txt(cx + 8, y + 132, 'Derive-Secret(·, "derived", "")', 11, K.INK, "start", family=K.MONO)
            s += txt(cx + 8, y + 148, T("→ salt nākamajam Extract", "→ salt of the next Extract"), 10.5,
                     K.GREY, "start")
    s += txt(cx + 8, 64, "salt = 0", 10.5, K.GREY, "start")
    s += line(cx, 46, cx, 68, "#444", 1.6)

    # labā puse: satiksmes noslēpumi
    ye = 70 + 52 + 17
    s += path_arrow("M %g %g L %g %g" % (cx + 86, ye, xr - 2, ye), "#888", dash="4 3")
    s += traffic(xr, ye - 19, "c e traffic", T("0-RTT dati (tikai ar PSK)", "0-RTT data (only with PSK)"),
                 fill=K.L_GREY, edge="#9aa5b1")

    yh = 250 + 52 + 17
    s += txt(cx + 96, yh - 8, "CH…SH", 11, K.BLUE, "start", weight="bold")
    for k, (lab, nm) in enumerate([("c hs traffic", "client_handshake_traffic_secret"),
                                   ("s hs traffic", "server_handshake_traffic_secret")]):
        yb = yh - 40 + 50 * k
        s += path_arrow("M %g %g L %g %g L %g %g" % (cx + 86, yh, xr - 24, yh, xr - 2, yb + 19))
        s += traffic(xr, yb, lab, nm)
    s += badge(xr + 266, yh - 21, 2)
    s += badge(xr + 266, yh + 29, 2)
    s += badge(cx - 100, yh, 1)

    ym = 430 + 52 + 17
    s += txt(cx + 96, ym - 8, T("CH…servera Fin", "CH…server Fin"), 11, K.BLUE, "start", weight="bold")
    for k, (lab, nm) in enumerate([("c ap traffic", "client_application_traffic_secret_0"),
                                   ("s ap traffic", "server_application_traffic_secret_0")]):
        yb = ym - 64 + 50 * k
        s += path_arrow("M %g %g L %g %g L %g %g" % (cx + 86, ym, xr - 24, ym, xr - 2, yb + 19))
        s += traffic(xr, yb, lab, nm)
        s += badge(xr + 266, yb + 19, 3)
    yb = ym + 36
    s += path_arrow("M %g %g L %g %g L %g %g" % (cx + 86, ym, xr - 24, ym, xr - 2, yb + 19), "#888", dash="4 3")
    s += traffic(xr, yb, "res master", T("CH…klienta Fin; atjaunošanai (PSK)", "CH…client Fin; for resumption (PSK)"),
                 fill=K.L_GREY, edge="#9aa5b1")
    s += badge(xr + 266, yb + 19, 5)
    s += badge(cx - 100, ym, 3)

    # pa labi: no satiksmes noslēpuma -> key, iv, finished_key
    bx, by, bw = 800, 196, 186
    s += rect(bx, by, bw, 150, "#ffffff", K.ORANGE, 1.4, 6, ' stroke-dasharray="5 4"')
    s += txt(bx + bw / 2, by + 20, T("no katra satiksmes", "from every traffic"), 11.5, weight="bold")
    s += txt(bx + bw / 2, by + 36, T("noslēpuma S:", "secret S:"), 11.5, weight="bold")
    for k, ln in enumerate(['key = Expand-Label(', '  S, "key", "", 16)', 'iv = Expand-Label(',
                            '  S, "iv", "", 12)']):
        s += txt(bx + 10, by + 60 + 17 * k, ln, 11, family=K.MONO, anchor="start")
    s += txt(bx + 10, by + 136, T("+ finished_key (Finished)", "+ finished_key (Finished)"), 10.5, K.GREY, "start")
    s += line(xr + 277, yh - 21, bx - 2, by + 75, K.ORANGE, 1.2, "4 3")
    s += line(xr + 277, yh + 29, bx - 2, by + 75, K.ORANGE, 1.2, "4 3")

    # secības leģenda
    ly = 616
    s += txt(20, ly - 14, T("Klienta secība: (1) pēc ServerHello aprēķina (EC)DHE un Handshake Secret; "
                            "(2) rokasspiediena atslēgas – atšifrē servera ziņojumus;",
                            "Client's order: (1) after ServerHello compute (EC)DHE and Handshake Secret; "
                            "(2) handshake keys – decrypt the server's messages;"),
             11.5, K.GREY, "start")
    s += txt(20, ly + 4, T("(3) pēc servera Finished – Master Secret un lietotnes atslēgas; (4) sūta savu "
                           "Finished; (5) resumption_master_secret nākamajai sesijai.",
                           "(3) after the server's Finished – Master Secret and application keys; (4) send its own "
                           "Finished; (5) resumption_master_secret for the next session."),
             11.5, K.GREY, "start")
    return s + "</svg>\n"


if __name__ == "__main__":
    K.main(build, "tls13-key-schedule.svg")
