# -*- coding: utf-8 -*-
"""AES-128 un GF(2^8) aritmētika tīrā Python (mācību nolūkiem, NAV konstanta laika!).

Moduli izmanto attēlu skripti (aes_round.py, aes_key_expansion.py, ecb_penguin.py)
un uzdevumu atbilžu pārbaude (lecture_numbers.py). Funkcijas seko FIPS 197:

    python aes128.py      # pārbauda FIPS 197 testu vektorus
"""

M = 0x11B                              # m(x) = x^8 + x^4 + x^3 + x + 1


def xtime(a):
    """Reizināšana ar x (t.i., ar 0x02) laukā GF(2^8)."""
    a <<= 1
    return a ^ M if a & 0x100 else a


def gmul(a, b):
    """Reizinājums a*b laukā GF(2^8): "skolas" reizināšana ar xtime un XOR."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = xtime(a)
        b >>= 1
    return r


def ginv(a):
    """Apgrieztais elements a^(-1) = a^254 (0 attēlo par 0)."""
    r, p, e = 1, a, 254
    while e:
        if e & 1:
            r = gmul(r, p)
        p = gmul(p, p)
        e >>= 1
    return r if a else 0


def rotl8(b, k):
    return ((b << k) | (b >> (8 - k))) & 0xFF


def affine(b):
    """S-bloka afīnais solis: b + rotl(b,1) + rotl(b,2) + rotl(b,3) + rotl(b,4) + 0x63."""
    return b ^ rotl8(b, 1) ^ rotl8(b, 2) ^ rotl8(b, 3) ^ rotl8(b, 4) ^ 0x63


SBOX = [affine(ginv(a)) for a in range(256)]
INV_SBOX = [0] * 256
for _a, _s in enumerate(SBOX):
    INV_SBOX[_s] = _a

RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


# --- stāvoklis: saraksts no 16 baitiem, s[r + 4c] = rinda r, kolonna c -------------

def sub_bytes(s):
    return [SBOX[b] for b in s]


def shift_rows(s):
    return [s[r + 4 * ((c + r) % 4)] for c in range(4) for r in range(4)]


def mix_column(col):
    a0, a1, a2, a3 = col
    return [gmul(a0, 2) ^ gmul(a1, 3) ^ a2 ^ a3,
            a0 ^ gmul(a1, 2) ^ gmul(a2, 3) ^ a3,
            a0 ^ a1 ^ gmul(a2, 2) ^ gmul(a3, 3),
            gmul(a0, 3) ^ a1 ^ a2 ^ gmul(a3, 2)]


def mix_columns(s):
    out = []
    for c in range(4):
        out += mix_column(s[4 * c:4 * c + 4])
    return out


def add_round_key(s, k):
    return [a ^ b for a, b in zip(s, k)]


def rot_word(w):
    return w[1:] + w[:1]


def sub_word(w):
    return [SBOX[b] for b in w]


def key_expansion(key):
    """44 vārdi w[0..43] (katrs -- 4 baiti) no 16 baitu atslēgas."""
    w = [list(key[4 * i:4 * i + 4]) for i in range(4)]
    for i in range(4, 44):
        t = w[i - 1]
        if i % 4 == 0:
            t = sub_word(rot_word(t))
            t = [t[0] ^ RCON[i // 4 - 1]] + t[1:]
        w.append([a ^ b for a, b in zip(w[i - 4], t)])
    return w


def round_keys(key):
    w = key_expansion(key)
    return [sum(w[4 * r:4 * r + 4], []) for r in range(11)]


def encrypt_trace(block, key):
    """Atgriež šifrteksta bloku un starprezultātu sarakstu [(nosaukums, stāvoklis), ...]."""
    rk = round_keys(key)
    s = add_round_key(list(block), rk[0])
    trace = [("start", 1, s)]
    for r in range(1, 11):
        s = sub_bytes(s)
        trace.append(("s_box", r, s))
        s = shift_rows(s)
        trace.append(("s_row", r, s))
        if r < 10:
            s = mix_columns(s)
            trace.append(("m_col", r, s))
        trace.append(("k_sch", r, rk[r]))
        s = add_round_key(s, rk[r])
        if r < 10:
            trace.append(("start", r + 1, s))
    return bytes(s), trace


def encrypt_block(block, key):
    return encrypt_trace(block, key)[0]


def ecb_encrypt(data, key):
    assert len(data) % 16 == 0
    return b"".join(encrypt_block(data[i:i + 16], key) for i in range(0, len(data), 16))


def ctr_encrypt(data, key, nonce12):
    """CTR kā GCM: skaitītāja bloks = nonce (12 baiti) || 32 bitu skaitītājs (sākot ar 2)."""
    out = bytearray()
    for j in range(0, len(data), 16):
        ks = encrypt_block(nonce12 + (2 + j // 16).to_bytes(4, "big"), key)
        out += bytes(a ^ b for a, b in zip(data[j:j + 16], ks))
    return bytes(out)


def hx(bs, sep=" "):
    return sep.join("%02x" % b for b in bs)


if __name__ == "__main__":
    assert gmul(0x57, 0x83) == 0xC1 and gmul(0x57, 0x13) == 0xFE
    assert SBOX[0x00] == 0x63 and SBOX[0x53] == 0xED
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    assert hx(key_expansion(key)[4], "") == "a0fafe17"
    ct = encrypt_block(bytes.fromhex("3243f6a8885a308d313198a2e0370734"), key)
    assert ct.hex() == "3925841d02dc09fbdc118597196a0b32", ct.hex()
    ct = encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff"),
                       bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert ct.hex() == "69c4e0d86a7b0430d8cdb78070b4c55a", ct.hex()
    assert mix_column([0xdb, 0x13, 0x53, 0x45]) == [0x8e, 0x4d, 0xa1, 0xbc]
    print("FIPS 197 test vectors: OK")
