# -*- coding: utf-8 -*-
"""Kopīgas SVG zīmēšanas palīgfunkcijas ANS nodaļas attēliem.

Šo moduli neizsauc tieši -- to importē skripti, kuru nosaukumi sakrīt ar
ģenerējamo SVG failu nosaukumiem:

    ans-slots.py      ->  ans-slots.svg
    ans-encode.py     ->  ans-encode.svg
    ans-decode.py     ->  ans-decode.svg
    ans-renorm.py     ->  ans-renorm.svg
    zstd-pipeline.py  ->  zstd-pipeline.svg

Prasības: tikai Python 3 standarta bibliotēka.
"""

import argparse
import os
import sys

# Windows konsolē noklusētais kodējums mēdz būt cp1252, kurā nav garumzīmju.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError, OSError):
        pass

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Consolas, Menlo, monospace"

# (aizpildījums, kontūra, teksts) -- ciklē pa alfabēta simboliem
PALETTE = [
    ("#dbe6f3", "#4C78A8", "#1f3a5f"),   # zils
    ("#fde5cc", "#F58518", "#7a3d00"),   # oranžs
    ("#dcecd8", "#54A24B", "#234d1c"),   # zaļš
    ("#ecdcea", "#B279A2", "#4f2a48"),   # violets
    ("#e8e2dc", "#9C755F", "#4a382c"),   # brūns
    ("#d9eeee", "#4CA3A3", "#134d4d"),   # tirkīzs
    ("#f5dede", "#B23B3B", "#6b1616"),   # sarkans
    ("#ece7d3", "#9C9C3B", "#4d4d12"),   # olīvzaļš
]

DEFAULT_FREQ = "A:3,C:1,G:3,U:2,$:1"
DEFAULT_MESSAGE = "GACGU$"


# --------------------------------------------------------------- modelis
class Alphabet(object):
    """Alfabēts ar kvantētām frekvencēm f(s) un kumulatīvām summām c(s)."""

    def __init__(self, spec):
        self.symbols, self.freq = [], {}
        for part in spec.split(","):
            name, _, count = part.partition(":")
            name = name.strip()
            if not name:
                raise ValueError("tukšs simbols specifikācijā: %r" % spec)
            self.symbols.append(name)
            self.freq[name] = int(count)
        self.M = sum(self.freq.values())
        self.cum, acc = {}, 0
        for s in self.symbols:
            self.cum[s] = acc
            acc += self.freq[s]
        self.color = {s: PALETTE[i % len(PALETTE)]
                      for i, s in enumerate(self.symbols)}

    def owner(self, r):
        """Simbols, kuram pieder sprauga ar atlikumu r."""
        for s in self.symbols:
            if self.cum[s] <= r < self.cum[s] + self.freq[s]:
                return s
        raise ValueError("sprauga %d neietilpst diapazonā [0;%d)" % (r, self.M))

    def rank(self, y):
        """y kārtas numurs sava īpašnieka apakšvirknē."""
        s = self.owner(y % self.M)
        return s, self.freq[s] * (y // self.M) + (y % self.M) - self.cum[s]

    def C(self, s, x):
        """Kodēšanas solis: x-tā sprauga, kas pieder simbolam s."""
        f, c = self.freq[s], self.cum[s]
        return self.M * (x // f) + (x % f) + c

    def D(self, x):
        """Atkodēšanas solis: (simbols, jaunais stāvoklis)."""
        r = x % self.M
        s = self.owner(r)
        return s, self.freq[s] * (x // self.M) + r - self.cum[s]

    def split(self, message):
        """Sadala ziņojumu simbolos (pa burtiem vai pa komatiem)."""
        if "," in message:
            return [p.strip() for p in message.split(",") if p.strip()]
        if all(len(s) == 1 for s in self.symbols):
            return list(message)
        raise ValueError("daudzburtu alfabētam ziņojumu atdaliet ar komatiem")

    def encode(self, message, x0=0):
        """Visu stāvokļu virkne, sākot ar x0. Ziņojumu apstrādā atpakaļgaitā."""
        chain, x = [x0], x0
        for s in reversed(self.split(message)):
            x = self.C(s, x)
            chain.append(x)
        return chain


# ------------------------------------------------------------ SVG primitīvi
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(w, h, title):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="%d" height="%d" role="img" aria-label="%s">\n'
        '<title>%s</title>\n'
        '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
        '<defs>\n'
        '  <marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">\n'
        '    <path d="M 0 0 L 10 5 L 0 10 z" fill="#444"/>\n'
        '  </marker>\n'
        '</defs>\n' % (w, h, w, h, esc(title), esc(title), w, h)
    )


def txt(x, y, s, size=13, fill="#222", anchor="middle", weight="normal",
        family=FONT, pre=False):
    sp = ' xml:space="preserve"' if pre else ""
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" '
            'text-anchor="%s" font-weight="%s"%s>%s</text>\n'
            % (x, y, family, size, fill, anchor, weight, sp, esc(s)))


def rect(x, y, w, h, fill, stroke, rx=4, sw=1.4):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"/>\n'
            % (x, y, w, h, rx, fill, stroke, sw))


def arrow(x1, y1, x2, y2, stroke="#444", sw=1.6):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
            'stroke-width="%s" marker-end="url(#arw)"/>\n'
            % (x1, y1, x2, y2, stroke, sw))


def mono_width(text, size):
    """Aptuvens monospace teksta platums pikseļos."""
    return 0.62 * size * len(text)


# ----------------------------------------------------------------- CLI
def default_out(script_file):
    """Blakus skriptam esošs .svg fails ar to pašu nosaukumu."""
    return os.path.splitext(os.path.abspath(script_file))[0] + ".svg"


def parser(script_file, description, freq=False, message=False):
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("-o", "--out", default=default_out(script_file),
                    help="izvades SVG fails (noklusēti: blakus skriptam)")
    if freq:
        ap.add_argument("-f", "--freq", default=DEFAULT_FREQ,
                        help='frekvences, piem. "A:3,C:1,G:3,U:2,$:1"')
    if message:
        ap.add_argument("-m", "--message", default=DEFAULT_MESSAGE,
                        help='kodējamais ziņojums, piem. "GACGU$"')
    return ap


def write(path, body):
    with open(path, "w", encoding="utf-8") as f:
        f.write(body + "</svg>\n")
    print("uzrakstīts %s (%d baiti)" % (path, os.path.getsize(path)))
