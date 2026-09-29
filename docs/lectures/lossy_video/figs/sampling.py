# -*- coding: utf-8 -*-
"""Ģenerē sampling.svg -- sinusoīdas paraugu ņemšana bieži un reti (Naikvista teorēma).

Signāls x(t) = sin(2 pi * 7 t) (7 Hz), t no 0 līdz 1 s. Trīs paraugu ņemšanas ātrumi:
* 40 Hz > 2 * 7 Hz  -- paraugi viennozīmīgi nosaka sinusoīdu;
* 14 Hz = 2 * 7 Hz  -- visi paraugi krīt nullēs: signāls "pazūd";
* 8 Hz  < 2 * 7 Hz  -- tie paši paraugi der arī 1 Hz sinusoīdai (aliasing),
                       jo sin(2 pi 7 n / 8) = -sin(2 pi n / 8).


Uzraksti ir latviski (sampling.svg) un angliski (sampling.en.svg):

    python sampling.py              # abas valodas
    python sampling.py --lang en    # tikai angļu
"""

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgplot as G  # noqa: E402

F = 7.0


LANG = "lv"                           # uzrakstu valoda: "lv" vai "en" (sk. main)


def T(lv, en):
    """Uzraksts izvēlētajā valodā LANG."""
    return en if LANG == "en" else lv


def svg_name(name):
    """Faila nosaukums izvēlētajā valodā: x.svg (latviski) vai x.en.svg (angliski)."""
    return name[:-4] + ".en.svg" if LANG == "en" else name


def panel(y, fs, title, alias=None):
    p = G.Plot(90, y, 780, 90, (0, 1), (-1.25, 1.25))
    s = p.frame([(k / 10, "%g" % (k / 10)) for k in range(0, 11)], [(-1, "−1"), (0, "0"), (1, "1")])
    ts = [k / 2000 for k in range(2001)]
    s += p.line(ts, [math.sin(2 * math.pi * F * t) for t in ts], G.GRAY, 1.4)
    if alias is not None:
        s += p.line(ts, [alias(t) for t in ts], G.ORANGE, 2.2, "6 4")
    n = int(round(fs))
    for k in range(n + 1):
        t = k / fs
        v = math.sin(2 * math.pi * F * t)
        s += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2"/>\n'
              % (p.X(t), p.Y(0), p.X(t), p.Y(v), G.BLUE))
        s += p.dot(t, v, G.BLUE, 3.6)
    s += G.txt(90, y - 8, title, 12.5, G.INK, "start", "bold")
    return s


def build():
    W, H = 900, 520
    s = G.head(W, H, T("Paraugu ņemšana bieži un reti", "Sampling often and rarely"))
    s += panel(40, 40, T("paraugi 40 reizes sekundē (40 Hz > 2 · 7 Hz): punkti viennozīmīgi nosaka 7 Hz sinusoīdu", "40 samples per second (40 Hz > 2 · 7 Hz): the points determine the 7 Hz sine wave uniquely"))
    s += panel(190, 14, T("paraugi 14 reizes sekundē (14 Hz = 2 · 7 Hz): visi paraugi krīt nullēs, signāls pazūd", "14 samples per second (14 Hz = 2 · 7 Hz): all samples fall on zeros, the signal disappears"))
    s += panel(340, 8, T("paraugi 8 reizes sekundē (8 Hz < 2 · 7 Hz): tie paši punkti der arī 1 Hz sinusoīdai", "8 samples per second (8 Hz < 2 · 7 Hz): the same points also fit a 1 Hz sine wave"),
               alias=lambda t: -math.sin(2 * math.pi * t))
    s += G.txt(480, 460, T("laiks, s", "time, s"), 12)
    s += G.txt(90, 486, T("Pelēkā līnija — īstais 7 Hz signāls; zilie punkti — paraugi;", "Gray line — the true 7 Hz signal; blue dots — the samples;"), 11.5, "#333", "start")
    s += G.txt(90, 504, T("oranžā raustītā līnija — zemākās frekvences sinusoīda (1 Hz), kas iet caur tiem "
                          "pašiem paraugiem.",
                          "orange dashed line — a lower-frequency sine wave (1 Hz) that passes through the "
                          "same samples."), 11.5, "#333", "start")
    s += "</svg>\n"
    return s


def main():
    global LANG
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lang", choices=["lv", "en", "all"], default="all",
                    help="uzrakstu valoda (noklusēti abas)")
    langs = {"lv": ["lv"], "en": ["en"], "all": ["lv", "en"]}[ap.parse_args().lang]
    for LANG in langs:
        G.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), svg_name("sampling.svg")), build())


if __name__ == "__main__":
    main()
