# -*- coding: utf-8 -*-
"""Ģenerē avif-pipeline.svg -- AVIF (AV1 intra kadra) kodēšanas soļu shēmu.

Tipisks gadījums: digitāla fotogrāfija, saspiesta ar zudumiem (lossy AVIF).
Soļi numurēti tāpat kā lekcijā (index.lv.md, "AVIF attēlu formāts").
Zīmēšanas palīgfunkcijas un krāsas ņemtas no jpeg-pipeline.py, lai abas
shēmas izskatītos vienādi.

    python avif-pipeline.py
"""

import importlib.util
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "jpeg_pipeline", os.path.join(HERE, "jpeg-pipeline.py"))
J = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(J)

txt, rect, line, arrow, path_arrow, badge = (
    J.txt, J.rect, J.line, J.arrow, J.path_arrow, J.badge)
BLUE, ORANGE, GREEN, PURPLE, RED, INK, GRID = (
    J.BLUE, J.ORANGE, J.GREEN, J.PURPLE, J.RED, J.INK, J.GRID)
DASH = ' stroke-dasharray="5 4"'


def partition(x, y, s, depth=0):
    """Superbloka sadalījums: dažādi kvadrāti un taisnstūri (piemērs)."""
    h = s / 2
    q = s / 4
    out = ""
    # 1. ceturksnis (augšā pa kreisi): 4 daļās, tā pirmā daļa vēlreiz 4 daļās
    out += line(x + q, y, x + q, y + h, INK, 0.9)
    out += line(x, y + q, x + h, y + q, INK, 0.9)
    out += line(x + q / 2, y, x + q / 2, y + q, INK, 0.9)
    out += line(x, y + q / 2, x + q, y + q / 2, INK, 0.9)
    # 2. ceturksnis (augšā pa labi): divi horizontāli taisnstūri
    out += line(x + h, y + q, x + s, y + q, INK, 0.9)
    # 3. ceturksnis (apakšā pa kreisi): divi vertikāli taisnstūri
    out += line(x + q, y + h, x + q, y + s, INK, 0.9)
    # 4. ceturksnis (apakšā pa labi): 4 daļās, viena no tām -- 2 vertikālos
    out += line(x + h + q, y + h, x + h + q, y + s, INK, 0.9)
    out += line(x + h, y + h + q, x + s, y + h + q, INK, 0.9)
    out += line(x + h + q + q / 2, y + h + q, x + h + q + q / 2, y + s, INK, 0.9)
    # ceturkšņu robežas
    out += line(x + h, y, x + h, y + s, INK, 1.4)
    out += line(x, y + h, x + s, y + h, INK, 1.4)
    return out


def residual_heat():
    """Paraugbloka atlikums pēc gludas (plaknes) prognozes -> DCT koeficienti."""
    a = J.BLOCK.astype(float)
    u, v = np.meshgrid(range(8), range(8), indexing="ij")
    X = np.stack([np.ones(64), u.ravel(), v.ravel()], axis=1)
    coef, *_ = np.linalg.lstsq(X, a.ravel(), rcond=None)
    res = a - (X @ coef).reshape(8, 8)
    b = J.dct2(res)
    m = np.log1p(np.abs(b)) / np.log1p(np.abs(b).max())
    return [["rgba(76,120,168,%.2f)" % (0.06 + 0.94 * t) for t in row] for row in m]


def build():
    W, H = 980, 700
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'width="%d" height="%d" role="img" aria-label="AVIF kodēšanas soļi">\n'
         '<title>AVIF kodēšanas soļi</title>\n' % (W, H, W, H))
    s += rect(0, 0, W, H, "#ffffff", "none", 0)
    s += ('<defs>\n  <marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" '
          'markerWidth="6" markerHeight="6" orient="auto-start-reverse">\n'
          '    <path d="M 0 0 L 10 5 L 0 10 z" fill="#444"/>\n'
          '  </marker>\n</defs>\n')
    s += txt(20, 28, "AVIF kodēšana (viens AV1 intra kadrs): 1.–9. solis",
             15, INK, "start", weight="bold")

    # --- 1. rinda: krāsu telpa, izretināšana, superbloki --------------------
    s += J.stack(20, 64, 104, 16, [("#dbe6f3", BLUE, "B"),
                                   ("#dcecd8", GREEN, "G"),
                                   ("#fbdcdc", RED, "R")])
    s += txt(88, 222, "RGB fotogrāfija", 12)

    s += arrow(160, 136, 236, 136)
    s += badge(198, 114, 1)
    s += txt(198, 158, "RGB → YCbCr", 12)

    s += J.stack(248, 64, 104, 16, [("#ecdcea", PURPLE, "Cr"),
                                    ("#fde5cc", ORANGE, "Cb"),
                                    ("#e9ecef", "#5a6a7a", "Y")])
    s += txt(316, 222, "Y, Cb, Cr", 12)

    s += arrow(386, 136, 462, 136)
    s += badge(424, 114, 2)
    s += txt(424, 158, "4:2:0", 12)
    s += txt(424, 174, "(vai 4:4:4)", 10.5, "#555")

    s += J.plane(474, 72, 116, "#e9ecef", "#5a6a7a", "Y")
    s += J.plane(602, 72, 56, "#fde5cc", ORANGE, "Cb", cells=4)
    s += J.plane(602, 132, 56, "#ecdcea", PURPLE, "Cr", cells=4)
    s += txt(566, 222, "Cb, Cr: puse no izšķirtspējas", 12)

    s += arrow(670, 136, 734, 136)
    s += badge(702, 114, 3)
    s += txt(702, 158, "superbloki", 12)

    gx, gy, sb = 746, 80, 52
    s += rect(gx, gy, 4 * sb, 2 * sb, "#e9ecef", "#5a6a7a", 1.4)
    for i in range(1, 4):
        s += line(gx + i * sb, gy, gx + i * sb, gy + 2 * sb, "#5a6a7a", 1)
    s += line(gx, gy + sb, gx + 4 * sb, gy + sb, "#5a6a7a", 1)
    hx, hy = gx + sb, gy
    s += rect(hx, hy, sb, sb, "#fde5cc", ORANGE, 2.2)
    s += txt(gx + 2 * sb, 66, "Y plakne: 64×64 superbloki", 12)

    # --- 2. rinda (no labās uz kreiso): sadalījums, prognoze, transformācija --
    px, py, ps = 790, 290, 160
    s += line(hx, hy + sb, px, py, ORANGE, 1.2, DASH)
    s += line(hx + sb, hy + sb, px + ps, py, ORANGE, 1.2, DASH)
    s += rect(px, py, ps, ps, "#f4f6f8", INK, 1.4)
    s += rect(px + 40, py + 40, 40, 40, "#fde5cc", ORANGE, 2.2)  # kodējamais bloks
    s += partition(px, py, ps)
    s += rect(px, py, ps, ps, "none", INK, 1.6)
    s += txt(px + ps / 2, py + ps + 20, "rekursīvs sadalījums blokos", 12)
    s += txt(px + ps / 2, py + ps + 36, "(no 128×128 līdz 4×4, arī taisnstūri)",
             10.5, "#555")

    s += arrow(782, 366, 716, 366)
    s += badge(749, 344, 4)
    s += txt(749, 388, "intra", 12)
    s += txt(749, 404, "prognoze", 12)

    # prognoze: kaimiņu pikseļi (augšā un pa kreisi) un virziens
    bx, by, c = 564, 298, 18
    for j in range(-1, 9):
        s += rect(bx + j * c, by - c, c, c, "#c9d3de", GRID, 0.6)
    for i in range(0, 8):
        s += rect(bx - c, by + i * c, c, c, "#c9d3de", GRID, 0.6)
    s += rect(bx, by, 8 * c, 8 * c, "#fff4e8", ORANGE, 1.6)
    for x0 in (bx + 5 * c, bx + 6.5 * c, bx + 8 * c):
        s += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.8" '
              'marker-end="url(#arw)"/>\n'
              % (x0 - 2, by + 4, x0 - 4 * c, by + 4 * c + 2, ORANGE))
    s += txt(bx + 4 * c - c / 2, by + 8 * c + 22, "prognoze no jau kodētiem", 12)
    s += txt(bx + 4 * c - c / 2, by + 8 * c + 38, "kaimiņu pikseļiem;", 12)
    s += txt(bx + 4 * c - c / 2, by + 8 * c + 54, "atlikums = bloks − prognoze",
             10.5, "#555")

    s += arrow(530, 366, 448, 366)
    s += badge(489, 344, 5)
    s += txt(489, 388, "transformācija", 12)
    s += txt(489, 404, "DCT, ADST, …", 10.5, "#555")

    cx, cy, cc = 270, 290, 19
    s += J.matrix(cx, cy, cc, fills=residual_heat())
    s += txt(cx + 4 * cc, cy + 8 * cc + 20, "atlikuma koeficienti", 12)
    s += txt(cx + 4 * cc, cy + 8 * cc + 36, "(bloks 4×4 … 64×64)",
             10.5, "#555")

    s += path_arrow([(262, 366), (110, 366), (110, 540)])
    s += badge(171, 344, 6)
    s += txt(171, 388, "kvantizācija", 12)
    s += txt(171, 404, "(qindex)", 10.5, "#555")

    # --- rekonstrukcijas cilpa: nākamie bloki prognozē no atkodētā ----------
    s += ('<path d="M 440 548 L 440 520 L 538 520 L 538 440 L 552 440" '
          'stroke="%s" stroke-width="1.4" fill="none"%s marker-end="url(#arw)"/>\n'
          % ("#777", DASH))
    s += txt(450, 536, "rekonstruētie pikseļi", 10.5, "#555", "start")

    # --- 3. rinda: kvantizētie dati, filtri, entropijas kods, konteiners -----
    by3, bh = 548, 100

    def box(x, w, title, lines, n=None, fill="#f4f6f8", stroke="#5a6a7a"):
        out = rect(x, by3, w, bh, fill, stroke, 1.4, 6)
        tx = x + 12
        if n is not None:
            out += badge(x + 20, by3 + 20, n)
            tx = x + 38
        out += txt(tx, by3 + 25, title, 12, INK, "start", weight="bold")
        for i, l in enumerate(lines):
            out += txt(x + 12, by3 + 46 + 16 * i, l, 11, "#333", "start")
        return out

    s += box(20, 200, "kvantizēti dati",
             ["koeficienti + bloku", "sadalījums, prognozes", "režīmi, transformāciju",
              "tipi"], fill="#eef3f9", stroke=BLUE)
    s += arrow(222, 598, 246, 598)
    s += box(250, 200, "cilpas filtri",
             ["atjauno attēlu kā", "atkodētājs; izvēlas",
              "deblocking, CDEF un", "loop restoration"], n=7)
    s += arrow(452, 598, 476, 598)
    s += box(480, 200, "entropijas kods",
             ["adaptīvs aritmētiskais", "kods ar kontekstiem",
              "→ AV1 bitu plūsma", "(OBU)"], n=8)
    s += arrow(682, 598, 706, 598)
    s += box(710, 250, "AVIF (HEIF) fails", [], n=9)
    fx, fy = 722, by3 + 38
    for label, w in [("ftyp", 44), ("meta", 90), ("mdat", 92)]:
        s += rect(fx, fy, w, 26, "#ffffff", "#5a6a7a", 1.2)
        s += txt(fx + w / 2, fy + 17, label, 11)
        fx += w
    s += txt(722, by3 + 82, "meta: izmēri, av1C, krāsu telpa", 10.5, "#333", "start")
    s += txt(722, by3 + 95, "mdat: AV1 kadra dati", 10.5, "#333", "start")

    s += "</svg>\n"
    return s


def main():
    out = os.path.join(HERE, "avif-pipeline.svg")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build())
    print("Wrote", out)


if __name__ == "__main__":
    main()
