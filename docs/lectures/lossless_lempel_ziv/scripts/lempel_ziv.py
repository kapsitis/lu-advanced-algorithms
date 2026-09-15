# -*- coding: utf-8 -*-
"""LZ77 un LZ78 algoritmi -- Python versijas pseidokodam no ../index.md.

Kods apzināti seko pseidokodam rindiņu pa rindiņai (komentāros ir pseidokoda
rindiņu numuri), tāpēc tas nav ne ātrs, ne "pitonisks". Pseidokodā masīvi
numurēti no 1; to panākam, masīva sākumā ievietojot neizmantotu elementu None.

Kodējumus var pierakstīt tāpat kā ../index.md:
    LZ77 trijnieki:  "(0,0,a),(0,0,b),(0,0,c),(3,6,d),(4,2,c)"
    LZ78 kodi:       "a,b,c,1,3,2,d,4,1,a"  vai  "A.B.C.1.3.2.D.4.1.A"
(LZ78 pierakstā alfabētā nedrīkst būt cipari, punkts vai komats.)

Piemēri:
    python lempel_ziv.py
    python -m pytest test_lempel_ziv.py
"""

import math
import re
import sys


# ------------------------------------------------------------------- LZ77

def lz77_encode(T, W, L=math.inf):
    """LZ77-Encode(T, n, W, L): atgriež trijnieku (d, ell, x) sarakstu.

    T -- ievades virkne; W -- loga garums; L -- priekšskata bufera garums
    (pēc noklusējuma nav ierobežots).
    """
    n = len(T)
    T = [None] + list(T)                                   # T[1:n]
    C = []
    i = 1                                                  # 1
    while i <= n:                                          # 2
        d, ell = 0, 0                                      # 3
        for s in range(i - 1, max(1, i - W) - 1, -1):      # 4  (downto)
            k = 0                                          # 5
            while k < min(L, n - i) and T[s + k] == T[i + k]:  # 6
                k = k + 1                                  # 7
            if k > ell:                                    # 8
                d, ell = i - s, k
        C.append((d, ell, T[i + ell]))                     # 9  Output(d, ell, T[i + ell])
        i = i + ell + 1                                    # 10
    return C


def lz77_decode(C):
    """LZ77-Decode(C): atjauno virkni no trijnieku (d, ell, x) saraksta."""
    T = [None]                                             # T[1:m], sākumā m = 0
    m = 0                                                  # 1
    for d, ell, x in C:                                    # 2
        for k in range(1, ell + 1):                        # 3
            if not 1 <= m + k - d < m + k:                 # (pseidokodā nav: nekorekta ievade)
                raise ValueError("nobīde %d norāda ārpus atkodētās daļas" % d)
            T.append(T[m + k - d])                         # 4  T[m + k] = T[m + k - d]
        m = m + ell + 1                                    # 5
        T.append(x)                                        # 6  T[m] = x
    return "".join(T[1:m + 1])                             # 7


_LZ77_TRIPLE = re.compile(r"\((\d+),(\d+),(.)\)", re.S)


def lz77_format(C):
    """[(0, 0, 'a'), (3, 6, 'd')] -> "(0,0,a),(3,6,d)"."""
    return ",".join("(%d,%d,%s)" % triple for triple in C)


def lz77_parse(s):
    """"(0,0,a),(3,6,d)" -> [(0, 0, 'a'), (3, 6, 'd')]."""
    C = [(int(d), int(ell), x) for d, ell, x in _LZ77_TRIPLE.findall(s)]
    if lz77_format(C) != s:
        raise ValueError("nekorekts LZ77 trijnieku pieraksts: %r" % s)
    return C


# ------------------------------------------------------------------- LZ78

def lz78_encode(T, S):
    """LZ78-Encode(T, n): atgriež kodu sarakstu -- burtus (str) un frāžu numurus (int).

    S -- alfabēts (piemēram, "abcd"); vārdnīcā D sākumā ir visi tā burti.
    Vārdnīca D katrai frāzei w glabā tās kodu D[w].
    """
    n = len(T)
    if not set(T) <= set(S):
        raise ValueError("ievadē ir burti, kas nav alfabētā %r" % S)
    if n == 0:                                             # pseidokodā pieņemts n >= 1
        return []
    T = [None] + list(T)                                   # T[1:n]
    C = []
    D = {x: x for x in S}                                  # 1  New-Dictionary(S)
    m = 0                                                  # 2
    w = T[1]                                               # 3
    for i in range(2, n + 1):                              # 4
        k = T[i]                                           # 5
        if w + k in D:                                     # 6
            w = w + k                                      # 7
        else:                                              # 8
            C.append(D[w])                                 # 9  Output(D[w])
            m = m + 1                                      # 10
            D[w + k] = m                                   # 11
            w = k                                          # 12
    C.append(D[w])                                         # 13 Output(D[w])
    return C


def lz78_decode(C, S):
    """LZ78-Decode(c_1 c_2 ... c_r): atjauno virkni no kodu saraksta.

    S -- alfabēts; vārdnīca D katram kodam c glabā frāzi D[c].
    """
    if not C:                                              # pseidokodā pieņemts r >= 1
        return ""
    out = []
    D = {x: x for x in S}                                  # 1  New-Dictionary(S)
    m = 0                                                  # 2
    w = D[C[0]]                                            # 3  w = D[c_1]
    out.append(w)                                          # 4  Output(w)
    for c in C[1:]:                                        # 5  for j = 2 to r
        if c in D:                                         # 6
            v = D[c]                                       # 7
        else:                                              # 8
            if c != m + 1:                                 # (pseidokodā nav: nekorekta ievade)
                raise ValueError("kods %r nav vārdnīcā" % (c,))
            v = w + w[0]                                   # 9  v = w w[1] (Python numurē no 0)
        out.append(v)                                      # 10 Output(v)
        m = m + 1                                          # 11
        D[m] = w + v[0]                                    # 12 D[m] = w v[1]
        w = v                                              # 13
    return "".join(out)


def lz78_format(C, sep=","):
    """['a', 'b', 1, 3] -> "a,b,1,3"."""
    return sep.join(str(c) for c in C)


def lz78_parse(s):
    """"a,b,1,3" vai "A.B.1.3" -> ['a', 'b', 1, 3]."""
    if s == "":
        return []
    C = []
    for token in re.split(r"[.,]", s):
        if re.fullmatch(r"[0-9]+", token):
            C.append(int(token))
        elif len(token) == 1:
            C.append(token)
        else:
            raise ValueError("nekorekts LZ78 kods %r virknē %r" % (token, s))
    return C


# ---------------------------------------------------------------- piemēri

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")               # Windows konsolē citādi garumzīmes nevar izdrukāt
    text = "abcabcabcdabc"
    C = lz77_encode(text, 6)
    print("LZ77, W = 6 (3.1. uzdevums)")
    print("  %s -> %s -> %s" % (text, lz77_format(C), lz77_decode(C)))

    text = "abcabcabcdabcaba"
    C = lz78_encode(text, "abcd")
    print("LZ78 (piemērs)")
    print("  %s -> %s -> %s" % (text, lz78_format(C), lz78_decode(C, "abcd")))

    print("LZ78 atkodēšana (3.2.-3.4. uzdevums)")
    for codes, S in [("A.B.C.1.3.2.D.4.1.A", "ABCD"),
                     ("a,a,b,1,2,4,2", "ab"),
                     ("a,b,a,3,4", "ab")]:
        print("  %s -> %s" % (codes, lz78_decode(lz78_parse(codes), S)))
