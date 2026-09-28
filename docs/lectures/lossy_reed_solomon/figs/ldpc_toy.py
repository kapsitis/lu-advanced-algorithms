# -*- coding: utf-8 -*-
"""LDPC "spēļu piemērs": Tanera grafs, bitu pārslēgšana un min-sum atkodēšana.

Skripts
1. no retas pārbaudes matricas H izveido Tanera grafu (šķautņu sarakstu);
2. atkodē saņemto signālu ar bitu pārslēgšanas (bit-flipping) atkodētāju, kas
   redz tikai cietos lēmumus (0 vai 1);
3. atkodē to pašu signālu ar min-sum atkodētāju, kas izmanto mīksto
   informāciju (cik droši ir katrs saņemtais bits);
4. izdrukā abu atkodētāju gaitu un uzzīmē ldpc-tanner.svg un ldpc-decoding.svg.

Kods: H ir 6 x 12, katrā kolonnā divi vieninieki (katrs bits piedalās divās
pārbaudēs), katrā rindā četri.  Pārbaudes var uzskatīt par oktaedra
virsotnēm, bitus -- par tā šķautnēm; mazākais cikls oktaedrā ir trijstūris,
tāpēc koda minimālais attālums ir d = 3, un cietā atkodēšana garantēti izlabo
tikai 1 kļūdu (tāpat kā Heminga kods).  Dimensija k = 12 - rank(H) = 7.

Kanāls: bitu 0 sūta kā +1, bitu 1 -- kā -1; saņemtā vērtība r_j ir signāls ar
troksni.  Zīme rāda ticamāko bitu, |r_j| -- cik tas ir drošs.

    python ldpc_toy.py
"""

import itertools
import os

import numpy as np

H = np.array([
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1]])

CODEWORD = np.array([1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0])      # nosūtītais
RECEIVED = np.array([0.1, 0.8, 0.3, 1.3, 0.8, 0.9, 0.6, 1.1, -1.3, 1.4, 0.9, 1.2])


# --- 1. Tanera grafs ----------------------------------------------------------

def tanner_edges(H):
    """Šķautne (i, j) savieno pārbaudi i ar bitu j, ja H[i, j] = 1."""
    return [(i, j) for i in range(H.shape[0]) for j in range(H.shape[1]) if H[i, j]]


# --- 2. Bitu pārslēgšana (cietie lēmumi) --------------------------------------

def bit_flip(H, y, max_iter=10):
    """Kamēr kāda pārbaude nav apmierināta, pārslēdz bitus, kuri piedalās
    visvairāk neapmierinātās pārbaudēs.  Atgriež (rezultāts, vēsture)."""
    y = y.copy()
    history = []
    for _ in range(max_iter):
        syndrome = H @ y % 2
        unsatisfied = syndrome @ H        # katram bitam: neapmierināto pārbaužu skaits
        history.append((y.copy(), syndrome, unsatisfied))
        if not syndrome.any():
            break
        y[unsatisfied == unsatisfied.max()] ^= 1
    return y, history


# --- 3. Min-sum (mīkstā informācija) ------------------------------------------

def min_sum(H, L, max_iter=10):
    """Ziņojumu apmaiņa Tanera grafā.  L[j] > 0 nozīmē "drīzāk 0", L[j] < 0 --
    "drīzāk 1"; |L[j]| ir drošums.  Atgriež (rezultāts, aposterioro vērtību
    vēsture, pārbaužu ziņojumi 1. iterācijā)."""
    edges = tanner_edges(H)
    q = {e: L[e[1]] for e in edges}               # bits -> pārbaude
    history, first_msgs = [], None
    for _ in range(max_iter):
        r = {}                                    # pārbaude -> bits
        for (i, j) in edges:
            others = [q[(i, k)] for (i2, k) in edges if i2 == i and k != j]
            r[(i, j)] = np.prod(np.sign(others)) * min(abs(v) for v in others)
        if first_msgs is None:
            first_msgs = r
        post = np.array([L[j] + sum(r[(i, j)] for (i, j2) in edges if j2 == j)
                         for j in range(H.shape[1])])
        history.append(post)
        c = (post < 0).astype(int)
        if not (H @ c % 2).any():
            break
        for (i, j) in edges:
            q[(i, j)] = L[j] + sum(r[(k, j)] for (k, j2) in edges if j2 == j and k != i)
    return (history[-1] < 0).astype(int), history, first_msgs


def rank2(M):
    """Matricas rangs pēc moduļa 2 (Gausa izslēgšana)."""
    M = M.copy() % 2
    rank = 0
    for col in range(M.shape[1]):
        rows = [i for i in range(rank, M.shape[0]) if M[i, col]]
        if not rows:
            continue
        M[[rank, rows[0]]] = M[[rows[0], rank]]
        for i in range(M.shape[0]):
            if i != rank and M[i, col]:
                M[i] ^= M[rank]
        rank += 1
    return rank


# --- SVG zīmēšana -------------------------------------------------------------

FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"
INK, BLUE, ORANGE, GREEN, RED = "#222", "#4C78A8", "#F58518", "#54A24B", "#E45756"


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal"):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s">%s</text>\n'
            % (x, y, FONT, size, fill, anchor, weight, s))


def rect(x, y, w, h, fill, stroke="#9aa5b1", sw=1, rx=0):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
            'stroke="%s" stroke-width="%g"/>\n' % (x, y, w, h, rx, fill, stroke, sw))


def svg_head(W, H_, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'width="%d" height="%d" role="img" aria-label="%s">\n<title>%s</title>\n'
            '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n'
            % (W, H_, W, H_, title, title, W, H_))


def num(v):
    return ("%.1f" % v).replace("-", "−")


def tanner_svg():
    m, n = H.shape
    W, Ht = 900, 340
    s = svg_head(W, Ht, "LDPC koda pārbaudes matrica H un Tanera grafs")
    # matrica H
    cx0, cy0, cc = 20, 60, 20
    s += txt(cx0 + n * cc / 2, 36, "pārbaudes matrica H", 13, weight="bold")
    for i in range(m):
        s += txt(cx0 - 6, cy0 + i * cc + 14, "", 11)
        for j in range(n):
            s += rect(cx0 + j * cc, cy0 + i * cc, cc, cc,
                      "#dbe6f3" if H[i, j] else "#ffffff", "#c9d3de", 0.8)
            s += txt(cx0 + j * cc + cc / 2, cy0 + i * cc + 14, str(H[i, j]), 11,
                     INK if H[i, j] else "#b8c0c8", weight="bold" if H[i, j] else "normal")
    for j in range(n):
        s += txt(cx0 + j * cc + cc / 2, cy0 + m * cc + 16, str(j + 1), 10, "#555")
    for i in range(m):
        s += txt(cx0 + n * cc + 14, cy0 + i * cc + 14, "p%d" % (i + 1), 10.5, "#555")
    s += txt(cx0 + n * cc / 2, cy0 + m * cc + 34, "kolonnas — biti, rindas — pārbaudes", 11, "#555")
    s += txt(cx0 + n * cc / 2, cy0 + m * cc + 50, "katrā kolonnā 2 vieninieki, katrā rindā 4", 11, "#555")

    # Tanera grafs
    gx0, gx1 = 390, 880
    ycheck, ybit = 80, 270
    s += txt((gx0 + gx1) / 2, 36, "Tanera grafs", 13, weight="bold")
    xb = [gx0 + (gx1 - gx0) * (j + 0.5) / n for j in range(n)]
    xc = [gx0 + (gx1 - gx0) * (i + 0.5) / m for i in range(m)]
    for (i, j) in tanner_edges(H):
        s += ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.3" '
              'stroke-opacity="0.75"/>\n' % (xc[i], ycheck + 14, xb[j], ybit - 14, "#5a6a7a"))
    for i in range(m):
        s += rect(xc[i] - 15, ycheck - 15, 30, 30, "#fde5cc", ORANGE, 1.6, 3)
        s += txt(xc[i], ycheck + 4.5, "p%d" % (i + 1), 12, INK, weight="bold")
        s += txt(xc[i], ycheck - 22, "⊕ = 0", 10.5, "#555")
    for j in range(n):
        s += ('<circle cx="%g" cy="%g" r="14" fill="#dbe6f3" stroke="%s" '
              'stroke-width="1.6"/>\n' % (xb[j], ybit, BLUE))
        s += txt(xb[j], ybit + 4.5, str(j + 1), 12, INK, weight="bold")
    s += txt(gx0 - 6, ycheck + 4, "pārbaudes", 11, "#555", "end")
    s += txt(gx0 - 6, ybit + 4, "biti", 11, "#555", "end")
    s += txt((gx0 + gx1) / 2, ybit + 40,
             "šķautne savieno pārbaudi i ar bitu j, ja H[i, j] = 1;", 11, "#555")
    s += txt((gx0 + gx1) / 2, ybit + 56,
             "katras pārbaudes bitu summa pēc moduļa 2 ir 0", 11, "#555")
    s += "</svg>\n"
    return s


def decoding_svg(y, bf_hist, bf_result, ms_hist, ms_result):
    n = H.shape[1]
    lw, cw, rh = 300, 48, 38
    W = lw + n * cw + 20
    rows = [
        ("nosūtītais koda vārds c", "bits", CODEWORD),
        ("saņemtās vērtības r (0 → +1, 1 → −1)", "value", RECEIVED),
        ("cietais lēmums y (r < 0 → 1)", "bits", y),
        ("bitu pārslēgšana: neapmierinātās pārbaudes", "count", bf_hist[0][2]),
        ("bitu pārslēgšana: rezultāts", "bits", bf_result),
        ("min–sum: vērtības pēc 1. iterācijas", "value", ms_hist[-1]),
        ("min–sum: rezultāts", "bits", ms_result),
    ]
    Ht = 70 + len(rows) * rh + 60
    s = svg_head(W, Ht, "Cietā un mīkstā LDPC atkodēšana")
    s += txt(20, 28, "Divas kļūdas (1. un 3. bits) vienā koda vārdā: cietā un mīkstā atkodēšana",
             14, INK, "start", weight="bold")
    for j in range(n):
        s += txt(lw + j * cw + cw / 2, 56, str(j + 1), 11, "#555")
    for k, (label, kind, vals) in enumerate(rows):
        y0 = 64 + k * rh
        sep = k in (3, 5)
        if sep:
            s += ('<line x1="20" y1="%g" x2="%g" y2="%g" stroke="#c9d3de" '
                  'stroke-width="1"/>\n' % (y0 - 3, W - 20, y0 - 3))
        s += txt(20, y0 + rh / 2 + 4, label, 12, INK, "start")
        for j in range(n):
            x = lw + j * cw
            if kind == "bits":
                ok = vals[j] == CODEWORD[j]
                fill = "#dcecd8" if ok else "#fbdcdc"
                stroke = GREEN if ok else RED
                s += rect(x + 3, y0 + 3, cw - 6, rh - 8, fill, stroke, 1.4, 4)
                s += txt(x + cw / 2, y0 + rh / 2 + 4, str(int(vals[j])), 13, INK, weight="bold")
            elif kind == "value":
                v = float(vals[j])
                col = BLUE if v >= 0 else ORANGE
                bar = min(abs(v), 3.2) / 3.2 * (cw - 10)
                s += rect(x + 5, y0 + rh - 11, bar, 5, col, col, 0)
                s += txt(x + cw / 2, y0 + rh / 2 + 1, num(v), 12, col, weight="bold")
            else:
                v = int(vals[j])
                s += txt(x + cw / 2, y0 + rh / 2 + 4, str(v), 12,
                         RED if v == max(vals) else "#555", weight="bold" if v == max(vals) else "normal")
    yb = 64 + len(rows) * rh + 14
    s += rect(20, yb - 10, 14, 14, "#dcecd8", GREEN, 1.4, 3)
    s += txt(40, yb + 2, "bits sakrīt ar nosūtīto", 11, "#333", "start")
    s += rect(220, yb - 10, 14, 14, "#fbdcdc", RED, 1.4, 3)
    s += txt(240, yb + 2, "kļūda", 11, "#333", "start")
    s += txt(300, yb + 2, "zilā vērtība → drīzāk 0, oranžā → drīzāk 1; josla — drošums |r|",
             11, "#333", "start")
    s += txt(20, yb + 24, "Bitu pārslēgšana pārslēdz 9. bitu un iegūst derīgu, bet nepareizu koda vārdu 000000000000; "
             "min–sum redz, ka 1. un 3. bits ir nedroši, un atrod pareizo.", 11, "#333", "start")
    s += "</svg>\n"
    return s


def main():
    m, n = H.shape
    print("H: %d x %d, rank %d, k = %d" % (m, n, rank2(H), n - rank2(H)))
    words = [np.array(v) for v in itertools.product([0, 1], repeat=n)
             if not (H @ np.array(v) % 2).any()]
    print("koda vārdu skaits %d, minimālais attālums d = %d"
          % (len(words), min(int(w.sum()) for w in words if w.any())))
    print("Tanera grafa šķautnes (pārbaude, bits):",
          [(i + 1, j + 1) for i, j in tanner_edges(H)])
    assert not (H @ CODEWORD % 2).any()

    y = (RECEIVED < 0).astype(int)
    print("\nnosūtīts c =", CODEWORD)
    print("saņemts  r =", RECEIVED)
    print("cietais  y =", y, " kļūdas bitos", [int(j) + 1 for j in np.nonzero(y != CODEWORD)[0]])

    bf, bf_hist = bit_flip(H, y)
    print("\nBitu pārslēgšana:")
    for t, (yy, syn, uns) in enumerate(bf_hist):
        print("  solis %d: y = %s, sindroms = %s, neapmierināto pārbaužu skaits = %s"
              % (t, yy, syn, uns))
    print("  rezultāts", bf, "pareizs" if (bf == CODEWORD).all() else "NEPAREIZS")

    ms, ms_hist, msgs = min_sum(H, RECEIVED)
    print("\nMin-sum:")
    for i in range(m):
        print("  pārbaude p%d sūta: %s" % (i + 1, {j + 1: round(float(v), 2)
                                                 for (i2, j), v in msgs.items() if i2 == i}))
    for t, post in enumerate(ms_hist):
        print("  pēc %d. iterācijas L = %s -> %s" % (t + 1, np.round(post, 2), (post < 0).astype(int)))
    print("  rezultāts", ms, "pareizs" if (ms == CODEWORD).all() else "NEPAREIZS")

    best = max(words, key=lambda w: RECEIVED @ (1 - 2 * w))
    print("\nMaksimālās ticamības (ML) koda vārds:", best,
          "(korelācija %.1f; nulles vārdam %.1f)"
          % (RECEIVED @ (1 - 2 * best), RECEIVED.sum()))

    here = os.path.dirname(os.path.abspath(__file__))
    for name, content in [("ldpc-tanner.svg", tanner_svg()),
                          ("ldpc-decoding.svg", decoding_svg(y, bf_hist, bf, ms_hist, ms))]:
        with open(os.path.join(here, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print("Wrote", name)


if __name__ == "__main__":
    main()
