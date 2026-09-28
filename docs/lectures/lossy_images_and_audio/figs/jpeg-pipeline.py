# -*- coding: utf-8 -*-
"""Ģenerē jpeg-pipeline.svg -- JPEG kodēšanas soļu shēmu (1.-7. solis).

Shēmā soļi numurēti tāpat kā lekcijā (index.lv.md, "JPEG iekodēšana").
8x8 bloka skaitļi ir īsti: paraugbloku (Wikipedia "JPEG" piemērs) pārveido ar
DCT-II (B = C A C^T), kvantizē ar standarta gaišuma tabulu un nolasa zig-zag
secībā.

    python jpeg-pipeline.py
"""

import os

import numpy as np

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Consolas, Menlo, monospace"
BLUE, ORANGE, GREEN, PURPLE, RED = "#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756"
INK, GRID = "#222", "#9aa5b1"

# Paraugbloks (gaišums Y, 0..255) un JPEG standarta gaišuma kvantizācijas tabula.
BLOCK = np.array([
    [52, 55, 61, 66, 70, 61, 64, 73],
    [63, 59, 55, 90, 109, 85, 69, 72],
    [62, 59, 68, 113, 144, 104, 66, 73],
    [63, 58, 71, 122, 154, 106, 70, 69],
    [67, 61, 68, 104, 126, 88, 68, 70],
    [79, 65, 60, 70, 77, 68, 58, 75],
    [85, 71, 64, 59, 55, 61, 65, 83],
    [87, 79, 69, 68, 65, 76, 78, 94]])
QTABLE = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]])


def dct2(a):
    """DCT-II 8x8 blokam: B = C A C^T (kā lekcijā)."""
    k, n = np.meshgrid(range(8), range(8), indexing="ij")
    c = np.cos((2 * n + 1) * k * np.pi / 16)
    c[0, :] *= np.sqrt(1 / 8)
    c[1:, :] *= np.sqrt(2 / 8)
    return c @ a @ c.T


def zigzag_order():
    """Pozīcijas (rinda, kolonna) zig-zag secībā."""
    return sorted(((i, j) for i in range(8) for j in range(8)),
                  key=lambda p: (p[0] + p[1],
                                 p[1] if (p[0] + p[1]) % 2 == 0 else p[0]))


# --- SVG palīgfunkcijas -------------------------------------------------------

def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal",
        family=FONT, style="normal", raw=False):
    if not raw:
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s" font-style="%s">%s</text>\n'
            % (x, y, family, size, fill, anchor, weight, style, s))


def rect(x, y, w, h, fill="#fff", stroke=INK, sw=1.4, rx=0, extra=""):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
            'stroke="%s" stroke-width="%g"%s/>\n'
            % (x, y, w, h, rx, fill, stroke, sw, extra))


def line(x1, y1, x2, y2, stroke="#444", sw=1.6, extra=""):
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" '
            'stroke-width="%g"%s/>\n' % (x1, y1, x2, y2, stroke, sw, extra))


def arrow(x1, y1, x2, y2, sw=2.2):
    return line(x1, y1, x2, y2, "#444", sw, ' marker-end="url(#arw)"')


def path_arrow(points, sw=2.2):
    d = " ".join(("M" if i == 0 else "L") + " %g %g" % p
                 for i, p in enumerate(points))
    return ('<path d="%s" stroke="#444" stroke-width="%g" fill="none" '
            'marker-end="url(#arw)"/>\n' % (d, sw))


def sub(s):
    """Apakšindekss teksta rindā."""
    return ('<tspan baseline-shift="sub" font-size="75%%">%s</tspan>' % s)


def badge(x, y, n):
    """Soļa numurs aplītī."""
    return ('<circle cx="%g" cy="%g" r="11" fill="%s"/>\n' % (x, y, BLUE)
            + txt(x, y + 4.5, str(n), 13, "#fff", weight="bold"))


def plane(x, y, size, fill, stroke, letter=None, cells=8):
    """Attēla plakne ar pikseļu režģi un burtu augšējā labajā stūrī."""
    s = rect(x, y, size, size, fill, stroke, 1.4)
    step = size / cells
    for i in range(1, cells):
        s += line(x + i * step, y, x + i * step, y + size, stroke, 0.5,
                  ' stroke-opacity="0.5"')
        s += line(x, y + i * step, x + size, y + i * step, stroke, 0.5,
                  ' stroke-opacity="0.5"')
    if letter:
        s += txt(x + size - 3, y + 13, letter, 12, stroke, "end", weight="bold")
    return s


def stack(x, y, size, d, layers):
    """Vairākas plaknes cita aiz citas (pēdējā -- priekšā)."""
    s = ""
    n = len(layers)
    for i, (fill, stroke, letter) in enumerate(layers):
        k = n - 1 - i
        s += plane(x + k * d, y + i * d, size, fill, stroke, letter)
    return s


def matrix(x, y, cell, fills=None, numbers=None, highlight=None, overlay=""):
    """8x8 matrica: šūnu krāsas un (neobligāti) skaitļi."""
    s = ""
    for i in range(8):
        for j in range(8):
            f = fills[i][j] if fills else "#fff"
            s += rect(x + j * cell, y + i * cell, cell, cell, f, GRID, 0.6)
    if highlight:
        i, j, col = highlight
        s += rect(x + j * cell, y + i * cell, cell, cell, "none", col, 2.4)
    s += rect(x, y, 8 * cell, 8 * cell, "none", INK, 1.4)
    s += overlay
    if numbers is not None:
        for i in range(8):
            for j in range(8):
                v = int(numbers[i][j])
                s += txt(x + (j + 0.5) * cell, y + (i + 0.5) * cell + 4,
                         str(v).replace("-", "−"), 10,
                         INK if v else "#b8c0c8",
                         weight="bold" if v else "normal")
    return s


def build():
    W, H = 980, 700
    coef = dct2(BLOCK - 128.0)
    quant = np.round(coef / QTABLE).astype(int)
    order = zigzag_order()
    zz = [quant[i][j] for i, j in order]

    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'width="%d" height="%d" role="img" aria-label="JPEG kodēšanas soļi">\n'
         '<title>JPEG kodēšanas soļi</title>\n' % (W, H, W, H))
    s += rect(0, 0, W, H, "#ffffff", "none", 0)
    s += ('<defs>\n  <marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" '
          'markerWidth="6" markerHeight="6" orient="auto-start-reverse">\n'
          '    <path d="M 0 0 L 10 5 L 0 10 z" fill="#444"/>\n'
          '  </marker>\n</defs>\n')
    s += txt(20, 28, "JPEG kodēšana: 1.–7. solis", 15, INK, "start",
             weight="bold")

    # --- 1. rinda: krāsu telpa, izretināšana, bloki -------------------------
    s += stack(20, 64, 104, 16, [("#dbe6f3", BLUE, "B"),
                                 ("#dcecd8", GREEN, "G"),
                                 ("#fbdcdc", RED, "R")])
    s += txt(88, 222, "RGB attēls", 12)

    s += arrow(160, 136, 236, 136)
    s += badge(198, 114, 1)
    s += txt(198, 158, "RGB → YCbCr", 12)

    s += stack(248, 64, 104, 16, [("#ecdcea", PURPLE, "Cr"),
                                  ("#fde5cc", ORANGE, "Cb"),
                                  ("#e9ecef", "#5a6a7a", "Y")])
    s += txt(316, 222, "Y (gaišums), Cb, Cr (krāsa)", 12)

    s += arrow(386, 136, 462, 136)
    s += badge(424, 114, 2)
    s += txt(424, 158, "4:2:0", 12)

    s += plane(474, 72, 116, "#e9ecef", "#5a6a7a", "Y")
    s += plane(602, 72, 56, "#fde5cc", ORANGE, "Cb", cells=4)
    s += plane(602, 132, 56, "#ecdcea", PURPLE, "Cr", cells=4)
    s += txt(566, 222, "Cb, Cr: vidējais katrā 2×2", 12)

    s += arrow(670, 136, 734, 136)
    s += badge(702, 114, 3)
    s += txt(702, 158, "8×8 bloki", 12)

    gx, gy, bs = 746, 66, 26
    s += rect(gx, gy, 8 * bs, 5 * bs, "#e9ecef", "#5a6a7a", 1.4)
    for i in range(1, 8):
        s += line(gx + i * bs, gy, gx + i * bs, gy + 5 * bs, "#5a6a7a", 0.8)
    for i in range(1, 5):
        s += line(gx, gy + i * bs, gx + 8 * bs, gy + i * bs, "#5a6a7a", 0.8)
    hx, hy = gx + 3 * bs, gy + 1 * bs
    s += rect(hx, hy, bs, bs, "#fde5cc", ORANGE, 2.2)
    s += txt(gx + 4 * bs, 56, "Y plakne, sadalīta 8×8 blokos", 12)

    # --- 2. rinda (no labās uz kreiso): DCT, kvantizācija, zig-zag ----------
    px, py, pc = 790, 290, 19
    dash = ' stroke-dasharray="5 4"'
    s += line(hx, hy + bs, px, py, ORANGE, 1.2, dash)
    s += line(hx + bs, hy + bs, px + 8 * pc, py, ORANGE, 1.2, dash)
    grays = [["rgb(%d,%d,%d)" % (v, v, v) for v in row] for row in BLOCK]
    s += matrix(px, py, pc, fills=grays)
    s += txt(px + 4 * pc, py + 8 * pc + 20, "viens 8×8 bloks (pikseļi)", 12)

    s += arrow(782, 366, 716, 366)
    s += badge(749, 344, 4)
    s += txt(749, 388, "DCT-II", 12)

    cx, cy, cc = 556, 290, 19
    mag = np.log1p(np.abs(coef)) / np.log1p(np.abs(coef).max())
    heat = [["rgba(76,120,168,%.2f)" % (0.08 + 0.92 * m) for m in row]
            for row in mag]
    s += matrix(cx, cy, cc, fills=heat)
    s += txt(cx + 4 * cc, cy + 8 * cc + 20, "DCT koeficienti", 12)
    s += txt(cx + 4 * cc, cy + 8 * cc + 36,
             "(zemās frekvences augšā pa kreisi)", 11, "#555")

    s += arrow(548, 366, 448, 366)
    s += badge(498, 344, 5)
    s += txt(498, 388, "kvantizācija", 12)
    s += txt(498, 404, "÷ Q" + sub("u,v") + ", noapaļo", 11, "#555", raw=True)

    qx, qy, qc = 240, 266, 25
    pts = " ".join("%g,%g" % (qx + (j + 0.5) * qc, qy + (i + 0.5) * qc)
                   for i, j in order)
    zig = ('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.6" '
           'stroke-opacity="0.45" stroke-linejoin="round"/>\n' % (pts, RED))
    s += matrix(qx, qy, qc, numbers=quant, highlight=(0, 0, ORANGE),
                overlay=zig)
    s += txt(qx + 4 * qc, qy + 8 * qc + 20, "kvantizēts bloks;", 12)
    s += txt(qx + 4 * qc, qy + 8 * qc + 36, "sarkanā līnija — zig-zag secība",
             11, "#555")

    s += path_arrow([(232, 366), (110, 366), (110, 538)])
    s += badge(171, 344, 6)
    s += txt(171, 388, "DC un AC", 12)
    s += txt(171, 404, "atdala", 12)

    # --- 3. rinda: DC starpības, AC virkne, entropijas kodēšana, fails ------
    dc = zz[0]
    ac = zz[1:]
    last = max(k for k, v in enumerate(ac) if v) + 1
    shown = " ".join(str(v).replace("-", "−") for v in ac[:14])

    s += rect(20, 546, 400, 52, "#fff4e8", ORANGE, 1.4, 6)
    s += txt(32, 566, "DC = %s (atbilst bloka vidējam gaišumam)"
             % str(dc).replace("-", "−"), 12, INK, "start", weight="bold")
    s += txt(32, 586, "kodē starpību ar iepriekšējā bloka DC: "
             "DC" + sub("k") + " − DC" + sub("k−1"), 12, INK, "start",
             raw=True)

    s += rect(20, 610, 400, 72, "#eef3f9", BLUE, 1.4, 6)
    s += txt(32, 630, "AC (63 koeficienti) zig-zag secībā:", 12, INK, "start",
             weight="bold")
    s += txt(32, 650, shown + " …", 12, INK, "start", family=MONO)
    s += txt(32, 670, "pēc %d. vietas tikai nulles → RLE, beigās EOB"
             % last, 12, INK, "start")

    s += line(420, 572, 440, 572, "#444", 1.6)
    s += line(420, 646, 440, 646, "#444", 1.6)
    s += line(440, 572, 440, 646, "#444", 1.6)
    s += arrow(440, 609, 548, 609)
    s += badge(494, 587, 7)
    s += txt(494, 631, "Hafmana vai", 12)
    s += txt(494, 647, "aritmētiskā", 12)
    s += txt(494, 663, "kodēšana", 12)

    s += txt(552, 613, "1100 0101 0100…", 11.5, INK, "start", family=MONO)
    s += arrow(662, 609, 684, 609)
    fx, fy = 690, 589
    segs = [("SOI", 34), ("galvene, tabulas", 104), ("saspiestie dati", 100),
            ("EOI", 34)]
    for label, w in segs:
        s += rect(fx, fy, w, 40, "#f4f6f8", "#5a6a7a", 1.4)
        s += txt(fx + w / 2, fy + 25, label, 11.5)
        fx += w
    s += txt(690 + 136, fy + 60, "JPEG (JFIF) fails", 12)

    s += "</svg>\n"
    return s


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "jpeg-pipeline.svg")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build())
    print("Wrote", out)


if __name__ == "__main__":
    main()
