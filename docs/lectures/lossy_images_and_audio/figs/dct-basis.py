# -*- coding: utf-8 -*-
"""Ģenerē dct-basis.svg -- DCT-II bāzes vektorus garumā N = 8.

k-tais bāzes vektors ir matricas C k-tā rinda:
    c_k[n] = alpha_k * cos(pi (2n + 1) k / 16),  n = 0..7,
kur alpha_0 = sqrt(1/8), alpha_k = sqrt(2/8).  Signāls x = sum_k y_k c_k,
tātad koeficients y_k ir k-tā vektora "daudzums" signālā.
Punkti -- vektora elementi; plānā līnija -- kosinusoīda, no kuras tie ņemti.

Uzraksti ir latviski (dct-basis.svg) un angliski (dct-basis.en.svg):

    python dct-basis.py              # abas valodas
    python dct-basis.py --lang en    # tikai angļu
"""

import importlib.util
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "jpeg_pipeline", os.path.join(HERE, "jpeg-pipeline.py"))
J = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(J)

N = 8


def alpha(k):
    return math.sqrt(1 / N) if k == 0 else math.sqrt(2 / N)


def basis(k, n):
    return alpha(k) * math.cos(math.pi * (2 * n + 1) * k / (2 * N))


def panel(x, y, k):
    w, h = 200, 110
    step = w / N
    y0 = y + h / 2
    scale = (h / 2 - 8) / 0.5              # |c_k[n]| <= 0.5
    s = J.rect(x, y, w, h, "#f8f9fb", "#c9d3de", 1, 4)
    s += J.line(x, y0, x + w, y0, "#9aa5b1", 0.8)
    pts = []
    for i in range(0, 161):
        t = -0.5 + N * i / 160             # nepārtraukts "n" no -0.5 līdz 7.5
        pts.append("%.1f,%.1f" % (x + (t + 0.5) * step,
                                  y0 - scale * alpha(k) * math.cos(math.pi * (2 * t + 1) * k / (2 * N))))
    s += ('<polyline points="%s" fill="none" stroke="%s" stroke-width="1" '
          'stroke-opacity="0.5"/>\n' % (" ".join(pts), J.BLUE))
    for n in range(N):
        px = x + (n + 0.5) * step
        py = y0 - scale * basis(k, n)
        s += J.line(px, y0, px, py, J.BLUE, 2)
        s += '<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>\n' % (px, py, J.BLUE)
    label = "k = 0 (DC)" if k == 0 else "k = %d" % k
    s += J.txt(x + w / 2, y - 8, label, 12.5, J.INK, weight="bold")
    return s


def build(lang="lv"):
    name = "DCT basis vectors" if lang == "en" else "DCT bāzes vektori"
    title = ("DCT-II basis vectors, N = 8" if lang == "en"
             else "DCT-II bāzes vektori, N = 8")
    W, H = 900, 320
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'width="%d" height="%d" role="img" aria-label="%s">\n'
         '<title>%s</title>\n' % (W, H, W, H, name, title))
    s += J.rect(0, 0, W, H, "#ffffff", "none", 0)
    for k in range(N):
        s += panel(20 + (k % 4) * 220, 30 + (k // 4) * 150, k)
    s += "</svg>\n"
    return s


def main():
    J.write_svgs("dct-basis", build, __doc__.splitlines()[0])


if __name__ == "__main__":
    main()
