# -*- coding: utf-8 -*-
"""Ģenerē audio-bands.svg -- frekvenču joslas: MP3 filtrubanka, auss kritiskās joslas, Opus.

* MP3 polifāzes filtrubanka: 32 vienāda platuma joslas (pie 44.1 kHz katra 689 Hz);
  katru joslu vēl sadala ar MDCT 18 līnijās (kopā 576).
* Kritiskās joslas (Bark skala, E. Zwicker): 24 joslas, zemās frekvencēs ~100 Hz platas.
* Opus CELT (48 kHz): 21 josla, robežas no RFC 6716 tabulas eband5ms (x 200 Hz).

    python audio_bands.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svgplot as G  # noqa: E402

MP3 = [k * 22050 / 32 for k in range(33)]
BARK = [0, 100, 200, 300, 400, 510, 630, 770, 920, 1080, 1270, 1480, 1720, 2000, 2320, 2700,
        3150, 3700, 4400, 5300, 6400, 7700, 9500, 12000, 15500]
OPUS = [200 * e for e in (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 28, 34, 40, 48, 60, 78, 100)]


def row(p, y, h, edges, fills, stroke):
    s = ""
    for k in range(len(edges) - 1):
        x0, x1 = p.X(edges[k]), p.X(edges[k + 1])
        s += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" '
              'stroke-width="0.8"/>\n' % (x0, y, x1 - x0, h, fills[k % 2], stroke))
    return s


def build():
    W, H = 960, 330
    s = G.head(W, H, "Frekvenču joslas")
    p = G.Plot(250, 40, 690, 220, (0, 22050), (0, 1))
    ticks = [(k * 2000, "%d" % (2 * k)) for k in range(0, 12)]
    for v, lab in ticks:
        X = p.X(v)
        s += ('<line x1="%.1f" y1="40" x2="%.1f" y2="260" stroke="#e3e7ec"/>\n' % (X, X))
        s += G.txt(X, 278, lab, 11, "#444")
    s += G.txt(p.x + p.w / 2, 300, "frekvence, kHz", 12)
    rows = [
        ("MP3 filtrubanka", "32 vienādas joslas", MP3, ("#dbe6f3", "#c3d5ea"), G.BLUE, 55),
        ("auss kritiskās joslas", "24 Bark joslas", BARK, ("#dcecd8", "#c4dfbd"), G.GREEN, 125),
        ("Opus (CELT)", "21 josla", OPUS, ("#fde5cc", "#fbd0a3"), G.ORANGE, 195),
    ]
    for name, sub_, edges, fills, stroke, y in rows:
        s += row(p, y, 46, edges, fills, stroke)
        s += G.txt(236, y + 20, name, 12.5, G.INK, "end", "bold")
        s += G.txt(236, y + 37, sub_, 11, "#555", "end")
    s += G.txt(20, 322, "MP3 joslas ir vienlīdz platas (689 Hz), bet auss zemās frekvences izšķir daudz "
               "smalkāk; Opus joslas tuvina auss kritiskās joslas.", 11.5, "#333", "start")
    s += "</svg>\n"
    return s


if __name__ == "__main__":
    G.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio-bands.svg"), build())
