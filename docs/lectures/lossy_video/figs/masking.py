# -*- coding: utf-8 -*-
"""Ģenerē frequency-masking.svg un temporal-masking.svg (vienkāršoti psihoakustiskie modeļi).

Frekvenču maskēšana:
* dzirdamības slieksnis klusumā (E. Terhardt, 1979):
  T(f) = 3.64 (f/1000)^-0.8 - 6.5 exp(-0.6 (f/1000 - 3.3)^2) + 0.001 (f/1000)^4  [dB SPL];
* Bark skala: z(f) = 13 atan(0.00076 f) + 3.5 atan((f/7500)^2);
* maskējošais tonis 1 kHz, 70 dB; tā maskēšanas slieksnis ir par 10 dB zemāks un
  samazinās par 27 dB uz Bark zemo frekvenču virzienā un par
  24 + 0.23/(f/1000) - 0.2 L dB uz Bark augsto frekvenču virzienā (tātad ~10 dB/Bark);
* kopējais slieksnis = max(klusuma slieksnis, maskēšanas slieksnis).

Temporālā maskēšana ir shematiska: priekšmaskēšana ~20 ms, pēcmaskēšana ~150 ms.


Uzraksti ir latviski (frequency-masking.svg, temporal-masking.svg) un angliski (frequency-masking.en.svg, temporal-masking.en.svg):

    python masking.py              # abas valodas
    python masking.py --lang en    # tikai angļu
"""

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgplot as G  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FM, LM = 1000.0, 70.0          # maskējošais tonis
OFFSET = 10.0                  # maskēšanas slieksnis zem maskējošā toņa līmeņa
PROBES = [(1200.0, 45.0), (4000.0, 25.0)]   # (frekvence, līmenis) pārbaudes toņiem


LANG = "lv"                           # uzrakstu valoda: "lv" vai "en" (sk. main)


def T(lv, en):
    """Uzraksts izvēlētajā valodā LANG."""
    return en if LANG == "en" else lv


def svg_name(name):
    """Faila nosaukums izvēlētajā valodā: x.svg (latviski) vai x.en.svg (angliski)."""
    return name[:-4] + ".en.svg" if LANG == "en" else name


def quiet(f):
    k = f / 1000.0
    return 3.64 * k ** -0.8 - 6.5 * math.exp(-0.6 * (k - 3.3) ** 2) + 1e-3 * k ** 4


def bark(f):
    return 13 * math.atan(0.00076 * f) + 3.5 * math.atan((f / 7500.0) ** 2)


def mask(f):
    dz = bark(f) - bark(FM)
    slope = 27.0 if dz < 0 else 24 + 0.23 / (FM / 1000.0) - 0.2 * LM
    return LM - OFFSET - slope * abs(dz)


def threshold(f):
    return max(quiet(f), mask(f))


def freq_svg():
    W, H = 900, 400
    s = G.head(W, H, T("Frekvenču maskēšana", "Frequency masking"))
    p = G.Plot(90, 30, 780, 290, (20, 20000), (-10, 100), xlog=True)
    xt = [(v, lab) for v, lab in [(20, "20"), (50, "50"), (100, "100"), (200, "200"), (500, "500"),
                                  (1000, "1k"), (2000, "2k"), (5000, "5k"), (10000, "10k"), (20000, "20k")]]
    s += p.frame(xt, [(v, str(v)) for v in range(0, 101, 20)], T("frekvence, Hz", "frequency, Hz"), T("skaņas līmenis, dB", "sound level, dB"))
    fs = [20 * (1000.0 ** (k / 600)) for k in range(601)]
    s += p.area(fs, [threshold(f) for f in fs], G.ORANGE, 0.12)
    s += p.line(fs, [quiet(f) for f in fs], G.GRAY, 2, "6 4")
    s += p.line(fs, [threshold(f) for f in fs], G.ORANGE, 2.4)
    s += p.vline(FM, -10, LM, G.RED, 4)
    s += G.txt(p.X(FM) - 8, p.Y(LM) - 6, T("maskējošais tonis 1 kHz, %d dB", "masking tone 1 kHz, %d dB") % LM, 11.5, G.RED, "end")
    legend = []
    for name, (f, lv) in zip("AB", PROBES):
        audible = lv > threshold(f)
        col = G.GREEN if audible else G.GRAY
        s += p.vline(f, -10, lv, col, 4, None if audible else "4 3")
        s += G.txt(p.X(f), p.Y(lv) - 6, name, 12.5, col, weight="bold")
        legend.append((col, "%s: %g Hz, %g dB — %s"
                       % (name, f, lv, T("dzirdams", "audible") if audible else T("nomaskēts", "masked"))))
    lx, ly = p.X(1250), p.Y(96)
    s += ('<rect x="%.1f" y="%.1f" width="262" height="84" rx="4" fill="#ffffff" fill-opacity="0.9" '
          'stroke="#c9d3de"/>\n' % (lx - 10, ly - 14))
    rows = [(G.ORANGE, None, T("maskēšanas slieksnis", "masking threshold")), (G.GRAY, "6 4", T("dzirdamības slieksnis klusumā", "threshold in quiet"))]
    for k, (col, dash, lab) in enumerate(rows):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        s += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"%s/>\n'
              % (lx, ly + 18 * k - 4, lx + 26, ly + 18 * k - 4, col, d))
        s += G.txt(lx + 34, ly + 18 * k, lab, 11.5, "#333", "start")
    for k, (col, lab) in enumerate(legend):
        s += G.txt(lx, ly + 36 + 18 * k, lab, 11.5, col, "start", "bold")
    s += G.txt(90, 385, T("Skaņa zem oranžās līknes nav dzirdama. Iekodētājs tur var atļauties lielu "
                          "kvantizācijas troksni (vai signālu nekodēt nemaz).",
                          "Sound below the orange curve is inaudible. There the encoder can afford a lot of "
                          "quantization noise (or not encode the signal at all)."), 11.5, "#333", "start")
    s += "</svg>\n"
    return s


def temporal_level(t):
    if t < 0:
        return 45 * math.exp(t / 5.0)             # priekšmaskēšana
    if t <= 200:
        return 45.0                               # vienlaicīgā maskēšana
    return 45 * math.exp(-(t - 200) / 35.0)      # pēcmaskēšana


def temporal_svg():
    W, H = 900, 380
    s = G.head(W, H, T("Temporālā maskēšana", "Temporal masking"))
    p = G.Plot(90, 40, 780, 250, (-60, 400), (0, 80))
    s += p.frame([(v, str(v)) for v in range(-50, 401, 50)], [(v, str(v)) for v in range(0, 81, 20)],
                 T("laiks, ms (0 — skaļās skaņas sākums)", "time, ms (0 — onset of the loud sound)"), T("līmenis, dB", "level, dB"))
    # MP3 garā loga garums pirms skaņas sākuma
    s += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="0.12" '
          'stroke="%s" stroke-dasharray="4 3"/>\n'
          % (p.X(-26), p.Y(30), p.X(0) - p.X(-26), p.Y(0) - p.Y(30), G.PURPLE, G.PURPLE))
    s += G.txt(p.X(-26) - 4, p.Y(24), T("MDCT logs", "MDCT window"), 11, G.PURPLE, "end")
    s += G.txt(p.X(-26) - 4, p.Y(24) + 14, "≈ 26 ms", 11, G.PURPLE, "end")
    # maskējošā skaņa
    s += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="0.25" '
          'stroke="%s"/>\n' % (p.X(0), p.Y(70), p.X(200) - p.X(0), p.Y(0) - p.Y(70), G.RED, G.RED))
    s += G.txt(p.X(100), p.Y(70) - 8, T("skaļa skaņa, 70 dB", "loud sound, 70 dB"), 12, G.RED, weight="bold")
    ts = [-60 + k * 0.5 for k in range(921)]
    s += p.area(ts, [temporal_level(t) for t in ts], G.ORANGE, 0.15)
    s += p.line(ts, [temporal_level(t) for t in ts], G.ORANGE, 2.4)
    s += G.txt(p.X(-12), p.Y(58), T("priekšmaskēšana", "pre-masking"), 11.5, G.ORANGE, "middle", "bold")
    s += G.txt(p.X(-12), p.Y(58) + 14, "≈ 20 ms", 11.5, G.ORANGE)
    s += G.txt(p.X(290), p.Y(40), T("pēcmaskēšana ≈ 150 ms", "post-masking ≈ 150 ms"), 11.5, G.ORANGE, "start", "bold")
    s += G.txt(90, 345, T("Skaņas zem oranžās līknes nav dzirdamas (shematiski). Ja kvantizācijas troksnis "
                          "izplūst pa visu MDCT logu pirms skaļās skaņas",
                          "Sounds below the orange curve are inaudible (schematic). If quantization noise "
                          "spreads over the whole MDCT window"), 11.5, "#333", "start")
    s += G.txt(90, 363, T("sākuma un logs ir garāks par priekšmaskēšanu, troksni dzird kā “pirmsatbalsi” "
                          "(pre-echo); tāpēc pārejās kodeki pārslēdzas uz īsiem logiem.",
                          "before the onset and the window is longer than pre-masking, the noise is heard as "
                          "“pre-echo”; so codecs use short windows at transients."),
               11.5, "#333", "start")
    s += "</svg>\n"
    return s


def main():
    global LANG
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lang", choices=["lv", "en", "all"], default="all",
                    help="uzrakstu valoda (noklusēti abas)")
    langs = {"lv": ["lv"], "en": ["en"], "all": ["lv", "en"]}[ap.parse_args().lang]
    for f, lv in PROBES:
        print("pārbaudes tonis %g Hz %g dB: slieksnis %.1f dB -> %s"
              % (f, lv, threshold(f), "dzirdams" if lv > threshold(f) else "nomaskēts"))
    for LANG in langs:
        G.save(os.path.join(HERE, svg_name("frequency-masking.svg")), freq_svg())
        G.save(os.path.join(HERE, svg_name("temporal-masking.svg")), temporal_svg())


if __name__ == "__main__":
    main()
