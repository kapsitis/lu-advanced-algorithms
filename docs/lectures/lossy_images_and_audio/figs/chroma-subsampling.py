# -*- coding: utf-8 -*-
"""Ģenerē chroma-subsampling.svg -- krāsainības izretināšanas shēmas J:a:b.

Katrai shēmai parādīts atsauces apgabals: J = 4 pikseļi platumā, 2 rindas.
Pelēkais režģis ir gaišuma (Y) paraugi -- tie ir visiem pikseļiem.  Krāsainie
taisnstūri rāda, kurus pikseļus aptver viens krāsainības paraugs (tas pats
izvietojums ir gan Cb, gan Cr plaknē).

Uzraksti ir latviski (chroma-subsampling.svg) un angliski
(chroma-subsampling.en.svg):

    python chroma-subsampling.py              # abas valodas
    python chroma-subsampling.py --lang en    # tikai angļu
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "jpeg_pipeline", os.path.join(HERE, "jpeg-pipeline.py"))
J = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(J)

# (nosaukums, krāsainības parauga platums un augstums pikseļos, paskaidrojums
# {valoda: teksts}, vērtību skaits uz pikseli)
SCHEMES = [
    ("4:4:4", 1, 1, {"lv": "bez izretināšanas", "en": "no subsampling"}, "3"),
    ("4:2:2", 2, 1, {"lv": "½ horizontāli", "en": "½ horizontally"}, "2"),
    ("4:2:0", 2, 2, {"lv": "½ horizontāli un vertikāli",
                     "en": "½ horizontally and vertically"}, "1.5"),
    ("4:1:1", 4, 1, {"lv": "¼ horizontāli", "en": "¼ horizontally"}, "1.5"),
    ("4:4:0", 1, 2, {"lv": "½ vertikāli", "en": "½ vertically"}, "2"),
]
PER_PIXEL = {"lv": "%s vērtības/pikselī", "en": "%s values/pixel"}
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


def build(lang="lv"):
    en = lang == "en"
    W, H = 960, 170
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'width="%d" height="%d" role="img" aria-label="%s">\n'
         '<title>%s</title>\n'
         % (W, H, W, H,
            "Chroma subsampling" if en else "Krāsainības izretināšana",
            "Chroma subsampling schemes J:a:b" if en
            else "Krāsainības izretināšanas shēmas J:a:b"))
    s += J.rect(0, 0, W, H, "#ffffff", "none", 0)
    for i, (name, cw, ch, n1, n2) in enumerate(SCHEMES):
        s += panel(28 + i * 190, 38, name, cw, ch, n1[lang],
                   PER_PIXEL[lang] % n2)
    s += "</svg>\n"
    return s


def main():
    J.write_svgs("chroma-subsampling", build, __doc__.splitlines()[0])


if __name__ == "__main__":
    main()
