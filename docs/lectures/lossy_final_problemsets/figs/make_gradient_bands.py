# -*- coding: utf-8 -*-
"""Izveido sintētisku testa attēlu gradient-bands.png (512 x 384 pikseļi).

Attēlā ir sešas horizontālas joslas (katra 64 pikseļus augsta):

1. pelēktoņu gradients no melnas (pa kreisi) līdz baltai (pa labi);
2. sarkanā kanāla gradients (G = B = 0);
3. zaļā kanāla gradients;
4. zilā kanāla gradients;
5. krāsu loks: nokrāsa (hue) mainās no 0 līdz 360 grādiem, piesātinājums 1;
6. pelēks fons ar plānām (1 pikseli platām) vertikālām melnām un baltām līnijām
   ik pēc 8 pikseļiem, kas sākas 3. kolonnā (līnijas nesakrīt ar 8 x 8 bloku robežām).

Vajadzīgs Pillow un NumPy:

    pip install pillow numpy
    python make_gradient_bands.py
"""

import colorsys
import os

import numpy as np
from PIL import Image

W, H = 512, 384
BAND = H // 6


def main():
    img = np.zeros((H, W, 3), dtype=np.float64)
    ramp = np.linspace(0, 255, W)
    img[0 * BAND:1 * BAND, :, :] = ramp[None, :, None]
    for channel in range(3):
        img[(1 + channel) * BAND:(2 + channel) * BAND, :, channel] = ramp[None, :]
    hues = np.array([colorsys.hsv_to_rgb(x / W, 1.0, 1.0) for x in range(W)]) * 255
    img[4 * BAND:5 * BAND, :, :] = hues[None, :, :]
    img[5 * BAND:6 * BAND, :, :] = 128
    for x in range(3, W, 8):
        img[5 * BAND:6 * BAND, x, :] = 0 if (x // 8) % 2 == 0 else 255

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gradient-bands.png")
    Image.fromarray(np.round(img).astype(np.uint8), "RGB").save(out)
    print("Wrote", out)


if __name__ == "__main__":
    main()
