import pytest
import aes128_reference

def test_something():
    result = aes128_reference.some()
    assert 3==result

# ... 
def test_reference():
    PLAINTEXT = 0x00112233445566778899aabbccddeeff
    KEY = 0x000102030405060708090a0b0c0d0e0f
    OUTPUT = 0x69c4e0d86a7b0430d8cdb78070b4c55a
    