# -*- coding: utf-8 -*-
"""Ģenerē sha256-diagram.svg -- SHA-256 aprēķina shēmu (FIPS 180-4).

1. Ziņojumu m (L biti) papildina: bits 1, nulles un L kā 64 bitu skaitlis,
   lai kopējais garums dalītos ar 512.
2. Rezultātu sadala 512 bitu blokos M_1, ..., M_N.
3. Sākot ar fiksētu vērtību H_0 (8 vārdi pa 32 bitiem), katrs bloks ar
   saspiešanas funkciju f pārrēķina stāvokli: H_i = f(H_{i-1}, M_i).
4. H_N (256 biti) ir SHA-256 vērtība.

Piemēra skaitļi ("abc") aprēķināti ar hashlib, papildinātais bloks -- ar
papildināšanas likumu, tāpēc tie vienmēr sakrīt ar īsto SHA-256.


Uzraksti ir latviski (sha256-diagram.svg) un angliski (sha256-diagram.en.svg):

    python sha256_diagram.py              # abas valodas
    python sha256_diagram.py --lang en    # tikai angļu
"""

import argparse
import hashlib
import os
import struct

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Consolas, Menlo, monospace"
INK, BLUE, ORANGE, GREEN, PURPLE = "#222", "#4C78A8", "#F58518", "#54A24B", "#B279A2"


LANG = "lv"                           # uzrakstu valoda: "lv" vai "en" (sk. main)


def T(lv, en):
    """Uzraksts izvēlētajā valodā LANG."""
    return en if LANG == "en" else lv


def svg_name(name):
    """Faila nosaukums izvēlētajā valodā: x.svg (latviski) vai x.en.svg (angliski)."""
    return name[:-4] + ".en.svg" if LANG == "en" else name


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal", family=FONT, raw=False):
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s">%s</text>\n'
            % (x, y, family, size, fill, anchor, weight, s if raw else esc(s)))


def sub(s):
    return '<tspan baseline-shift="sub" font-size="75%%">%s</tspan>' % s


def sup(s):
    return '<tspan baseline-shift="super" font-size="75%%">%s</tspan>' % s


def rect(x, y, w, h, fill, stroke, sw=1.4, rx=0, extra=""):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
            'stroke="%s" stroke-width="%g"%s/>\n' % (x, y, w, h, rx, fill, stroke, sw, extra))


def arrow(x1, y1, x2, y2, col="#444"):
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.8" '
            'marker-end="url(#arw)"/>\n' % (x1, y1, x2, y2, col))


def badge(x, y, n):
    return ('<circle cx="%g" cy="%g" r="11" fill="%s"/>\n' % (x, y, BLUE)
            + txt(x, y + 4.5, str(n), 13, "#fff", weight="bold"))


def padded(m):
    return m + b"\x80" + b"\x00" * ((55 - len(m)) % 64) + struct.pack(">Q", 8 * len(m))


def build():
    title = T("SHA-256 aprēķins", "SHA-256 computation")
    W, H = 960, 480
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
         'height="%d" role="img" aria-label="%s">\n<title>%s</title>\n'
         '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
         '<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
         'markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
         'fill="#444"/></marker></defs>\n' % (W, H, W, H, title, title, W, H))
    s += txt(20, 28, T("SHA-256: jebkāda garuma ievade → 256 bitu vērtība", "SHA-256: input of any length → 256-bit value"), 15, INK,
             "start", weight="bold")

    # --- 1. rinda: ievade, papildināšana, bloki -------------------------------
    y, h = 58, 50
    s += rect(20, y, 150, h, "#f4f6f8", "#5a6a7a", 1.4, 6)
    s += txt(95, y + 21, T("ziņojums m", "message m"), 12, weight="bold")
    s += txt(95, y + 38, T("L biti, L &lt; 2", "L bits, L &lt; 2") + sup("64"), 11, "#444", raw=True)
    s += arrow(174, y + h / 2, 226, y + h / 2)
    s += badge(200, y - 4, 1)
    x = 232
    for label, w, fill, stroke in [(T("m (L biti)", "m (L bits)"), 220, "#dbe6f3", BLUE), ("1", 26, "#fde5cc", ORANGE),
                                   ("0 … 0", 110, "#f4f6f8", "#9aa5b1"),
                                   (T("L (64 biti)", "L (64 bits)"), 110, "#fde5cc", ORANGE)]:
        s += rect(x, y, w, h, fill, stroke, 1.4)
        s += txt(x + w / 2, y + h / 2 + 4, label, 12)
        x += w
    s += txt(232 + 233, y + h + 18, T("papildināšana: kopējais garums dalās ar 512", "padding: the total length is a multiple of 512"), 11.5, "#444")
    s += arrow(x + 4, y + h / 2, x + 52, y + h / 2)
    s += badge(x + 28, y - 4, 2)
    bx = x + 58
    for k, lab in enumerate(["M" + sub("1"), "M" + sub("2"), "…", "M" + sub("N")]):
        s += rect(bx + k * 42, y + 5, 38, h - 10, "#dbe6f3" if lab != "…" else "#ffffff",
                  BLUE if lab != "…" else "#ffffff", 1.4, 3)
        s += txt(bx + k * 42 + 19, y + h / 2 + 5, lab, 12.5, weight="bold", raw=True)
    s += txt(bx + 82, y + h + 18, T("512 bitu bloki", "512-bit blocks"), 11.5, "#444")

    # --- 2. rinda: saspiešanas funkciju ķēde ----------------------------------
    y2, h2 = 222, 54
    s += badge(20 + 11, y2 - 66, 3)
    s += txt(48, y2 - 61, T("katrs bloks pārrēķina 256 bitu stāvokli: H", "each block updates the 256-bit state: H") + sub("i") +
             " = f(H" + sub("i−1") + ", M" + sub("i") + ")", 12, INK, "start", raw=True)
    s += rect(20, y2, 110, h2, "#ecdcea", PURPLE, 1.4, 6)
    s += txt(75, y2 + 22, "H" + sub("0") + " (IV)", 12.5, weight="bold", raw=True)
    s += txt(75, y2 + 40, T("8 × 32 biti", "8 × 32 bits"), 11, "#444")
    xs = [200, 400, 640]
    names = ["1", "2", "N"]
    prev = 130
    for k, (fx, nm) in enumerate(zip(xs, names)):
        if k == 2:
            s += txt(560, y2 + h2 / 2 + 5, "…", 18, "#444")
            prev = 580
        s += arrow(prev + 4, y2 + h2 / 2, fx - 4, y2 + h2 / 2)
        s += rect(fx, y2 + 4, 56, h2 - 8, "#fde5cc", ORANGE, 1.6, 6)
        s += txt(fx + 28, y2 + h2 / 2 + 6, "f", 16, weight="bold", family=MONO)
        s += arrow(fx + 28, y2 - 26, fx + 28, y2 + 2)
        s += txt(fx + 28, y2 - 30, "M" + sub(nm), 12, weight="bold", raw=True)
        if k < 2:
            s += arrow(fx + 60, y2 + h2 / 2, fx + 96, y2 + h2 / 2)
            s += txt(fx + 116, y2 + h2 / 2 + 5, "H" + sub(nm), 12.5, weight="bold", raw=True)
            prev = fx + 132
    s += arrow(700, y2 + h2 / 2, 736, y2 + h2 / 2)
    s += rect(740, y2, 200, h2, "#dcecd8", GREEN, 1.6, 6)
    s += txt(840, y2 + 22, "H" + sub("N") + " = SHA-256(m)", 12.5, weight="bold", raw=True)
    s += txt(840, y2 + 40, T("256 biti = 64 hex cipari", "256 bits = 64 hex digits"), 11, "#444")
    s += badge(720, y2 - 6, 4)

    # --- 3. rinda: f iekšpuse un piemērs --------------------------------------
    y3 = 318
    s += ('<path d="M 228 %g L 228 %g" stroke="%s" stroke-width="1.2" stroke-dasharray="5 4"/>\n'
          % (y2 + h2 - 4, y3, ORANGE))
    s += rect(20, y3, 450, 140, "#fff8f0", ORANGE, 1.2, 6)
    s += txt(34, y3 + 22, T("saspiešanas funkcija f(H, M)", "compression function f(H, M)"), 12.5, INK, "start", weight="bold")
    lines = [
        T("1. bloku M (16 vārdi pa 32 bitiem) paplašina līdz 64 vārdiem", "1. the block M (16 words of 32 bits) is expanded to 64 words"),
        "\t W" + sub("0") + ", …, W" + sub("63") + T(" ar bīdēm, rotācijām un XOR;", " with shifts, rotations and XOR;"),
        T("2. 64 raundi: 8 vārdu stāvokli a, …, h maina ar loģiskām", "2. 64 rounds update the 8-word state a, …, h with the logical"),
        T("\t funkcijām Ch, Maj, Σ", "\t functions Ch, Maj, Σ") + sub("0") + ", Σ" + sub("1") + T(", konstantēm K", ", constants K") + sub("t") +
        T(" un saskaitīšanu mod 2", " and addition mod 2") + sup("32") + ";",
        T("3. rezultātu pieskaita iepriekšējam H (katru vārdu mod 2", "3. the result is added to the previous H (each word mod 2") + sup("32") + ").",
    ]
    for k, l in enumerate(lines):
        ind = 16 if l.startswith("\t") else 0
        s += txt(34 + ind, y3 + 46 + 19 * k, l.lstrip("\t "), 11.5, "#333", "start", raw=True)

    m = b"abc"
    blk = padded(m).hex()
    dig = hashlib.sha256(m).hexdigest()
    dig2 = hashlib.sha256(b"abd").hexdigest()
    s += rect(490, y3, 450, 140, "#f4f6f8", "#5a6a7a", 1.2, 6)
    s += txt(504, y3 + 22, T("piemērs: m = “abc” (L = 24 biti, N = 1)", "example: m = “abc” (L = 24 bits, N = 1)"), 12.5, INK, "start",
             weight="bold")
    s += txt(504, y3 + 44, "M" + sub("1") + ":", 11.5, "#333", "start", raw=True)
    s += txt(534, y3 + 44, " ".join([blk[:8], blk[8:16], "…", blk[-16:-8], blk[-8:]]),
             11.5, "#333", "start", family=MONO)
    s += txt(504, y3 + 66, "SHA-256:", 11.5, "#333", "start")
    s += txt(504, y3 + 84, " ".join(dig[i:i + 8] for i in range(0, 32, 8)), 11.5, GREEN,
             "start", "bold", MONO)
    s += txt(504, y3 + 100, " ".join(dig[i:i + 8] for i in range(32, 64, 8)), 11.5, GREEN,
             "start", "bold", MONO)
    s += txt(504, y3 + 124, "“abd”: " + " ".join(dig2[i:i + 8] for i in range(0, 24, 8)) +
             T(" … (pilnīgi cita)", " … (completely different)"), 11.5, "#333", "start", family=MONO)
    s += "</svg>\n"
    return s


def main():
    global LANG
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lang", choices=["lv", "en", "all"], default="all",
                    help="uzrakstu valoda (noklusēti abas)")
    langs = {"lv": ["lv"], "en": ["en"], "all": ["lv", "en"]}[ap.parse_args().lang]
    for LANG in langs:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), svg_name("sha256-diagram.svg"))
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(build())
        print("Wrote", out)


if __name__ == "__main__":
    main()
