# -*- coding: utf-8 -*-
"""pytest testi failam lempel_ziv.py.

Palaišana no repozitorija saknes:
    python -m pytest docs/applied_algorithms/lossless_lempel_ziv/scripts
"""

import math
import random

import pytest

from lempel_ziv import (lz77_decode, lz77_encode, lz77_format, lz77_parse,
                        lz78_decode, lz78_encode, lz78_format, lz78_parse)

INF = math.inf

# Teksti saspiešanai un atspiešanai (arī ar atstarpēm un garumzīmēm).
TEXTS = [
    "",
    "a",
    "banana",
    "mississippi",
    "abcabcabcdabc",
    "to be or not to be",
    "abrakadabra abrakadabra",
    "ķēķis ķēķī",
]


# ------------------------------------------------------------------- LZ77

# (teksts, W, L, trijnieki)
LZ77_EXAMPLES = [
    # 3.1. uzdevums
    ("abcabcabcdabc", 6, INF, "(0,0,a),(0,0,b),(0,0,c),(3,6,d),(4,2,c)"),
    # nav atkārtojumu -- tikai atsevišķi burti
    ("abcdef", 6, INF, "(0,0,a),(0,0,b),(0,0,c),(0,0,d),(0,0,e),(0,0,f)"),
    # sakritība pārklājas ar kodējamo daļu: d = 1, bet ell = 8
    ("aaaaaaaaaa", 1, INF, "(0,0,a),(1,8,a)"),
    # priekšskata buferis L = 3 ierobežo sakritības garumu
    ("aaaaaaaaaa", 1, 3, "(0,0,a),(1,3,a),(1,3,a),(0,0,a)"),
    # logs W = 3 ir par īsu, lai redzētu iepriekšējo "abc" ...
    ("abcXabc", 3, INF, "(0,0,a),(0,0,b),(0,0,c),(0,0,X),(0,0,a),(0,0,b),(0,0,c)"),
    # ... bet W = 4 jau pietiek
    ("abcXabc", 4, INF, "(0,0,a),(0,0,b),(0,0,c),(0,0,X),(4,2,c)"),
    # vienāda garuma sakritībām izvēlas tuvāko: (3,2,z), nevis (6,2,z)
    ("abxabyabz", 32, INF, "(0,0,a),(0,0,b),(0,0,x),(3,2,y),(3,2,z)"),
]


@pytest.mark.parametrize("text, W, L, triples", LZ77_EXAMPLES)
def test_lz77_encode_examples(text, W, L, triples):
    assert lz77_format(lz77_encode(text, W, L)) == triples


@pytest.mark.parametrize("text, W, L, triples", LZ77_EXAMPLES)
def test_lz77_decode_examples(text, W, L, triples):
    assert lz77_decode(lz77_parse(triples)) == text


@pytest.mark.parametrize("L", [INF, 1, 4])
@pytest.mark.parametrize("W", [1, 3, 32])
@pytest.mark.parametrize("text", TEXTS)
def test_lz77_round_trip(text, W, L):
    assert lz77_decode(lz77_encode(text, W, L)) == text


def test_lz77_random_round_trip():
    rng = random.Random(77)
    for _ in range(500):
        text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 40)))
        W = rng.randint(1, 8)
        L = rng.choice([INF, rng.randint(1, 8)])
        assert lz77_decode(lz77_encode(text, W, L)) == text, (text, W, L)


def test_lz77_decode_rejects_bad_offset():
    with pytest.raises(ValueError):
        lz77_decode(lz77_parse("(0,0,a),(5,1,b)"))    # 5 pozīcijas atpakaļ vēl nekā nav
    with pytest.raises(ValueError):
        lz77_decode(lz77_parse("(0,0,a),(0,1,b)"))    # garums bez nobīdes


def test_lz77_parse_rejects_garbage():
    with pytest.raises(ValueError):
        lz77_parse("(0,0,a) (1,1,b)")


# ------------------------------------------------------------------- LZ78

# (teksts, alfabēts, kodi)
LZ78_EXAMPLES = [
    # piemērs no ../index.md
    ("abcabcabcdabcaba", "abcd", "a,b,c,1,3,2,d,4,1,a"),
    # 3.2. uzdevums
    ("ABCABCABCDABCABA", "ABCD", "A.B.C.1.3.2.D.4.1.A"),
    # 3.3. uzdevums
    ("aabaaabaaaab", "ab", "a,a,b,1,2,4,2"),
    # 3.4. uzdevums: kodi 3 un 4 vēl nav atkodētāja vārdnīcā
    ("abaaaaaa", "ab", "a,b,a,3,4"),
    # nav atkārtojumu -- tikai atsevišķi burti
    ("abcd", "abcd", "a,b,c,d"),
    # frāzes aa, aaa, aaaa -- katrs kods vēl nav atkodētāja vārdnīcā
    ("aaaaaaaaaa", "a", "a,1,2,3"),
]


@pytest.mark.parametrize("text, S, codes", LZ78_EXAMPLES)
def test_lz78_encode_examples(text, S, codes):
    assert lz78_encode(text, S) == lz78_parse(codes)


@pytest.mark.parametrize("text, S, codes", LZ78_EXAMPLES)
def test_lz78_decode_examples(text, S, codes):
    assert lz78_decode(lz78_parse(codes), S) == text


def test_lz78_format_matches_page_notation():
    assert lz78_format(lz78_encode("abcabcabcdabcaba", "abcd")) == "a,b,c,1,3,2,d,4,1,a"
    assert lz78_format(lz78_encode("ABCABCABCDABCABA", "ABCD"), sep=".") == "A.B.C.1.3.2.D.4.1.A"


@pytest.mark.parametrize("text", TEXTS)
def test_lz78_round_trip(text):
    S = "".join(sorted(set(text)))
    assert lz78_decode(lz78_encode(text, S), S) == text


def test_lz78_random_round_trip():
    rng = random.Random(78)
    for _ in range(500):
        S = rng.choice(["ab", "abc"])
        text = "".join(rng.choice(S) for _ in range(rng.randint(0, 60)))
        assert lz78_decode(lz78_encode(text, S), S) == text, text


def test_lz78_encode_rejects_letter_outside_alphabet():
    with pytest.raises(ValueError):
        lz78_encode("abc", "ab")


def test_lz78_decode_rejects_unknown_code():
    with pytest.raises(ValueError):
        lz78_decode(lz78_parse("a,b,5"), "ab")         # nākamais iespējamais kods ir 2
