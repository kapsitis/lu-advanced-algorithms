# -*- coding: utf-8 -*-
"""Ģenerē p-frame-encoding.svg -- P-freima makrobloka kodēšana ar kustības vektoru.

Sintētisks piemērs ar īstiem pikseļiem (gaišuma plakne 64 x 48, makrobloki 16 x 16):

* atsauces kadrā (reference frame) uz vienkrāsaina fona ir svītraina figūriņa;
* pašreizējā kadrā (current frame) figūriņa ir nobīdījusies par (+6, +3) pikseļiem
  un kļuvusi par 4 vienībām gaišāka (piemēram, mainījies apgaismojums);
* iekodētājs pašreizējā kadra makroblokam ar pilnu pārlasi (SAD) meklē
  līdzīgāko 16 x 16 apgabalu atsauces kadrā; nobīde līdz tam ir kustības
  vektors (MV);
* kodē MV un atlikumu = bloks - prognoze. Salīdzinājumam parādīts arī atlikums
  bez kustības kompensācijas (MV = 0).

Kadri iegulti kā nelieli PNG attēli (palielināti bez izplūšanas), shēma --
SVG elementi.

    python p_frame_encoding.py
"""

import base64
import io
import os

import numpy as np
from PIL import Image

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Consolas, Menlo, monospace"
INK, BLUE, ORANGE, GREEN, RED = "#222", "#4C78A8", "#F58518", "#54A24B", "#E45756"

W_F, H_F, MB = 64, 48, 16
BG = 110
SHIFT = (6, 3)            # figūriņas nobīde (dx, dy) pašreizējā kadrā
BRIGHTEN = 4              # apgaismojuma izmaiņa figūriņai
TARGET = (1, 1)           # kodējamais makrobloks (kolonna, rinda)
SEARCH = 8                # meklēšanas logs +-8 pikseļi


def draw_scene(cx, cy, extra):
    """Vienkrāsains fons un svītraina elipsveida figūriņa ar centru (cx, cy)."""
    y, x = np.mgrid[0:H_F, 0:W_F]
    img = np.full((H_F, W_F), BG, dtype=int)
    inside = ((x - cx) / 11.0) ** 2 + ((y - cy) / 9.0) ** 2 <= 1.0
    stripes = np.where(((x - cx) // 4) % 2 == 0, 200, 150)
    img[inside] = stripes[inside] + extra
    return img


REF = draw_scene(23, 22, 0)
CUR = draw_scene(23 + SHIFT[0], 22 + SHIFT[1], BRIGHTEN)


def motion_search(cur, ref, bx, by):
    """Pilna pārlase: MV (dx, dy), kas minimizē SAD; prognoze = ref nobīdītā vietā."""
    block = cur[by:by + MB, bx:bx + MB]
    best = None
    for dy in range(-SEARCH, SEARCH + 1):
        for dx in range(-SEARCH, SEARCH + 1):
            x0, y0 = bx + dx, by + dy
            if 0 <= x0 <= W_F - MB and 0 <= y0 <= H_F - MB:
                sad = int(np.abs(block - ref[y0:y0 + MB, x0:x0 + MB]).sum())
                if best is None or sad < best[0]:
                    best = (sad, dx, dy)
    return best


def png_b64(arr, scale):
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "L")
    img = img.resize((arr.shape[1] * scale, arr.shape[0] * scale), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def residual_rgb(res, scale):
    """Atlikums krāsās: 0 -> balts, pozitīvs -> sarkans, negatīvs -> zils."""
    a = np.sqrt(np.clip(np.abs(res) / 60.0, 0, 1))   # nelineāri, lai redzētu arī mazas vērtības
    r = np.where(res >= 0, 255, 255 * (1 - a))
    g = 255 * (1 - a)
    b = np.where(res >= 0, 255 * (1 - a), 255)
    rgb = np.stack([r, g, b], axis=-1).astype(np.uint8)
    img = Image.fromarray(rgb, "RGB").resize((res.shape[1] * scale, res.shape[0] * scale),
                                             Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal", family=FONT):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s">%s</text>\n' % (x, y, family, size, fill, anchor, weight, s))


def image(x, y, w, h, b64):
    return ('<image x="%g" y="%g" width="%g" height="%g" preserveAspectRatio="none" '
            'style="image-rendering:pixelated" xlink:href="data:image/png;base64,%s"/>\n'
            % (x, y, w, h, b64))


def rect(x, y, w, h, stroke, sw=2, dash=None, fill="none", rx=0):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" '
            'stroke-width="%g"%s/>\n' % (x, y, w, h, rx, fill, stroke, sw, d))


def arrow(x1, y1, x2, y2, col="#444", sw=1.8):
    marker = "arwb" if col == BLUE else "arw"
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g" '
            'marker-end="url(#%s)"/>\n' % (x1, y1, x2, y2, col, sw, marker))


def frame_panel(x, y, arr, s, title):
    out = txt(x, y - 10, title, 13, INK, "start", "bold")
    out += image(x, y, W_F * s, H_F * s, png_b64(arr, s))
    for k in range(1, W_F // MB):
        out += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#fff" stroke-width="1" '
                'stroke-opacity="0.8"/>\n' % (x + k * MB * s, y, x + k * MB * s, y + H_F * s))
    for k in range(1, H_F // MB):
        out += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#fff" stroke-width="1" '
                'stroke-opacity="0.8"/>\n' % (x, y + k * MB * s, x + W_F * s, y + k * MB * s))
    out += rect(x, y, W_F * s, H_F * s, "#5a6a7a", 1.2)
    return out


def build():
    bx, by = TARGET[0] * MB, TARGET[1] * MB
    sad, dx, dy = motion_search(CUR, REF, bx, by)
    block = CUR[by:by + MB, bx:bx + MB]
    pred = REF[by + dy:by + dy + MB, bx + dx:bx + dx + MB]
    res = block - pred
    res0 = block - REF[by:by + MB, bx:bx + MB]
    sad0 = int(np.abs(res0).sum())

    W, H = 960, 600
    s = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         'viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="P-freima kodēšana">\n'
         '<title>P-freima makrobloka kodēšana ar kustības vektoru</title>\n'
         '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
         '<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
         'markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
         'fill="#444"/></marker><marker id="arwb" viewBox="0 0 10 10" refX="9" refY="5" '
         'markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
         'fill="#4C78A8"/></marker></defs>\n' % (W, H, W, H, W, H))

    S = 5                                  # kadru palielinājums
    fx, fy_ref, fy_cur = 20, 44, 340
    s += frame_panel(fx, fy_ref, REF, S, "atsauces kadrs (reference frame)")
    s += frame_panel(fx, fy_cur, CUR, S, "pašreizējais kadrs (current frame)")
    # kodējamais makrobloks pašreizējā kadrā
    s += rect(fx + bx * S, fy_cur + by * S, MB * S, MB * S, ORANGE, 3)
    # tā pati vieta atsauces kadrā (pārtraukti) un labākā sakritība (zaļi)
    s += rect(fx + bx * S, fy_ref + by * S, MB * S, MB * S, ORANGE, 2, "6 4")
    s += rect(fx + (bx + dx) * S, fy_ref + (by + dy) * S, MB * S, MB * S, GREEN, 3)
    c0 = (fx + (bx + MB / 2) * S, fy_ref + (by + MB / 2) * S)
    c1 = (fx + (bx + dx + MB / 2) * S, fy_ref + (by + dy + MB / 2) * S)
    s += ('<circle cx="%g" cy="%g" r="3.5" fill="%s"/>' % (c0[0], c0[1], BLUE)) + chr(10)
    s += arrow(c0[0], c0[1], c1[0], c1[1], BLUE, 3)
    s += txt(fx + W_F * S + 10, fy_ref + (by + dy) * S + 10, "labākā sakritība", 11.5, GREEN, "start")
    s += txt(fx + W_F * S + 10, fy_ref + by * S + MB * S - 4, "tā pati vieta", 11.5, ORANGE, "start")
    s += txt(fx + W_F * S + 10, fy_ref + by * S + MB * S + 12, "kā pašreizējā blokā", 11.5, ORANGE, "start")
    s += txt(fx + W_F * S + 10, fy_cur + by * S + MB * S / 2, "kodējamais", 11.5, ORANGE, "start")
    s += txt(fx + W_F * S + 10, fy_cur + by * S + MB * S / 2 + 15, "makrobloks 16×16", 11.5, ORANGE, "start")
    s += txt(fx, fy_ref + H_F * S + 20, "kustības vektors MV = (%+d, %+d)" % (dx, dy), 12.5, BLUE, "start", "bold")

    # --- izgrieztie bloki un atlikumi ------------------------------------------
    B = 5
    bw = MB * B
    cx0, cy0 = 480, 76
    s += txt(cx0 + bw / 2, cy0 - 26, "pašreizējais", 12, INK, weight="bold")
    s += txt(cx0 + bw / 2, cy0 - 10, "bloks", 12, INK, weight="bold")
    s += image(cx0, cy0, bw, bw, png_b64(block, B)) + rect(cx0, cy0, bw, bw, ORANGE, 2.5)
    px0 = cx0 + bw + 50
    s += txt(px0 + bw / 2, cy0 - 26, "prognoze", 12, INK, weight="bold")
    s += txt(px0 + bw / 2, cy0 - 10, "(atsauce + MV)", 12, INK, weight="bold")
    s += image(px0, cy0, bw, bw, png_b64(pred, B)) + rect(px0, cy0, bw, bw, GREEN, 2.5)
    s += txt(cx0 + bw + 25, cy0 + bw / 2 + 6, "−", 22, INK, weight="bold")

    rx0, ry0 = cx0 + (bw + 50) / 2, cy0 + bw + 50
    s += txt(rx0 + bw / 2, ry0 - 12, "atlikums = bloks − prognoze", 12, INK, weight="bold")
    s += image(rx0, ry0, bw, bw, residual_rgb(res, B)) + rect(rx0, ry0, bw, bw, "#5a6a7a", 1.2)
    s += arrow(rx0 + bw / 2, cy0 + bw + 6, rx0 + bw / 2, ry0 - 22)
    vals = sorted(set(res.ravel().tolist()))
    s += txt(rx0 + bw / 2, ry0 + bw + 18, "vērtības: %s; SAD = %d" % (", ".join(map(str, vals)), sad),
             11.5, "#333")

    zx0 = rx0
    zy0 = ry0 + bw + 58
    s += txt(zx0 - 16, zy0 + bw / 2 - 8, "salīdzinājumam:", 11.5, "#555", "end")
    s += txt(zx0 - 16, zy0 + bw / 2 + 8, "bez kustības (MV = 0)", 11.5, "#555", "end")
    s += image(zx0, zy0, bw, bw, residual_rgb(res0, B)) + rect(zx0, zy0, bw, bw, "#5a6a7a", 1.2)
    s += txt(zx0 + bw / 2, zy0 + bw + 18, "lielas vērtības; SAD = %d" % sad0, 11.5, "#333")

    # --- kas tiek nosūtīts ------------------------------------------------------
    qx = 760
    s += ('<rect x="%g" y="%g" width="180" height="56" rx="6" fill="#dbe6f3" stroke="%s" '
          'stroke-width="1.4"/>\n' % (qx, 60, BLUE))
    s += txt(qx + 90, 84, "kustības vektors", 12, INK, weight="bold")
    s += txt(qx + 90, 102, "(%+d, %+d)" % (dx, dy), 12, INK, family=MONO)
    s += ('<rect x="%g" y="%g" width="180" height="70" rx="6" fill="#fde5cc" stroke="%s" '
          'stroke-width="1.4"/>\n' % (qx, 200, ORANGE))
    s += txt(qx + 90, 224, "transformācija", 12, INK, weight="bold")
    s += txt(qx + 90, 241, "+ kvantizācija", 12, INK, weight="bold")
    s += txt(qx + 90, 259, "(tikai atlikumam)", 11, "#444")
    s += arrow(rx0 + bw + 8, ry0 + bw / 2, qx - 6, 235)
    s += ('<rect x="%g" y="%g" width="180" height="56" rx="6" fill="#dcecd8" stroke="%s" '
          'stroke-width="1.4"/>\n' % (qx, 320, GREEN))
    s += txt(qx + 90, 344, "entropijas kods", 12, INK, weight="bold")
    s += txt(qx + 90, 362, "(CAVLC vai CABAC)", 11, "#444")
    s += arrow(qx + 90, 272, qx + 90, 316)
    s += ('<path d="M %g %g L %g %g L %g %g" stroke="#444" stroke-width="1.8" fill="none" '
          'marker-end="url(#arw)"/>\n' % (qx + 184, 88, qx + 196, 88, qx + 196, 340))
    s += ('<line x1="%g" y1="340" x2="%g" y2="340" stroke="#444" stroke-width="1.8" '
          'marker-end="url(#arw)"/>\n' % (qx + 196, qx + 184))
    s += arrow(qx + 90, 378, qx + 90, 410)
    s += txt(qx + 90, 428, "0100110…", 13, INK, family=MONO)
    return s + "</svg>\n", (dx, dy, sad, sad0, vals)


def main():
    svg, info = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "p-frame-encoding.svg")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("Wrote", out)
    print("MV = (%+d, %+d), SAD ar MV = %d, SAD bez MV = %d, atlikuma vērtības %s" % info)


if __name__ == "__main__":
    main()
