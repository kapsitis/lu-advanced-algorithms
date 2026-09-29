# -*- coding: utf-8 -*-
"""Ģenerē vp9-gop.svg -- VP9 dekodēšanas un rādīšanas secība ar slēptu ALTREF.

Struktūra ņemta no vp9-examples/bouncing_ball_ARF.ivf (inspect_ivf.py izvade):
dekodēšanas secībā 0 ir atslēgas freims, 1 ir slēptais ALTREF (show_frame = 0),
kas vienā IVF ierakstā (superfreimā) iepakots kopā ar 2 (rāda kā 1. kadru);
nākamais slēptais ALTREF ir 14, superfreimā kopā ar 15 (rāda kā 13. kadru).
Parādīti pirmie 16 kodētie freimi.

    python vp9_gop.py
"""

import os

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
INK, BLUE, ORANGE, GREEN, PURPLE = "#222", "#4C78A8", "#F58518", "#54A24B", "#B279A2"

# (dekodēšanas numurs, loma, rādīšanas numurs vai None, IVF ieraksts)
FRAMES = [(0, "K", 0, 0), (1, "A", None, 1), (2, "I", 1, 1)] + \
         [(d, "I", d - 1, d - 1) for d in range(3, 14)] + \
         [(14, "A", None, 13), (15, "I", 13, 13)]


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal"):
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s">%s</text>\n' % (x, y, FONT, size, fill, anchor, weight, s))


def build():
    W, H = 960, 300
    step, bw = 48, 40
    x0 = 130
    yd, yv = 70, 200
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img" aria-label="VP9 dekodēšanas un rādīšanas secība">\n'
         '<title>VP9 dekodēšanas un rādīšanas secība</title>\n'
         '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
         '<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
         'markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
         'fill="#777"/></marker></defs>\n' % (W, H, W, H, W, H))
    s += txt(20, 44, "dekodēšanas", 12, INK, "start", "bold")
    s += txt(20, 60, "secība", 12, INK, "start", "bold")
    s += txt(20, yv + 18, "rādīšanas", 12, INK, "start", "bold")
    s += txt(20, yv + 34, "secība", 12, INK, "start", "bold")
    style = {"K": ("#dcecd8", GREEN, "K"), "A": ("#fde5cc", ORANGE, "ARF"), "I": ("#dbe6f3", BLUE, "")}
    # superfreimi: vienā IVF ierakstā ir divi kodēti freimi
    for d in (1, 14):
        x = x0 + d * step - 5
        s += ('<rect x="%g" y="%g" width="%g" height="%g" rx="8" fill="none" stroke="%s" '
              'stroke-width="1.4" stroke-dasharray="5 3"/>\n' % (x, yd - 22, step + bw + 10, bw + 44, PURPLE))
        s += txt(x + (step + bw + 10) / 2, yd - 28, "superfreims", 10.5, PURPLE)
    disp_x = {}
    for d, role, disp, ivf in FRAMES:
        x = x0 + d * step
        fill, stroke, lab = style[role]
        dash = ' stroke-dasharray="4 3"' if role == "A" else ""
        s += ('<rect x="%g" y="%g" width="%g" height="%g" rx="5" fill="%s" stroke="%s" '
              'stroke-width="1.6"%s/>\n' % (x, yd, bw, bw, fill, stroke, dash))
        s += txt(x + bw / 2, yd + 20, str(d), 13, INK, weight="bold")
        s += txt(x + bw / 2, yd + 36, lab if lab else "inter", 10, "#444")
        if disp is not None:
            disp_x[disp] = x
    for disp, xd in sorted(disp_x.items()):
        xv = x0 + disp * step + step / 2 + bw / 2
        s += ('<rect x="%g" y="%g" width="%g" height="%g" rx="5" fill="#f4f6f8" stroke="#5a6a7a" '
              'stroke-width="1.4"/>\n' % (xv - bw / 2, yv, bw, 36))
        s += txt(xv, yv + 23, str(disp), 13, INK, weight="bold")
        s += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#777" stroke-width="1.2" '
              'marker-end="url(#arw)"/>\n' % (xd + bw / 2, yd + bw + 2, xv, yv - 3))
    s += txt(x0 + 1 * step + bw / 2, yd + bw + 36, "netiek rādīts", 10.5, ORANGE)
    s += txt(x0 + 14 * step + bw / 2, yd + bw + 36, "netiek rādīts", 10.5, ORANGE)
    s += txt(20, H - 16, "Slēptos ALTREF freimus (show_frame = 0) dekodē un saglabā kā atsauces; "
             "tos neparāda, bet no tiem prognozē nākamos kadrus.", 11.5, "#333", "start")
    s += "</svg>\n"
    return s


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vp9-gop.svg")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build())
    print("Wrote", out)


if __name__ == "__main__":
    main()
