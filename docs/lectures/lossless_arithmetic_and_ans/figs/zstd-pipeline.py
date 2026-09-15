# -*- coding: utf-8 -*-
"""Ģenerē zstd-pipeline.svg -- Zstandard bloka apstrādes shēmu.

Šis ir statisks shēmas attēls; vienīgā komandrindas iespēja ir izvades fails.

    python zstd-pipeline.py
"""

import ansfig as A


def build():
    W, H = 940, 336
    s = A.head(W, H, "Zstandard bloka uzbūve")
    s += A.txt(20, 28, "Zstandard: LZ77 + entropijas kodēšana "
                       "(FSE = tANS un Hafmans)", 14.5, "#222", "start",
               weight="bold")

    BW, BH = 168, 56
    y1 = 132
    s += A.rect(20, y1, BW, BH, "#f4f6f8", "#5a6a7a", rx=6)
    s += A.txt(20 + BW / 2, y1 + 24, "ievades bloks", 12.5, "#222")
    s += A.txt(20 + BW / 2, y1 + 41, "(līdz 128 KB)", 12.5, "#222")
    s += A.arrow(196, y1 + BH / 2, 224, y1 + BH / 2)
    s += A.rect(228, y1, BW, BH, "#dbe6f3", "#4C78A8", rx=6)
    s += A.txt(228 + BW / 2, y1 + 24, "LZ77 meklētājs", 12.5, "#222")
    s += A.txt(228 + BW / 2, y1 + 41, "(atkārtojumi logā)", 12.5, "#222")
    s += A.arrow(400, y1 + BH / 2, 424, y1 + BH / 2)

    sx = 440
    streams = [("literāļi", "(nesakritušie baiti)", "#fde5cc", "#F58518",
                "Hafmana koks"),
               ("garumi", "(match / literal length)", "#dcecd8", "#54A24B",
                "FSE  (tANS)"),
               ("nobīdes", "(match offsets)", "#ecdcea", "#B279A2",
                "FSE  (tANS)")]
    for y, (l1, l2, fill, stroke, coder) in zip([56, 132, 208], streams):
        s += A.rect(sx, y, 186, 56, fill, stroke, rx=6)
        s += A.txt(sx + 93, y + 24, l1, 12.5, "#222", weight="bold")
        s += A.txt(sx + 93, y + 41, l2, 11.5, "#333")
        s += A.arrow(sx + 190, y + 28, sx + 216, y + 28)
        s += A.rect(sx + 220, y + 5, 128, 46, "#ffffff", stroke, rx=6)
        s += A.txt(sx + 284, y + 33, coder, 13, stroke, weight="bold")
        s += A.arrow(sx + 352, y + 28, sx + 380, y + 28)
        s += ('<path d="M 428 %d L 428 %d L %d %d" stroke="#444" '
              'stroke-width="1.4" fill="none"/>\n'
              % (y1 + BH / 2, y + 28, sx - 8, y + 28))
        s += A.arrow(sx - 10, y + 28, sx - 2, y + 28)

    s += A.rect(sx + 384, 74, 76, 176, "#f4f6f8", "#5a6a7a", rx=6)
    s += A.txt(sx + 422, 156, "saspiests", 12.5, "#16324f", weight="bold")
    s += A.txt(sx + 422, 172, "bloks", 12.5, "#16324f", weight="bold")
    s += A.txt(20, 306, "Katra bloka galvenē glabā arī sablīvētas frekvenču "
                        "tabulas, tāpēc atkodētājs uzbūvē tieši tās pašas "
                        "FSE tabulas.", 12.5, "#444", "start")
    return s


def main():
    args = A.parser(__file__, "Zstandard bloka shēma").parse_args()
    A.write(args.out, build())


if __name__ == "__main__":
    main()
