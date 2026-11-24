# -*- coding: utf-8 -*-
"""Ģenerē levenstein-distance.svg -- Levenšteina attāluma matricu diviem vārdiem.

Rindas atbilst vārda A burtiem, kolonnas -- vārda B burtiem; pirmā rinda un
pirmā kolonna (ar "-") atbilst tukšajam prefiksam. Šūnā (i, j) ir Levenšteina
attālums M[i, j] starp A[0..i-1] un B[0..j-1]. Ar sarkanu iekrāsots viens
optimālais labojumu ceļš no M[0, 0] līdz M[m, n].

Attēlā nav uzrakstu nevienā valodā (tikai burti un skaitļi), tāpēc to pašu
failu var lietot gan latviskajā, gan angliskajā lekcijas versijā.

    python levenstein-distance.py                    # A = tcat, B = atcaca
    python levenstein-distance.py kitten sitting -o kitten.svg
"""

import argparse
import os

FONT = "DejaVu Sans Mono, Consolas, Menlo, Courier New, monospace"
INK, RED = "#222", "#E00000"
HEAD_FILL, GRID = "#A8DCDC", "#555"
CELL = 36                              # šūnas izmērs pikseļos
PAD = 2                                # mala ap tabulu


def levenshtein_matrix(a, b):
    """Atgriež (m+1) x (n+1) matricu M ar Levenšteina attālumiem starp prefiksiem."""
    m, n = len(a), len(b)
    M = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        M[i][0] = i
    for j in range(n + 1):
        M[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                M[i][j] = M[i - 1][j - 1]
            else:
                M[i][j] = 1 + min(M[i - 1][j], M[i][j - 1], M[i - 1][j - 1])
    return M


def optimal_path(a, b, M):
    """Atjauno vienu optimālo ceļu no (m, n) uz (0, 0); atgriež šūnu kopu.

    Ja ir vairākas iespējas, priekšroku dod (1) sakrītošam burtam pa diagonāli,
    (2) burta iespraušanai (no kreisās), (3) aizstāšanai pa diagonāli,
    (4) burta dzēšanai (no augšas).
    """
    i, j = len(a), len(b)
    path = {(i, j)}
    while (i, j) != (0, 0):
        if i > 0 and j > 0 and a[i - 1] == b[j - 1] and M[i][j] == M[i - 1][j - 1]:
            i, j = i - 1, j - 1
        elif j > 0 and M[i][j] == M[i][j - 1] + 1:
            j -= 1
        elif i > 0 and j > 0 and M[i][j] == M[i - 1][j - 1] + 1:
            i, j = i - 1, j - 1
        else:
            i -= 1
        path.add((i, j))
    return path


def text(x, y, s, fill=INK, size=20):
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="middle" dominant-baseline="central">%s</text>\n'
            % (x, y, FONT, size, fill, s))


def rect(x, y, w, h, fill):
    return ('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" '
            'stroke="%s" stroke-width="1"/>\n' % (x, y, w, h, fill, GRID))


def make_svg(a, b):
    M = levenshtein_matrix(a, b)
    path = optimal_path(a, b, M)
    rows, cols = len(a) + 2, len(b) + 2      # + virsraksta rinda/kolonna un "-"
    width, height = cols * CELL + 2 * PAD, rows * CELL + 2 * PAD
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
           'viewBox="0 0 %d %d">\n' % (width, height, width, height),
           '<rect width="100%" height="100%" fill="#FFFFFF"/>\n']
    col_labels = ["", "−"] + list(b)     # "−" -- mīnusa zīme (tukšais prefikss)
    row_labels = ["−"] + list(a)
    for c in range(cols):
        for r in range(rows):
            x, y = PAD + c * CELL, PAD + r * CELL
            cx, cy = x + CELL / 2, y + CELL / 2
            if r == 0 or c == 0:              # virsraksta šūnas
                out.append(rect(x, y, CELL, CELL, HEAD_FILL))
                label = col_labels[c] if r == 0 else row_labels[r - 1]
                if label:
                    out.append(text(cx, cy, label))
            else:
                i, j = r - 1, c - 1
                out.append(rect(x, y, CELL, CELL, "#FFFFFF"))
                out.append(text(cx, cy, M[i][j], RED if (i, j) in path else INK))
    out.append("</svg>\n")
    return "".join(out), M[len(a)][len(b)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("a", nargs="?", default="tcat", help="vārds A (rindas), noklusēti: tcat")
    ap.add_argument("b", nargs="?", default="atcaca", help="vārds B (kolonnas), noklusēti: atcaca")
    ap.add_argument("-o", "--output", default=None,
                    help="izvades fails (noklusēti: levenstein-distance.svg blakus skriptam)")
    args = ap.parse_args()
    out = args.output or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "levenstein-distance.svg")
    svg, dist = make_svg(args.a, args.b)
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print("M(%s, %s) = %d -> %s" % (args.a, args.b, dist, out))


if __name__ == "__main__":
    main()
