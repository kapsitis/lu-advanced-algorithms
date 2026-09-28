# -*- coding: utf-8 -*-
"""Izveido animētu AVIF failu bouncing-ball.avif: bumba 16:9 taisnstūrī.

Vienkrāsaina bumba pārvietojas 45 grādu leņķī pa gaišu fonu un atstarojas no
malām tādā pašā leņķī.  Animācija ir bezšuvju cilpa:

* bumbas centrs pa x ass pārvietojas intervālā garumā A = W - 2R, pa y ass --
  intervālā garumā B = H - 2R.  Ar W, H, R = 640, 360, 40 ir A = 560, B = 280,
  tātad kustība atkārtojas ik pēc 2A = 1120 pikseļiem (tas dalās arī ar 2B);
* ātrums STEP = 4 pikseļi kadrā, tātad cilpā ir 1120 / 4 = 280 kadri
  (50 kadri sekundē -> 5.6 sekundes);
* bumba sāk kreisās malas vidū, tāpēc tā nekad netrāpa tieši stūrī.

Malas nogludina (anti-aliasing): katram pikselim aprēķina, kāda tā daļa ir
bumbas iekšpusē (4 x 4 apakšpikseļi), un sajauc fona un bumbas krāsu šajā
proporcijā.  Tāpēc bumba izskatās apaļa arī tad, ja tās centrs nav pikseļa
centrā.

Vajadzīgs Pillow ar AVIF atbalstu (jaunākās Pillow versijas to satur jau
iebūvētu; skripts pārbaudīts ar Pillow 12.1):

    pip install pillow numpy
    python animated_avif.py
"""

import os

import numpy as np
from PIL import Image

W, H = 640, 360            # 16:9
R = 40                     # bumbas rādiuss (pikseļos)
STEP = 4                   # pārvietojums pa katru asi vienā kadrā
FPS = 50
BACKGROUND = (244, 241, 232)
BALL = (76, 120, 168)
SUPERSAMPLE = 4            # apakšpikseļi katrā virzienā (anti-aliasing)


def bounce(t, length):
    """Trīsstūra vilnis: vieta 0..length, kas atstarojas no abiem galiem."""
    t %= 2 * length
    return t if t <= length else 2 * length - t


def coverage(cx, cy):
    """Katram pikselim: kāda daļa no tā ir apļa iekšpusē (0..1)."""
    s = SUPERSAMPLE
    offsets = (np.arange(s) + 0.5) / s                     # apakšpikseļu centri
    xs = (np.arange(W)[:, None] + offsets[None, :]).ravel()  # W*s
    ys = (np.arange(H)[:, None] + offsets[None, :]).ravel()  # H*s
    inside = ((xs[None, :] - cx) ** 2 + (ys[:, None] - cy) ** 2) <= R * R
    return inside.reshape(H, s, W, s).mean(axis=(1, 3))


def frame(cx, cy):
    a = coverage(cx, cy)[..., None]
    rgb = (1 - a) * np.array(BACKGROUND) + a * np.array(BALL)
    return Image.fromarray(np.round(rgb).astype(np.uint8), "RGB")


def main():
    A, B = W - 2 * R, H - 2 * R
    period = 2 * A                     # 2A dalās ar 2B, jo A = 2B
    assert period % (2 * B) == 0 and period % STEP == 0
    frames = []
    for i in range(period // STEP):
        t = i * STEP
        cx = R + bounce(t, A)          # sāk pie kreisās malas
        cy = R + bounce(t + B // 2, B) # ... tās vidusdaļā
        frames.append(frame(cx, cy))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "bouncing-ball.avif")
    frames[0].save(out, format="AVIF", save_all=True, append_images=frames[1:],
                   duration=1000 // FPS, loop=0, quality=80,
                   subsampling="4:4:4")
    print("Wrote %s: %d frames, %d bytes" % (out, len(frames), os.path.getsize(out)))


if __name__ == "__main__":
    main()
