# -*- coding: utf-8 -*-
"""H.264 (un MPEG) freimu sūtīšanas un atskaņošanas secība ar B-freimiem.

No atskaņošanas secības parauga (piemēram, "IBBPBBPBBI") aprēķina, kādā
secībā freimi jānosūta: B-freimu prognozē gan no iepriekšējā, gan no nākamā
enkurfreima (I vai P), tāpēc nākamais enkurfreims jānosūta (un jāatkodē)
PIRMS B-freimiem, kas atskaņošanas secībā ir pirms tā.

Skripts izdrukā tabulu un uzzīmē h264-frame-order.svg:
augšā -- sūtīšanas (dekodēšanas) secība, apakšā -- atskaņošanas secība,
bultiņas rāda, kur katrs freims nonāk atskaņošanas brīdī; loki zem apakšējās
rindas rāda, no kuriem freimiem katrs P un B freims tiek prognozēts.
Apzīmējumā I_0, B_1, ... apakšindekss ir freima numurs atskaņošanas secībā.

    python h264_frame_order.py [PARAUGS]      (noklusējums: IBBPBBPBBI)
"""

import os
import sys

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
INK, BLUE, ORANGE, GREEN = "#222", "#4C78A8", "#F58518", "#54A24B"
STYLE = {"I": ("#dcecd8", GREEN), "P": ("#dbe6f3", BLUE), "B": ("#fde5cc", ORANGE)}


def coding_order(pattern):
    """Atskaņošanas indeksi sūtīšanas secībā."""
    order, pending_b = [], []
    for i, t in enumerate(pattern):
        if t == "B":
            pending_b.append(i)          # gaida nākamo enkurfreimu
        else:
            order.append(i)              # enkurfreims (I vai P) iet pirmais
            order.extend(pending_b)      # tad B-freimi, kas stāv pirms tā
            pending_b = []
    order.extend(pending_b)              # (ja virkne beidzas ar B)
    return order


def references(pattern):
    """Katram freimam -- atskaņošanas indeksi, no kuriem to prognozē."""
    anchors = [i for i, t in enumerate(pattern) if t != "B"]
    refs = {}
    for i, t in enumerate(pattern):
        if t == "P":
            refs[i] = [max(a for a in anchors if a < i)]
        elif t == "B":
            prev = [a for a in anchors if a < i]
            nxt = [a for a in anchors if a > i]
            refs[i] = ([prev[-1]] if prev else []) + ([nxt[0]] if nxt else [])
        else:
            refs[i] = []
    return refs


def label(x, y, t, idx, size=15):
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" text-anchor="middle" '
            'font-weight="bold">%s<tspan baseline-shift="sub" font-size="70%%">%d</tspan></text>\n'
            % (x, y, FONT, size, INK, t, idx))


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal"):
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" text-anchor="%s" '
            'font-weight="%s">%s</text>\n' % (x, y, FONT, size, fill, anchor, weight, s))


def build(pattern):
    order = coding_order(pattern)
    refs = references(pattern)
    n = len(pattern)
    step, bw = 70, 50
    x0 = 190
    ytop, ybot = 60, 210
    W, H = x0 + n * step + 20, 420
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img" aria-label="H.264 freimu secība">\n<title>H.264 freimu sūtīšanas un '
         'atskaņošanas secība</title>\n<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
         '<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
         'markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
         'fill="#777"/></marker></defs>\n' % (W, H, W, H, W, H))
    s += txt(20, ytop + 20, "sūtīšanas", 13, INK, "start", "bold")
    s += txt(20, ytop + 36, "(dekodēšanas) secība", 13, INK, "start", "bold")
    s += txt(20, ybot + 20, "atskaņošanas", 13, INK, "start", "bold")
    s += txt(20, ybot + 36, "secība", 13, INK, "start", "bold")

    def box(x, y, i):
        fill, stroke = STYLE[pattern[i]]
        return ('<rect x="%g" y="%g" width="%g" height="%g" rx="6" fill="%s" stroke="%s" '
                'stroke-width="1.8"/>\n' % (x, y, bw, bw, fill, stroke)) + label(x + bw / 2, y + 31, pattern[i], i)

    for pos, i in enumerate(order):
        x = x0 + pos * step
        s += txt(x + bw / 2, ytop - 10, str(pos), 11, "#777")
        s += box(x, ytop, i)
        xb = x0 + i * step
        s += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#777" stroke-width="1.4" '
              'marker-end="url(#arw)"/>\n' % (x + bw / 2, ytop + bw + 2, xb + bw / 2, ybot - 4))
    for i in range(n):
        x = x0 + i * step
        s += box(x, ybot, i)
        s += txt(x + bw / 2, ybot + bw + 16, str(i), 11, "#777")

    # atsauču loki zem atskaņošanas rindas
    for i, rs in refs.items():
        for r in rs:
            side = 1 if r < i else -1          # atsauce pa kreisi (+1) vai pa labi (-1)
            xa = x0 + r * step + bw / 2 + 10 * side
            xb = x0 + i * step + bw / 2 - 10 * side
            depth = 10 + 16 * abs(i - r)
            y = ybot + bw + 24
            col = ORANGE if pattern[i] == "B" else BLUE
            s += ('<path d="M %g %g Q %g %g %g %g" stroke="%s" stroke-width="1.3" fill="none" '
                  'stroke-opacity="0.8" marker-end="url(#arw)"/>\n'
                  % (xa, y, (xa + xb) / 2, y + depth, xb, y, col))
    s += txt(20, H - 34, "Loki: no kura freima prognozē (zilie — P-freimi no iepriekšējā enkurfreima, "
             "oranžie — B-freimi no abiem blakus enkurfreimiem).", 11.5, "#333", "start")
    s += txt(20, H - 16, "Apakšindekss ir freima numurs atskaņošanas secībā; pelēkie skaitļi augšā — "
             "numurs sūtīšanas secībā.", 11.5, "#333", "start")
    s += "</svg>\n"
    return s, order


def main():
    pattern = sys.argv[1] if len(sys.argv) > 1 else "IBBPBBPBBI"
    assert set(pattern) <= set("IPB") and pattern[0] == "I", "paraugam jāsākas ar I un jāsatur tikai I, P, B"
    svg, order = build(pattern)
    names = ["%s%d" % (pattern[i], i) for i in range(len(pattern))]
    print("atskaņošanas secība:", " ".join(names))
    print("sūtīšanas secība:   ", " ".join(names[i] for i in order))
    print("sūtīšanas numurs katram atskaņošanas freimam:",
          " ".join(str(order.index(i)) for i in range(len(pattern))))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h264-frame-order.svg")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("Wrote", out)


if __name__ == "__main__":
    main()
