# -*- coding: utf-8 -*-
"""Ģenerē ecb-penguin.svg -- "ECB pingvīns": attēls, šifrēts ar AES-128 ECB un CTR režīmā.

Attēls (160 x 160 pikseļi, 1 baits pikselim, pelēktoņu) ir uzzīmēts ar Pillow,
tad tā baitus rindu pa rindai šifrē ar aes128.py: ECB režīmā katrs 16 baitu bloks
(16 pikseļi vienā rindā) tiek šifrēts atsevišķi, CTR režīmā -- pieskaitīts
(XOR) atslēgas plūsmai. Vienādas krāsas laukumi ECB režīmā kļūst par vienādiem
šifrteksta blokiem, tāpēc kontūras paliek redzamas. Trīs attēli iegulti SVG kā PNG.

    python ecb_penguin.py [--lang lv|en|both]
"""

import base64
import hashlib
import io

from PIL import Image, ImageDraw

import svgkit as K
from svgkit import T, txt
from aes128 import ecb_encrypt, ctr_encrypt

N = 160                                # attēla izmērs pikseļos
SCALE = 2                              # palielinājums SVG attēlā


def penguin():
    im = Image.new("L", (N, N), 235)                       # gaišs fons
    d = ImageDraw.Draw(im)
    d.ellipse((38, 18, 122, 150), fill=30)                 # ķermenis
    d.ellipse((56, 54, 104, 146), fill=250)                # vēders
    d.ellipse((56, 20, 104, 64), fill=30)                  # galva
    d.ellipse((64, 32, 76, 46), fill=250)                  # acis
    d.ellipse((84, 32, 96, 46), fill=250)
    d.ellipse((68, 37, 74, 44), fill=30)
    d.ellipse((86, 37, 92, 44), fill=30)
    d.polygon([(70, 50), (90, 50), (80, 62)], fill=150)    # knābis
    d.ellipse((44, 140, 76, 156), fill=150)                # kājas
    d.ellipse((84, 140, 116, 156), fill=150)
    return im


def png_uri(im):
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def build():
    key = hashlib.sha256(b"ECB pingvins").digest()[:16]
    im = penguin()
    raw = im.tobytes()
    ecb = Image.frombytes("L", (N, N), ecb_encrypt(raw, key))
    ctr = Image.frombytes("L", (N, N), ctr_encrypt(raw, key, bytes(12)))

    title = T("Viens un tas pats attēls: atklātais teksts, AES-128-ECB un AES-128-CTR",
              "The same image: plaintext, AES-128-ECB and AES-128-CTR")
    side = N * SCALE
    W, H = 3 * side + 4 * 30, side + 110
    s = K.header(W, H, title)
    s += txt(30, 28, title, 15, anchor="start", weight="bold")
    labels = [(T("atklātais teksts", "plaintext"), T("160 × 160 baiti", "160 × 160 bytes")),
              (T("ECB režīms", "ECB mode"), T("vienādi bloki → vienādi šifrteksti", "equal blocks → equal ciphertexts")),
              (T("CTR režīms", "CTR mode"), T("neatšķirams no nejauša trokšņa", "looks like random noise"))]
    for k, img in enumerate([im, ecb, ctr]):
        x = 30 + k * (side + 30)
        s += ('<image x="%d" y="50" width="%d" height="%d" style="image-rendering:pixelated" '
              'preserveAspectRatio="none" href="%s"/>\n' % (x, side, side, png_uri(img)))
        s += K.rect(x, 50, side, side, "none", "#333", 1)
        s += txt(x + side / 2, 50 + side + 24, labels[k][0], 13, weight="bold")
        s += txt(x + side / 2, 50 + side + 44, labels[k][1], 11.5, K.GREY)
    return s + "</svg>\n"


if __name__ == "__main__":
    K.main(build, "ecb-penguin.svg")
