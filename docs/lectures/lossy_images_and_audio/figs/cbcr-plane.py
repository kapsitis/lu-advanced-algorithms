# -*- coding: utf-8 -*-
"""Ģenerē cbcr-plane.svg -- YCbCr krāsu telpas CbCr plakni, ja Y = 128.

Katram (Cb, Cr) no 0..255 krāsu aprēķina ar JFIF formulām
    R = Y + 1.402 (Cr - 128)
    G = Y - 0.344136 (Cb - 128) - 0.714136 (Cr - 128)
    B = Y + 1.772 (Cb - 128)
un apgriež līdz 0..255.  Krāsu laukums ir iegults kā PNG attēls, asis un
uzraksti -- SVG teksts.

Uzraksti ir latviski (cbcr-plane.svg) un angliski (cbcr-plane.en.svg):

    python cbcr-plane.py              # abas valodas
    python cbcr-plane.py --lang en    # tikai angļu
"""

import argparse
import base64
import io
import os

import numpy as np
from PIL import Image

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
Y = 128


def plane_png():
    cb, cr = np.meshgrid(np.arange(256), np.arange(255, -1, -1))  # Cr aug uz augšu
    r = Y + 1.402 * (cr - 128)
    g = Y - 0.344136 * (cb - 128) - 0.714136 * (cr - 128)
    b = Y + 1.772 * (cb - 128)
    rgb = np.clip(np.round(np.stack([r, g, b], axis=-1)), 0, 255).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(rgb, "RGB").save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def txt(x, y, s, size=12, anchor="middle", weight="normal", fill="#222"):
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s">%s</text>\n'
            % (x, y, FONT, size, fill, anchor, weight, s))


def build(lang="lv"):
    title = ("CbCr plane for Y = 128" if lang == "en"
             else "CbCr plakne, ja Y = 128")
    X0, Y0, S = 56, 20, 256
    W, H = X0 + S + 24, Y0 + S + 52
    s = ('<svg xmlns="http://www.w3.org/2000/svg" '
         'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 %d %d" '
         'width="%d" height="%d" role="img" aria-label="%s">\n'
         '<title>%s</title>\n' % (W, H, W, H, title, title))
    s += '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n' % (W, H)
    s += ('<image x="%d" y="%d" width="%d" height="%d" '
          'preserveAspectRatio="none" style="image-rendering:pixelated" '
          'xlink:href="data:image/png;base64,%s"/>\n' % (X0, Y0, S, S, plane_png()))
    s += ('<rect x="%d" y="%d" width="%d" height="%d" fill="none" '
          'stroke="#222" stroke-width="1.2"/>\n' % (X0, Y0, S, S))
    # Asis caur neitrālo punktu (Cb, Cr) = (128, 128), kas ir pelēks.
    cx, cy = X0 + 128, Y0 + S - 128
    s += ('<line x1="%d" y1="%g" x2="%d" y2="%g" stroke="#fff" stroke-width="1" '
          'stroke-opacity="0.8"/>\n' % (X0, cy, X0 + S, cy))
    s += ('<line x1="%g" y1="%d" x2="%g" y2="%d" stroke="#fff" stroke-width="1" '
          'stroke-opacity="0.8"/>\n' % (cx, Y0, cx, Y0 + S))
    for v in (0, 64, 128, 192, 255):
        x = X0 + v + 0.5
        y = Y0 + S - v - 0.5
        s += ('<line x1="%g" y1="%d" x2="%g" y2="%d" stroke="#222"/>\n'
              % (x, Y0 + S, x, Y0 + S + 5))
        s += txt(x, Y0 + S + 18, str(v), 11)
        s += ('<line x1="%d" y1="%g" x2="%d" y2="%g" stroke="#222"/>\n'
              % (X0 - 5, y, X0, y))
        s += txt(X0 - 8, y + 4, str(v), 11, "end")
    s += txt(X0 + S / 2, Y0 + S + 40, "Cb", 13, weight="bold")
    s += ('<text x="16" y="%g" font-family="%s" font-size="13" fill="#222" '
          'text-anchor="middle" font-weight="bold" '
          'transform="rotate(-90 16 %g)">Cr</text>\n'
          % (Y0 + S / 2, FONT, Y0 + S / 2))
    s += "</svg>\n"
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lang", choices=["lv", "en", "all"], default="all",
                    help="uzrakstu valoda (noklusēti abas)")
    langs = {"lv": ["lv"], "en": ["en"], "all": ["lv", "en"]}[ap.parse_args().lang]
    here = os.path.dirname(os.path.abspath(__file__))
    for lang in langs:
        out = os.path.join(here, "cbcr-plane" + (".en" if lang == "en" else "") + ".svg")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(build(lang))
        print("Wrote", out)


if __name__ == "__main__":
    main()
