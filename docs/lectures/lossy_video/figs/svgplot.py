# -*- coding: utf-8 -*-
"""Mazs SVG grafiku palīgmodulis audio attēliem (sampling.py, audio_bands.py,
masking.py, audio_examples.py).  Tas pats stils kā pārējiem lekcijas attēliem.
"""

import math

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
INK, BLUE, ORANGE, GREEN, RED, PURPLE, GRAY = (
    "#222", "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#9aa5b1")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal", rotate=None, raw=False):
    tr = ' transform="rotate(%g %g %g)"' % (rotate, x, y) if rotate is not None else ""
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s"%s>%s</text>\n'
            % (x, y, FONT, size, fill, anchor, weight, tr, s if raw else esc(s)))


def sub(s):
    return '<tspan baseline-shift="sub" font-size="75%%">%s</tspan>' % s


def head(W, H, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
            'role="img" aria-label="%s">\n<title>%s</title>\n'
            '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
            '<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
            'fill="#444"/></marker></defs>\n' % (W, H, W, H, esc(title), esc(title), W, H))


class Plot:
    """Taisnstūra grafiks ar lineāru vai logaritmisku x asi."""

    def __init__(self, x, y, w, h, xr, yr, xlog=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.xr, self.yr, self.xlog = xr, yr, xlog

    def X(self, v):
        a, b = self.xr
        if self.xlog:
            return self.x + self.w * (math.log10(v) - math.log10(a)) / (math.log10(b) - math.log10(a))
        return self.x + self.w * (v - a) / (b - a)

    def Y(self, v):
        a, b = self.yr
        return self.y + self.h - self.h * (v - a) / (b - a)

    def frame(self, xticks=(), yticks=(), xlabel="", ylabel="", grid=True):
        s = ""
        for v, lab in xticks:
            X = self.X(v)
            if grid:
                s += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e3e7ec" '
                      'stroke-width="1"/>\n' % (X, self.y, X, self.y + self.h))
            s += txt(X, self.y + self.h + 16, lab, 11, "#444")
        for v, lab in yticks:
            Y = self.Y(v)
            if grid:
                s += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e3e7ec" '
                      'stroke-width="1"/>\n' % (self.x, Y, self.x + self.w, Y))
            s += txt(self.x - 6, Y + 4, lab, 11, "#444", "end")
        s += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#5a6a7a" '
              'stroke-width="1.2"/>\n' % (self.x, self.y, self.w, self.h))
        if xlabel:
            s += txt(self.x + self.w / 2, self.y + self.h + 34, xlabel, 12, INK)
        if ylabel:
            s += txt(self.x - 44, self.y + self.h / 2, ylabel, 12, INK, rotate=-90)
        return s

    def line(self, xs, ys, col=BLUE, sw=2, dash=None, opacity=1.0, clip=True):
        pts = []
        for a, b in zip(xs, ys):
            X, Y = self.X(a), self.Y(b)
            if clip:
                Y = min(max(Y, self.y), self.y + self.h)
            pts.append("%.1f,%.1f" % (X, Y))
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="%g" '
                'stroke-linejoin="round" stroke-opacity="%g"%s/>\n' % (" ".join(pts), col, sw, opacity, d))

    def area(self, xs, ys, col, opacity=0.2):
        pts = ["%.1f,%.1f" % (self.X(xs[0]), self.y + self.h)]
        pts += ["%.1f,%.1f" % (self.X(a), min(max(self.Y(b), self.y), self.y + self.h)) for a, b in zip(xs, ys)]
        pts += ["%.1f,%.1f" % (self.X(xs[-1]), self.y + self.h)]
        return '<polygon points="%s" fill="%s" fill-opacity="%g" stroke="none"/>\n' % (" ".join(pts), col, opacity)

    def dot(self, xv, yv, col=RED, r=4):
        return '<circle cx="%.1f" cy="%.1f" r="%g" fill="%s"/>\n' % (self.X(xv), self.Y(yv), r, col)

    def vline(self, xv, y0, y1, col=RED, sw=3, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%g"%s/>\n'
                % (self.X(xv), self.Y(y0), self.X(xv), self.Y(y1), col, sw, d))


def save(path, svg):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("Wrote", path)
