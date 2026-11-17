# -*- coding: utf-8 -*-
"""Šofa (Schoof) algoritms līknes punktu skaitam (mācību versija, mazam p).

Līkne E: y^2 = f(x) = x^3 + ax + b virs F_p. Atrod Frobeniusa pēdu t (#E = p + 1 - t),
aprēķinot t mod l maziem pirmskaitļiem l un saliekot ar Ķīniešu atlikumu teorēmu.

Polinomus glabā kā koeficientu sarakstus [c0, c1, c2, ...] (c0 + c1 x + c2 x^2 + ...).
Punkts no E[l] ir formā (A(x), B(x) * y), kur A, B ir polinomi pēc moduļa h(x) | psi_l(x);
bezgalīgi tālo punktu O attēlo ar None. Nav optimizēts -- tikai mācībām!

    python schoof.py      # izdrukā 12.7. uzdevuma soļus līknei y^2 = x^3 + x + 4 virs F_23
"""

from math import isqrt

O = None


# ---------- polinomi virs F_p ----------

def trim(f):
    while f and f[-1] == 0:
        f.pop()
    return f


def padd(f, g, p):
    n = max(len(f), len(g))
    return trim([((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0)) % p for i in range(n)])


def pneg(f, p):
    return [(-c) % p for c in f]


def psub(f, g, p):
    return padd(f, pneg(g, p), p)


def pmul(f, g, p):
    if not f or not g:
        return []
    r = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            r[i + j] = (r[i + j] + a * b) % p
    return trim(r)


def pdivmod(f, g, p):
    """Dalīšana ar atlikumu: f = q*g + r, deg r < deg g."""
    f = f[:]
    inv = pow(g[-1], -1, p)
    q = [0] * max(len(f) - len(g) + 1, 0)
    while len(f) >= len(g) and f:
        c = f[-1] * inv % p
        d = len(f) - len(g)
        q[d] = c
        for i, b in enumerate(g):
            f[i + d] = (f[i + d] - c * b) % p
        trim(f)
    return trim(q), f


def pmod(f, g, p):
    return pdivmod(f, g, p)[1]


def pgcd(f, g, p):
    while g:
        f, g = g, pmod(f, g, p)
    inv = pow(f[-1], -1, p)
    return [c * inv % p for c in f]          # normēts (vecākais koeficients 1)


def ppow(f, e, h, p):
    """f^e mod h (ātrā kāpināšana)."""
    r, f = [1], pmod(f, h, p)
    while e:
        if e & 1:
            r = pmod(pmul(r, f, p), h, p)
        f = pmod(pmul(f, f, p), h, p)
        e >>= 1
    return r


def pcompose(f, g, h, p):
    """f(g(x)) mod h (Hornera shēma)."""
    r = []
    for c in reversed(f):
        r = pmod(padd(pmul(r, g, p), [c], p), h, p)
    return r


class NotInvertible(Exception):
    """Dalītājs nav apgriežams pēc moduļa h: atrasts netriviāls h dalītājs g."""
    def __init__(self, g):
        self.g = g


def pinv(f, h, p):
    """f^{-1} mod h ar paplašināto Eiklīda algoritmu."""
    r0, r1, s0, s1 = h[:], pmod(f, h, p), [], [1]
    while r1:
        q, r = pdivmod(r0, r1, p)
        r0, r1, s0, s1 = r1, r, s1, psub(s0, pmul(q, s1, p), p)
    if len(r0) != 1:
        raise NotInvertible([c * pow(r0[-1], -1, p) % p for c in r0])   # gcd(f, h) != 1
    return pmod([c * pow(r0[0], -1, p) % p for c in s0], h, p)


def show(f, var="x"):
    if not f:
        return "0"
    terms = []
    for i in range(len(f) - 1, -1, -1):
        c = f[i]
        if c == 0:
            continue
        mono = "" if i == 0 else (var if i == 1 else f"{var}^{i}")
        terms.append(str(c) if not mono else (mono if c == 1 else f"{c}{mono}"))
    return " + ".join(terms)


# ---------- dalīšanas polinomi ----------

def division_polynomials(a, b, p, n_max):
    """Dalīšanas polinomi psi_n. Nepāra n glabā psi_n(x); pāra n glabā g_n(x), kur psi_n = y * g_n.

    psi_0 = 0, psi_1 = 1, psi_2 = 2y, psi_3 = 3x^4 + 6ax^2 + 12bx - a^2,
    psi_4 = 4y (x^6 + 5ax^4 + 20bx^3 - 5a^2x^2 - 4abx - 8b^2 - a^3),
    psi_{2m+1} = psi_{m+2} psi_m^3 - psi_{m-1} psi_{m+1}^3,
    psi_{2m}   = psi_m / (2y) * (psi_{m+2} psi_{m-1}^2 - psi_{m-2} psi_{m+1}^2),
    kur y^2 aizstāj ar f(x) = x^3 + ax + b.
    """
    F = [b % p, a % p, 0, 1]
    F2 = pmul(F, F, p)
    half = pow(2, -1, p)
    psi = {0: [], 1: [1], 2: [2],
           3: trim([(-a * a) % p, 12 * b % p, 6 * a % p, 0, 3]),
           4: trim([4 * c % p for c in [-8 * b * b - a ** 3, -4 * a * b, -5 * a * a, 20 * b, 5 * a, 0, 1]])}
    for n in range(5, n_max + 1):
        m = n // 2
        P = psi
        cube = lambda f: pmul(f, pmul(f, f, p), p)
        sq = lambda f: pmul(f, f, p)
        if n % 2 == 1:                       # n = 2m + 1; pāra indeksu reizinājumā y^4 = f^2
            t1 = pmul(P[m + 2], cube(P[m]), p)
            t2 = pmul(P[m - 1], cube(P[m + 1]), p)
            if m % 2 == 0:
                t1 = pmul(t1, F2, p)
            else:
                t2 = pmul(t2, F2, p)
            psi[n] = psub(t1, t2, p)
        else:                                # n = 2m
            t = psub(pmul(P[m + 2], sq(P[m - 1]), p), pmul(P[m - 2], sq(P[m + 1]), p), p)
            psi[n] = [c * half % p for c in pmul(P[m], t, p)]
    return psi


# ---------- punkti formā (A(x), B(x) y) pēc moduļa h ----------

def add(P, Q, F, a, h, p):
    if P is O:
        return Q
    if Q is O:
        return P
    (a1, b1), (a2, b2) = [(pmod(A, h, p), pmod(B, h, p)) for (A, B) in (P, Q)]
    if a1 == a2:                                               # vienādas x koordinātes
        if padd(b1, b2, p) == []:
            return O                                           # P + (-P) = O
        if b1 != b2:                                           # sakrīt tikai daļā punktu
            raise NotInvertible(pgcd(psub(b1, b2, p), h, p))
        num = padd([c * 3 % p for c in pmul(a1, a1, p)], [a % p], p)
        den = pmul([2], pmul(b1, F, p), p)                     # dubultošana: 1/(2y) = y/(2f)
    else:
        num, den = psub(b2, b1, p), psub(a2, a1, p)
    mu = pmod(pmul(num, pinv(den, h, p), p), h, p)             # lambda = mu(x) * y
    lam2 = pmod(pmul(F, pmul(mu, mu, p), p), h, p)             # lambda^2 = mu^2 f(x)
    a3 = psub(psub(lam2, a1, p), a2, p)
    b3 = pmod(psub(pmul(mu, psub(a1, a3, p), p), b1, p), h, p)
    return (pmod(a3, h, p), b3)


def mul(k, P, F, a, h, p):
    R = O
    for _ in range(k):
        R = add(R, P, F, a, h, p)
    return R


# ---------- Šofa algoritms ----------

def trace_mod_2(F, p):
    """t pāra <=> f(x) ir sakne F_p <=> gcd(x^p - x, f) != 1."""
    xp = ppow([0, 1], p, F, p)
    g = pgcd(F, psub(xp, [0, 1], p), p)
    print(f"  x^{p} mod f = {show(xp)};  gcd(x^{p} - x, f) = {show(g)}")
    return 0 if len(g) > 1 else 1


def trace_mod_l(l, F, a, psi_l, p):
    h = psi_l
    while True:
        try:
            xp = ppow([0, 1], p, h, p)                         # x^p
            yp = ppow(F, (p - 1) // 2, h, p)                   # y^p = f^((p-1)/2) * y
            xp2 = pcompose(xp, xp, h, p)                       # x^(p^2) = (x^p)^p
            yp2 = pmod(pmul(pcompose(yp, xp, h, p), yp, p), h, p)
            P = (pmod([0, 1], h, p), [1])                      # vispārīgais punkts (x, y)
            frob = (xp, yp)
            frob2 = (xp2, yp2)
            qbar = p % l
            qP = mul(qbar, P, F, a, h, p)
            print(f"  modulis h = {show(h)} (deg {len(h) - 1})")
            print(f"  x^p      = {show(xp)}")
            print(f"  x^(p^2)  = {show(xp2)}")
            print(f"  p mod {l} = {qbar};  x-koord. punktam {qbar}P = {show(qP[0])}")
            lhs = add(frob2, qP, F, a, h, p)                   # phi^2(P) + qbar P
            if lhs is O:
                print(f"  phi^2(P) + {qbar}P = O  =>  t = 0 (mod {l})")
                return 0
            R = O
            for tau in range(1, l):
                R = add(R, frob, F, a, h, p)                   # tau * phi(P)
                if R == lhs:
                    print(f"  phi^2(P) + {qbar}P = {tau} * phi(P)  =>  t = {tau} (mod {l})")
                    return tau
            raise AssertionError("tau nav atrasts")
        except NotInvertible as e:
            g = e.g
            print(f"  netriviāls dalītājs {show(g)} -- turpinām pēc moduļa tā")
            h = g if len(g) <= len(pdivmod(h, g, p)[0]) else pdivmod(h, g, p)[0]


def crt(residues):
    t, M = 0, 1
    for r, m in residues:
        k = (r - t) * pow(M, -1, m) % m
        t, M = t + M * k, M * m
    return t, M


def schoof(a, b, p):
    F = [b % p, a % p, 0, 1]
    bound = 4 * isqrt(p) + 4                                   # vajag prod l > 4 sqrt(p)
    primes, prod = [], 1
    for l in range(2, 100):
        if all(l % q for q in range(2, l)) and l != p:
            primes.append(l)
            prod *= l
            if prod * prod > 16 * p:
                break
    print(f"E: y^2 = {show(F)} virs F_{p};  4*sqrt(p) = {4 * p ** 0.5:.2f};  pirmskaitļi {primes}")
    psi = division_polynomials(a, b, p, max(primes))
    res = []
    for l in primes:
        print(f"l = {l}:")
        tl = trace_mod_2(F, p) if l == 2 else trace_mod_l(l, F, a, psi[l], p)
        if l == 2:
            print(f"  => t = {tl} (mod 2)")
        res.append((tl, l))
    t, M = crt(res)
    if t > M // 2:
        t -= M
    print(f"KAT: t = {t} (mod {M}), |t| <= 2 sqrt(p) = {2 * p ** 0.5:.2f}  =>  t = {t}")
    n = p + 1 - t
    print(f"#E = p + 1 - t = {p} + 1 - ({t}) = {n}")
    return n


def brute_force(a, b, p):
    return 1 + sum(1 for x in range(p) for y in range(p) if (y * y - x ** 3 - a * x - b) % p == 0)


if __name__ == "__main__":
    n = schoof(1, 4, 23)
    print("Pārbaude ar pilno pārlasi:", brute_force(1, 4, 23))
    for (a, b, p) in [(2, 2, 17), (-3, 7, 271), (3, 5, 101), (7, 11, 1009)]:
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            s = schoof(a, b, p)
        print(f"y^2 = x^3 + {a}x + {b} virs F_{p}: Šofs {s}, pārlase {brute_force(a, b, p)}")
