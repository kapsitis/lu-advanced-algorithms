# -*- coding: utf-8 -*-
"""Ģenerē chroma-subsampling.svg -- krāsainības izretināšanas shēmas J:a:b.

Katrai shēmai parādīts atsauces apgabals: J = 4 pikseļi platumā, 2 rindas.
Pelēkais režģis ir gaišuma (Y) paraugi -- tie ir visiem pikseļiem.  Krāsainie
taisnstūri rāda, kurus pikseļus aptver viens krāsainības paraugs (tas pats
izvietojums ir gan Cb, gan Cr plaknē).

    python chroma-subsampling.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "jpeg_pipeline", os.path.join(HERE, "jpeg-pipeline.py"))
J = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(J)

# (nosaukums, krāsainības parauga platums un augstums pikseļos, paskaidrojums)
SCHEMES = [
    ("4:4:4", 1, 1, "bez izretināšanas", "3 vērtības/pikselī"),
    ("4:2:2", 2, 1, "½ horizontāli", "2 vērtības/pikselī"),
    ("4:2:0", 2, 2, "½ horizontāli un vertikāli", "1.5 vērtības/pikselī"),
    ("4:1:1", 4, 1, "¼ horizontāli", "1.5 vērtības/pikselī"),
    ("4:4:0", 1, 2, "½ vertikāli", "2 vērtības/pikselī"),
]
FILL, STROKE = "#dcecd8", J.GREEN      # viens krāsainības paraugs


def panel(x, y, name, cw, ch, note1, note2):
    cell = 34
    s = J.txt(x + 2 * cell, y - 12, name, 15, J.INK, weight="bold")
    # krāsainības paraugi
    for r in range(0, 2, ch):
        for c in range(0, 4, cw):
            s += J.rect(x + c * cell + 2, y + r * cell + 2, cw * cell - 4,
                        ch * cell - 4, FILL, STROKE, 1.6, 7)
            s += ('<circle cx="%g" cy="%g" r="4" fill="%s"/>\n'
                  % (x + (c + cw / 2) * cell, y + (r + ch / 2) * cell, STROKE))
    # gaišuma paraugi: režģis
    for i in range(5):
        s += J.line(x + i * cell, y, x + i * cell, y + 2 * cell, "#5a6a7a", 0.8,
                    ' stroke-opacity="0.6"')
    for i in range(3):
        s += J.line(x, y + i * cell, x + 4 * cell, y + i * cell, "#5a6a7a", 0.8,
                    ' stroke-opacity="0.6"')
    a = 4 // cw
    b = 0 if ch == 2 else a
    s += J.txt(x + 2 * cell, y + 2 * cell + 20,
               "a = %d, b = %d" % (a, b), 12, "#333")
    s += J.txt(x + 2 * cell, y + 2 * cell + 38, note1, 11, "#555")
    s += J.txt(x + 2 * cell, y + 2 * cell + 54, note2, 11, "#555")
    return s


def build():
    W, H = 960, 170
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'width="%d" height="%d" role="img" aria-label="Krāsainības izretināšana">\n'
         '<title>Krāsainības izretināšanas shēmas J:a:b</title>\n' % (W, H, W, H))
    s += J.rect(0, 0, W, H, "#ffffff", "none", 0)
    for i, (name, cw, ch, n1, n2) in enumerate(SCHEMES):
        s += panel(28 + i * 190, 38, name, cw, ch, n1, n2)
    s += "</svg>\n"
    return s


def main():
    out = os.path.join(HERE, "chroma-subsampling.svg")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build())
    print("Wrote", out)


if __name__ == "__main__":
    main()
