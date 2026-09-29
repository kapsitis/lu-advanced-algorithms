# -*- coding: utf-8 -*-
"""Ģenerē ethernet-frame.svg -- Ethernet II kadrs un tā datu lauks (IPv4 + TCP).

Parādīti lauku garumi bitos un kontrolsummas trijos protokolu slāņos:

* Ethernet (kanāla slānis): FCS -- CRC-32 (32 biti) no mērķa adreses līdz
  datu lauka beigām; to aprēķina un pārbauda tīkla karte;
* IPv4 (tīkla slānis): galvenes kontrolsumma (16 biti) -- tikai IP galvenei;
* TCP (transporta slānis): kontrolsumma (16 biti) -- TCP galvenei un datiem.

Lauku platumi attēlā nav proporcionāli garumiem (datu lauks ir daudz garāks).


Uzraksti ir latviski (ethernet-frame.svg) un angliski (ethernet-frame.en.svg):

    python ethernet_frame.py              # abas valodas
    python ethernet_frame.py --lang en    # tikai angļu
"""

import argparse
import os

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
INK, BLUE, ORANGE, GREEN = "#222", "#4C78A8", "#F58518", "#54A24B"
GRAYF, GRAYS = "#eceff3", "#8a96a3"


LANG = "lv"                           # uzrakstu valoda: "lv" vai "en" (sk. main)


def T(lv, en):
    """Uzraksts izvēlētajā valodā LANG."""
    return en if LANG == "en" else lv


def svg_name(name):
    """Faila nosaukums izvēlētajā valodā: x.svg (latviski) vai x.en.svg (angliski)."""
    return name[:-4] + ".en.svg" if LANG == "en" else name


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal"):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s">%s</text>\n'
            % (x, y, FONT, size, fill, anchor, weight, s))


def rect(x, y, w, h, fill, stroke, sw=1.4, rx=0, extra=""):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
            'stroke="%s" stroke-width="%g"%s/>\n' % (x, y, w, h, rx, fill, stroke, sw, extra))


def line(x1, y1, x2, y2, stroke="#444", sw=1.4, extra=""):
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"%s/>\n'
            % (x1, y1, x2, y2, stroke, sw, extra))


def fields(x0, y, h, items):
    """Lauku rinda: (nosaukums, garums, platums, aizpildījums, apmale)."""
    s, x, pos = "", x0, []
    for name, bits, w, fill, stroke in items:
        s += rect(x, y, w, h, fill, stroke)
        lines = name.split("\n")
        for k, l in enumerate(lines):
            s += txt(x + w / 2, y + h / 2 - 6 * (len(lines) - 1) + 12 * k + 1, l, 12,
                     INK, weight="bold" if stroke in (ORANGE, GREEN) else "normal")
        s += txt(x + w / 2, y + h + 16, bits, 11, "#444")
        pos.append((x, w))
        x += w
    return s, pos


def build():
    title = T("Ethernet kadrs un kontrolsummas", "Ethernet frame and checksums")
    W, H = 960, 430
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
         'height="%d" role="img" aria-label="%s">\n'
         '<title>%s</title>\n'
         '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
         '<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" '
         'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         '<path d="M 0 0 L 10 5 L 0 10 z" fill="#444"/></marker></defs>\n'
         % (W, H, W, H, title, title, W, H))

    # --- Ethernet kadrs -------------------------------------------------------
    s += txt(20, 28, T("Ethernet II kadrs (kanāla slānis, OSI 2. slānis)", "Ethernet II frame (data link layer, OSI layer 2)"), 14, INK,
             "start", weight="bold")
    y1, h1 = 50, 56
    row, pos = fields(20, y1, h1, [
        (T("Preambula", "Preamble"), T("56 biti", "56 bits"), 110, GRAYF, GRAYS),
        ("SFD", T("8 biti", "8 bits"), 50, GRAYF, GRAYS),
        (T("Mērķa\nMAC adrese", "Destination\nMAC address"), T("48 biti", "48 bits"), 120, "#f4f6f8", "#5a6a7a"),
        (T("Sūtītāja\nMAC adrese", "Source\nMAC address"), T("48 biti", "48 bits"), 120, "#f4f6f8", "#5a6a7a"),
        ("EtherType", T("16 biti", "16 bits"), 90, "#f4f6f8", "#5a6a7a"),
        (T("Dati (payload)", "Data (payload)"), T("368 – 12 000 biti (46 – 1500 baiti)", "368 – 12 000 bits (46 – 1500 bytes)"), 300, "#dbe6f3", BLUE),
        ("FCS\nCRC-32", T("32 biti", "32 bits"), 100, "#fde5cc", ORANGE),
    ])
    s += row
    # iekava: CRC-32 aprēķina pār mērķa adresi ... datiem
    bx0 = pos[2][0]
    bx1 = pos[5][0] + pos[5][1]
    yb = y1 + h1 + 30
    s += ('<path d="M %g %g L %g %g L %g %g L %g %g" stroke="%s" stroke-width="1.6" '
          'fill="none"/>\n' % (bx0, yb, bx0, yb + 8, bx1, yb + 8, bx1, yb, ORANGE))
    fx = pos[6][0] + pos[6][1] / 2
    s += ('<path d="M %g %g L %g %g L %g %g" stroke="%s" stroke-width="1.6" fill="none" '
          'marker-end="url(#arw)"/>\n' % ((bx0 + bx1) / 2, yb + 8, (bx0 + bx1) / 2, yb + 26,
                                          fx, yb + 26, ORANGE))
    s += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.6" '
          'marker-end="url(#arw)"/>\n' % (fx, yb + 26, fx, y1 + h1 + 24, ORANGE))
    s += txt((bx0 + bx1) / 2, yb + 44,
             T("sūtītājs aprēķina CRC-32 no šiem laukiem un ieraksta to FCS laukā; "
               "saņēmējs pārrēķina un bojātu kadru izmet",
               "the sender computes CRC-32 over these fields and writes it into FCS; "
               "the receiver recomputes it and drops a corrupted frame"), 11.5, "#333")
    s += txt(20 + 80, yb + 12, T("sinhronizācija (nepārbauda)", "sync (not checked)"), 11, "#666")

    # --- datu lauka saturs: IPv4 + TCP ---------------------------------------
    y2, h2 = 290, 56
    s += txt(20, y2 - 38, T("Ethernet datu lauka saturs: IPv4 pakete ar TCP segmentu", "Contents of the Ethernet data field: an IPv4 packet with a TCP segment"), 14, INK,
             "start", weight="bold")
    row2, pos2 = fields(60, y2, h2, [
        ("", T("160 biti (bez opcijām)", "160 bits (no options)"), 260, "#f4f6f8", "#5a6a7a"),
        ("", T("160 biti (bez opcijām)", "160 bits (no options)"), 260, "#f4f6f8", "#5a6a7a"),
        (T("TCP dati", "TCP data"), T("pārējie biti", "remaining bits"), 300, "#dbe6f3", BLUE),
    ])
    s += row2
    # kontrolsummu lauki galvenēs
    for (x, w), label in zip(pos2[:2], [T("80.–95. bits", "bits 80–95"), T("128.–143. bits", "bits 128–143")]):
        cx = x + w - 92
        s += rect(cx, y2 + 6, 84, h2 - 12, "#dcecd8", GREEN, 1.6, 3)
        s += txt(cx + 42, y2 + h2 / 2 - 2, T("kontrolsumma", "checksum"), 10.5, INK, weight="bold")
        s += txt(cx + 42, y2 + h2 / 2 + 12, label, 10, "#333")
    s += txt(pos2[0][0] + 84, y2 + h2 / 2 + 5, T("IPv4 galvene", "IPv4 header"), 12)
    s += txt(pos2[1][0] + 84, y2 + h2 / 2 + 5, T("TCP galvene", "TCP header"), 12)
    s += txt(60, y2 + h2 + 40,
             T("IPv4 galvenes kontrolsumma sargā tikai IP galveni; TCP kontrolsumma — TCP galveni un datus "
               "(un IP adreses).",
               "The IPv4 header checksum protects only the IP header; the TCP checksum covers the TCP "
               "header and data (and the IP addresses)."), 11.5, "#333", "start")
    s += txt(60, y2 + h2 + 58,
             T("Abas ir 16 bitu vārdu summa ar pārnesi (vieninieku papildkods) — daudz vājākas par CRC-32.",
               "Both are sums of 16-bit words with end-around carry (ones' complement) — much weaker "
               "than CRC-32."), 11.5, "#333", "start")
    s += "</svg>\n"
    return s


def main():
    global LANG
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lang", choices=["lv", "en", "all"], default="all",
                    help="uzrakstu valoda (noklusēti abas)")
    langs = {"lv": ["lv"], "en": ["en"], "all": ["lv", "en"]}[ap.parse_args().lang]
    for LANG in langs:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), svg_name("ethernet-frame.svg"))
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(build())
        print("Wrote", out)


if __name__ == "__main__":
    main()
