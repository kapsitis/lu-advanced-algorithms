import pytest
from GF8 import *

def test_add():
    a = GF8(0x57)
    b = GF8(0x83)
    expected = GF8(0xD4)
    c = a + b
    assert c == expected 

def test_mul():
    a = GF8(0x57)
    b = GF8(0x83)
    expected = GF8(0xC1)
    c = a * b
    assert c == expected

def test_inverse():
    args = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
    vals = [0x00, 0x01, 0x8D, 0xF6, 0xCB, 0x52, 0x7B, 0xD1, 0xE8, 0x4F]
    for i in range(len(args)): 
        x = GF8(args[i])
        x_inv = x.inv()
        assert x_inv == GF8(vals[i])

def test_sbox():
    a = GF8(0x9a)
    expected = GF8(0xb8)
    b = a.sbox()
    assert b == expected

def test_sbox2():
    args = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
    vals = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76]
    for i in range(len(args)): 
        x = GF8(args[i])
        y = x.sbox()
        assert y == GF8(vals[i])

    
def test_invsbox():
    a = GF8(0xb8)
    expected = GF8(0x9a)
    b = a.inv_sbox()
    assert b == expected

def test_invsbox2():
    args = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
    vals = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb]
    for i in range(len(args)): 
        x = GF8(args[i])
        y = x.inv_sbox()
        assert y == GF8(vals[i])

# Checking round constants: https://en.wikipedia.org/wiki/AES_key_schedule#Round_constants
def test_round_constants():
    # TODO - Replace this by the constants self.rc in KeyScheduler class
    expected_constants = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
    for i in range(1, len(expected_constants)-1):
        rc_prev = GF8(expected_constants[i])
        rc_next = GF8(expected_constants[i+1])
        TWO = GF8(0x02)
        ZERO = GF8(0x00)
        assert TWO*rc_prev == rc_next
        # Note that in GF(256) we have A + A = 0 (not A + A = 2*A)
        assert rc_prev + rc_prev == ZERO

# def test_get_double():
#     TWO = GF8(0x02)
#     for i in range(256):
#         gfi = GF8(i)
#         gfi_double1 = TWO*gfi
#         gfi_double2 = gfi.get_double()
#         assert gfi_double1 == gfi_double2

