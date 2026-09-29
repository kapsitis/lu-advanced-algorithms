# -*- coding: utf-8 -*-
"""Ģenerē sampling.svg -- sinusoīdas paraugu ņemšana bieži un reti (Naikvista teorēma).

Signāls x(t) = sin(2 pi * 7 t) (7 Hz), t no 0 līdz 1 s. Trīs paraugu ņemšanas ātrumi:
* 40 Hz > 2 * 7 Hz  -- paraugi viennozīmīgi nosaka sinusoīdu;
* 14 Hz = 2 * 7 Hz  -- visi paraugi krīt nullēs: signāls "pazūd";
* 8 Hz  < 2 * 7 Hz  -- tie paši paraugi der arī 1 Hz sinusoīdai (aliasing),
                       jo sin(2 pi 7 n / 8) = -sin(2 pi n / 8).

    python sampling.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgplot as G  # noqa: E402

F = 7.0


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
    s = G.head(W, H, "Paraugu ņemšana bieži un reti")
    s += panel(40, 40, "paraugi 40 reizes sekundē (40 Hz > 2 · 7 Hz): punkti viennozīmīgi nosaka 7 Hz sinusoīdu")
    s += panel(190, 14, "paraugi 14 reizes sekundē (14 Hz = 2 · 7 Hz): visi paraugi krīt nullēs, signāls pazūd")
    s += panel(340, 8, "paraugi 8 reizes sekundē (8 Hz < 2 · 7 Hz): tie paši punkti der arī 1 Hz sinusoīdai",
               alias=lambda t: -math.sin(2 * math.pi * t))
    s += G.txt(480, 460, "laiks, s", 12)
    s += G.txt(90, 486, "Pelēkā līnija — īstais 7 Hz signāls; zilie punkti — paraugi;", 11.5, "#333", "start")
    s += G.txt(90, 504, "oranžā raustītā līnija — zemākās frekvences sinusoīda (1 Hz), kas iet caur tiem "
               "pašiem paraugiem.", 11.5, "#333", "start")
    s += "</svg>\n"
    return s


if __name__ == "__main__":
    G.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sampling.svg"), build())
