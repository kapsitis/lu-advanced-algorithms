import pytest
from myaes_key_sch import *


def test_kshword_tostr():
    key_hex = "000102030405060708090a0b0c0d0e0f"
    numBits = 128
    key_int = int(key_hex, 16)
    key_bytes = key_int.to_bytes(16, 'big', signed = False)

    keyScheduler = KeyScheduler([key_bytes[0:4], key_bytes[4:8], key_bytes[8:12], key_bytes[12:16]], numBits)

    wordValOne = KeySchWord([GfByte(0), GfByte(0), GfByte(0), GfByte(1)])
    assert wordValOne.__str__() == '00000001'

    w1 = keyScheduler.WList[0] + wordValOne
    assert w1.__str__() == '00010202'
    w2 = keyScheduler.WList[3] + wordValOne
    assert w2.__str__() == '0C0D0E0E'
    
def test_kshword_add():
    wordValOne = KeySchWord([GfByte(i) for i in [40, 13, 123, 160]])
    wordValTwo = KeySchWord([GfByte(i) for i in [82, 86, 109, 117]])
    wordResult = wordValOne + wordValTwo
    wordExpected = KeySchWord([GfByte(i) for i in [40 ^ 81, 13 ^ 86, 123 ^ 109, 160 ^ 117]])
    # assert wordResult == wordExpected
    gf0 = GfByte(40) + GfByte(82)
    gf1 = GfByte(13) + GfByte(86)
    gf2 = GfByte(123) + GfByte(109)
    gf3 = GfByte(160) + GfByte(117)
    wordExpected2 = KeySchWord([gf0, gf1, gf2, gf3])
    assert wordResult == wordExpected2


def test_kshword_rmul():
    wordValOne = KeySchWord([GfByte(i) for i in [40, 13, 123, 160]])
    result = 3*wordValOne
    THREE = GfByte(0x03)
    wordExpected = KeySchWord([THREE*GfByte(i) for i in [40, 13, 123, 160]])
    assert result == wordExpected

# Verify, if RotWord() computes correctly
def test_kshword_rotword():
    wordValOne = KeySchWord([GfByte(i) for i in [40, 13, 123, 160]])
    wordExpected = KeySchWord([GfByte(i) for i in [13, 123, 160, 40]])
    result = wordValOne.RotWord()
    assert result == wordExpected

# Verify, if SubWord() computes correctly
def test_kshword_subword():
    wordValOne = KeySchWord([GfByte(i) for i in [0x28, 0x0d, 0x7b, 0xa0]])
    wordExpected = KeySchWord([GfByte(i) for i in [0x34, 0xd7, 0x21, 0xe0]])
    result = wordValOne.SubWord()
    assert result == wordExpected


# Check, if all round keys are correct for a 128-byte KeyScheduler object
def test_key_rounds128():
    key_hex = '000102030405060708090a0b0c0d0e0f'
    key_int = int(key_hex, 16)
    key_bytes = key_int.to_bytes(16, 'big', signed = False)

    numBits = 128
    assert len(key_bytes) == numBits//8

    keyScheduler = KeyScheduler([key_bytes[0:4], key_bytes[4:8], key_bytes[8:12], key_bytes[12:16]], numBits)

    expected_rounds_hex = ['000102030405060708090a0b0c0d0e0f',
    'd6aa74fdd2af72fadaa678f1d6ab76fe',
    'b692cf0b643dbdf1be9bc5006830b3fe',
    'b6ff744ed2c2c9bf6c590cbf0469bf41',
    '47f7f7bc95353e03f96c32bcfd058dfd',
    '3caaa3e8a99f9deb50f3af57adf622aa',
    '5e390f7df7a69296a7553dc10aa31f6b',
    '14f9701ae35fe28c440adf4d4ea9c026',
    '47438735a41c65b9e016baf4aebf7ad2',
    '549932d1f08557681093ed9cbe2c974e',
    '13111d7fe3944a17f307a78b4d2b30c5']

    for i in range(11):
        round_bytes = keyScheduler.getRoundKey(i)
        expected_round_int = int(expected_rounds_hex[i], 16)
        expected_round_bytes = expected_round_int.to_bytes(16, 'big', signed=False)
        assert round_bytes == expected_round_bytes


