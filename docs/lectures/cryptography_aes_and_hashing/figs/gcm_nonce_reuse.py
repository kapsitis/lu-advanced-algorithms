# -*- coding: utf-8 -*-
"""11.5. uzdevuma atrisinājums: AES-GCM nonce atkārtošana ("aizliegtais uzbrukums").

Divi viena bloka ziņojumi bez AAD šifrēti ar vienu un to pašu atslēgu un nonce.
Tagam T = C*H^2 + L*H + E_K(J0) (laukā GF(2^128)), tāpēc
    T1 + T2 = (C1 + C2) * H^2   =>   H^2 = (T1 + T2) / (C1 + C2),
un H ir vienīgā kvadrātsakne: H = (H^2)^(2^127), jo kāpināšana kvadrātā laukā
GF(2^128) ir bijekcija. Pēc tam aprēķina E_K(J0) un viltotā ziņojuma tagu.

GCM blokus attēlo par lauka elementiem "apgrieztā" bitu secībā: bloka pirmais
(augstākais) bits ir koeficients pie x^0 (NIST SP 800-38D, 6.3).

    pip install galois
    python gcm_nonce_reuse.py
"""

import galois

GF = galois.GF(2**128, irreducible_poly="x^128 + x^7 + x^2 + x + 1",
               primitive_element="x", verify=False)


def el(block_hex):
    """16 baitu GCM bloks (hex) -> lauka elements."""
    return GF(int(format(int(block_hex, 16), "0128b")[::-1], 2))


def block(e):
    """Lauka elements -> 16 baitu GCM bloks (hex)."""
    return "%032x" % int(format(int(e), "0128b")[::-1], 2)


def xor_hex(a, b):
    return "%032x" % (int(a, 16) ^ int(b, 16))


# Uzdevuma dati (atslēga uzbrucējam nav zināma)
P1 = b"PAY ALICE 100EUR".hex()
C1, T1 = "387e417fd9e07f33c30cbd2dd15347f4", "b1ee85781df2f20409071e20cf681ff7"
C2, T2 = "387e417fdae37450bf1cbc2dc15347f4", "2d6fdb7a33538dfc0b526cdf458ac003"
L = "%032x" % 128                       # len(A) = 0 biti, len(C) = 128 biti

# (a) otrais atklātais teksts: CTR atslēgas plūsma ir vienāda
P2 = xor_hex(xor_hex(C1, C2), P1)
print("(a) P2 =", bytes.fromhex(P2))

# (b) GHASH atslēga H
H2 = (el(T1) + el(T2)) / (el(C1) + el(C2))
H = H2 ** (2**127)
print("(b) H  =", block(H))

# (c) viltojums: P3 tajā pašā pozīcijā, tags ar to pašu E_K(J0)
EJ0 = el(T1) + el(C1) * H**2 + el(L) * H
P3 = b"PAY EVE 9999 EUR".hex()
C3 = xor_hex(xor_hex(C1, P1), P3)
T3 = el(C3) * H**2 + el(L) * H + EJ0
print("(c) E_K(J0) =", block(EJ0))
print("    C3 =", C3, " T3 =", block(T3))

try:                                    # pārbaude ar īsto atslēgu (ja ir pakete cryptography)
    import hashlib
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key = hashlib.sha256(b"LU algoritmi 2026").digest()[:16]
    nonce = bytes.fromhex("cafebabefacedbaddecaf888")
    print("    check:", AESGCM(key).decrypt(nonce, bytes.fromhex(C3 + block(T3)), None))
except ImportError:
    pass
