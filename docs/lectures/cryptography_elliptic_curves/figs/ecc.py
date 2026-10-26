# -*- coding: utf-8 -*-
"""Mācību eliptisko līkņu aritmētika (Veierštrāsa forma y^2 = x^3 + ax + b virs F_p).

Lekcijas skaitļu pārbaudei un attēlu skriptiem. Punktu glabā kā pāri (x, y);
bezgalīgi tālo punktu O attēlo ar None. Nav konstanta laika -- tikai mācībām!

    python ecc.py        # izdrukā lekcijas piemērus un uzdevumu atbildes
"""

O = None                                 # bezgalīgi tālais punkts (neitrālais elements)


class Curve:
    def __init__(self, a, b, p):
        assert (4 * a ** 3 + 27 * b ** 2) % p != 0, "singulāra līkne"
        self.a, self.b, self.p = a % p, b % p, p

    def on_curve(self, P):
        if P is O:
            return True
        x, y = P
        return (y * y - x ** 3 - self.a * x - self.b) % self.p == 0

    def neg(self, P):
        return O if P is O else (P[0], -P[1] % self.p)

    def add(self, P, Q):
        """P + Q ar hordas un pieskares formulām."""
        p = self.p
        if P is O:
            return Q
        if Q is O:
            return P
        (x1, y1), (x2, y2) = P, Q
        if x1 == x2 and (y1 + y2) % p == 0:
            return O                     # P + (-P) = O (arī 2P, ja y = 0)
        if P == Q:
            lam = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam * lam - x1 - x2) % p
        return (x3, (lam * (x1 - x3) - y1) % p)

    def lam(self, P, Q):
        """Slīpums lambda (aprēķinu izdrukām)."""
        p = self.p
        (x1, y1), (x2, y2) = P, Q
        if P == Q:
            return (3 * x1 * x1 + self.a) * pow(2 * y1, -1, p) % p
        return (y2 - y1) * pow(x2 - x1, -1, p) % p

    def points(self):
        """Visi afīnie punkti (bez O), sakārtoti pēc x, y."""
        p = self.p
        sq = {}
        for y in range(p):
            sq.setdefault(y * y % p, []).append(y)
        return [(x, y) for x in range(p) for y in sq.get((x ** 3 + self.a * x + self.b) % p, [])]

    def order(self):
        """Grupas kārta #E (ieskaitot O)."""
        return len(self.points()) + 1

    def point_order(self, P):
        k, Q = 1, P
        while Q is not O:
            Q, k = self.add(Q, P), k + 1
        return k

    def mul(self, k, P):
        """Dubultošana un saskaitīšana (no augstākā bita)."""
        R = O
        for bit in bin(k)[2:] if k > 0 else "":
            R = self.add(R, R)
            if bit == "1":
                R = self.add(R, P)
        return R

    def mul_trace(self, k, P):
        """Dubultošana un saskaitīšana: soļu saraksts (bits, operācija, R)."""
        R, steps = O, []
        for i, bit in enumerate(bin(k)[2:]):
            if i == 0:
                R = P
                steps.append((bit, "R = P", R))
                continue
            R = self.add(R, R)
            steps.append((bit, "R = 2R", R))
            if bit == "1":
                R = self.add(R, P)
                steps.append((bit, "R = R + P", R))
        return steps

    def ladder_trace(self, k, P):
        """Montgomerija kāpnes: (bits, R0, R1) pēc katra bita; invariants R1 - R0 = P."""
        R0, R1, steps = O, P, []
        for bit in bin(k)[2:]:
            if bit == "0":
                R0, R1 = self.add(R0, R0), self.add(R0, R1)
            else:
                R0, R1 = self.add(R0, R1), self.add(R1, R1)
            steps.append((bit, R0, R1))
        return steps


def fmt(P):
    return "O" if P is O else "(%d, %d)" % P


# ---------------------------------------------------------------- ECDSA
def ecdsa_sign(E, G, n, d, h, k):
    R = E.mul(k, G)
    r = R[0] % n
    s = pow(k, -1, n) * (h + r * d) % n
    assert r != 0 and s != 0
    return r, s


def ecdsa_verify(E, G, n, Q, h, sig):
    r, s = sig
    w = pow(s, -1, n)
    u1, u2 = h * w % n, r * w % n
    X = E.add(E.mul(u1, G), E.mul(u2, Q))
    return X is not O and X[0] % n == r, (w, u1, u2, X)


# ---------------------------------------------------------------- lekcijas piemēri
E17, G17 = Curve(2, 2, 17), (5, 1)                     # y^2 = x^3 + 2x + 2 virs F_17
E23, G23, N23 = Curve(1, 4, 23), (0, 2), 29            # y^2 = x^3 + x + 4 virs F_23
EL, GL = Curve(-3, 7, 263), None                       # Montgomerija kāpņu piemēra līkne (sk. zemāk)

P256 = dict(
    p=2 ** 256 - 2 ** 224 + 2 ** 192 + 2 ** 96 - 1,
    a=-3,
    b=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    Gx=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    Gy=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
    n=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
)


if __name__ == "__main__":
    print("DH Z_23, g=5:", pow(5, 6, 23), pow(5, 15, 23), pow(8, 15, 23), pow(19, 6, 23))
    print("F17:", E17.order(), [fmt(E17.mul(k, G17)) for k in range(1, 20)])
    print("F23:", E23.order(), E23.point_order(G23))
    print(" ", [(k, fmt(E23.mul(k, G23))) for k in range(1, 29)])
    E = Curve(P256["a"], P256["b"], P256["p"])
    G = (P256["Gx"], P256["Gy"])
    print("P-256: G on curve", E.on_curve(G), " nG = O", E.mul(P256["n"], G) is O)
