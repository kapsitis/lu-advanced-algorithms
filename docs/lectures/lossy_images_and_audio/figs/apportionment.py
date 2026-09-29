# -*- coding: utf-8 -*-
"""Ģenerē hondt.svg un sainte-lague.svg -- vietu sadalījumu trim partijām.

Katrs vēlēšanu iznākums ir punkts vienādmalu trijstūrī ar baricentriskajām
koordinātēm (a, b, c), a + b + c = 1 (partiju A, B, C balsu daļas).
Trijstūri sadala apgabalos pēc tā, kādu vietu sadalījumu K:M:N
(K + M + N = SEATS) piešķir dalītāju metode:

* Donta (D'Hondt) metode:       dalītāji 1, 2, 3, ...
* Senlaga (Sainte-Laguë) metode: dalītāji 1, 3, 5, ...

Sadalījums s ir iespējams tieši tad, ja katrai partijai q ar s_q > 0 un katrai
partijai p:  v_q / d(s_q - 1) >= v_p / d(s_p).  Tās ir lineāras nevienādības,
tāpēc katrs apgabals ir izliekts daudzstūris; to iegūst, apgriežot trijstūri ar
pusplaknēm.  Punkts katrā apgabalā rāda balsu attiecību K:M:N, kas tieši
atbilst piešķirtajām vietām.

Uzraksti ir latviski (hondt.svg, sainte-lague.svg) un angliski
(hondt.en.svg, sainte-lague.en.svg):

    python apportionment.py              # abas valodas
    python apportionment.py --lang en    # tikai angļu
"""

import argparse
import os

SEATS = 5
FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
INK = "#222"
# Partiju krāsas (A, B, C); apgabalu krāsas ir to sajaukums.
PARTY_RGB = [(76, 120, 168), (245, 133, 24), (84, 162, 75)]

METHODS = {
    "hondt": ({"lv": "Donta (D'Hondt) metode", "en": "D'Hondt method"},
              lambda k: k + 1),
    "sainte-lague": ({"lv": "Senlaga (Sainte-Laguë) metode",
                      "en": "Sainte-Laguë method"}, lambda k: 2 * k + 1),
}
SUBTITLE = {"lv": "%d vietas, 3 partijas", "en": "%d seats, 3 parties"}

# Trijstūra virsotnes: A augšā, B apakšā pa kreisi, C apakšā pa labi.
SIDE = 400
H3 = SIDE * 3 ** 0.5 / 2
VA, VB, VC = (260, 78), (60, 78 + H3), (460, 78 + H3)
W, H = 520, 78 + H3 + 62


def to_xy(v):
    a, b, c = v
    return (a * VA[0] + b * VB[0] + c * VC[0], a * VA[1] + b * VB[1] + c * VC[1])


def clip(poly, w):
    """Sutherland-Hodgman: atstāj daudzstūra daļu, kur w . v >= 0."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = sum(wi * pi for wi, pi in zip(w, p))
        fq = sum(wi * qi for wi, qi in zip(w, q))
        if fp >= 0:
            out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append(tuple(pi + t * (qi - pi) for pi, qi in zip(p, q)))
    return out


def region(s, d):
    """Baricentrisko punktu apgabals, kuram metode piešķir sadalījumu s."""
    poly = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
    for q in range(3):
        if s[q] == 0:
            continue
        for p in range(3):
            if p == q:
                continue
            # v_q * d(s_p) - v_p * d(s_q - 1) >= 0
            w = [0.0, 0.0, 0.0]
            w[q] += d(s[p])
            w[p] -= d(s[q] - 1)
            poly = clip(poly, w)
            if not poly:
                return []
    return poly


def area(pts):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2)
                   in zip(pts, pts[1:] + pts[:1]))) / 2


def color(s):
    """Partiju krāsu sajaukums proporcionāli vietām, pabalināts."""
    rgb = [sum(s[i] * PARTY_RGB[i][k] for i in range(3)) / SEATS for k in range(3)]
    return "rgb(%d,%d,%d)" % tuple(round(255 - 0.30 * (255 - c)) for c in rgb)


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal"):
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s" stroke="#ffffff" '
            'stroke-width="3" stroke-linejoin="round" paint-order="stroke">'
            '%s</text>\n'
            % (x, y, FONT, size, fill, anchor, weight, s))


def label_pos(s, x, y):
    """Uzraksta vieta: ārpus trijstūra, ja punkts ir uz malas; citādi zem punkta."""
    k, m, n = s
    if s == (SEATS, 0, 0):
        return x, y - 12, "middle"
    if s == (0, SEATS, 0):
        return x - 8, y + 20, "middle"
    if s == (0, 0, SEATS):
        return x + 8, y + 20, "middle"
    if k == 0:                      # mala BC (apakšā)
        return x, y + 20, "middle"
    if n == 0:                      # mala AB (pa kreisi)
        return x - 10, y + 4, "end"
    if m == 0:                      # mala AC (pa labi)
        return x + 10, y + 4, "start"
    return x, y + 18, "middle"


def build(key, lang="lv"):
    titles, d = METHODS[key]
    title = titles[lang]
    allocs = [(k, m, SEATS - k - m) for k in range(SEATS, -1, -1)
              for m in range(SEATS - k, -1, -1)]
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'width="%d" height="%d" role="img" aria-label="%s">\n<title>%s: '
         '%s</title>\n'
         % (W, H, W, H, title, title, SUBTITLE[lang] % SEATS))
    s += '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n' % (W, H)

    for a in allocs:
        pts = [to_xy(v) for v in region(a, d)]
        if len(pts) < 3 or area(pts) < 1e-6:
            raise SystemExit("%s: sadalījumam %s nav apgabala" % (key, a))
        s += ('<polygon points="%s" fill="%s" stroke="#333" stroke-width="1.2" '
              'stroke-linejoin="round"/>\n'
              % (" ".join("%.2f,%.2f" % p for p in pts), color(a)))

    s += ('<polygon points="%s" fill="none" stroke="%s" stroke-width="2"/>\n'
          % (" ".join("%.2f,%.2f" % p for p in (VA, VB, VC)), INK))

    for a in allocs:
        x, y = to_xy(tuple(t / SEATS for t in a))
        s += '<circle cx="%.2f" cy="%.2f" r="4.5" fill="#333"/>\n' % (x, y)
        lx, ly, anchor = label_pos(a, x, y)
        s += txt(lx, ly, "%d:%d:%d" % a, 11.5, "#333", anchor)

    s += txt(VA[0], VA[1] - 30, "A", 15, INK, weight="bold")
    s += txt(VB[0] - 30, VB[1] + 6, "B", 15, INK, weight="bold")
    s += txt(VC[0] + 30, VC[1] + 6, "C", 15, INK, weight="bold")
    s += "</svg>\n"
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lang", choices=["lv", "en", "all"], default="all",
                    help="uzrakstu valoda (noklusēti abas)")
    langs = {"lv": ["lv"], "en": ["en"], "all": ["lv", "en"]}[ap.parse_args().lang]
    here = os.path.dirname(os.path.abspath(__file__))
    for key in METHODS:
        for lang in langs:
            out = os.path.join(here, key + (".en" if lang == "en" else "") + ".svg")
            with open(out, "w", encoding="utf-8", newline="\n") as f:
                f.write(build(key, lang))
            print("Wrote", out)


if __name__ == "__main__":
    main()
