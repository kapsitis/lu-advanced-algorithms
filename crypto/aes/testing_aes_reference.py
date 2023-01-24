import pytest

import aes_reference

import binascii


# See https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf, page 35
def test_reference():
    plaintext_hex = "00112233445566778899aabbccddeeff"
    key_hex = "000102030405060708090a0b0c0d0e0f"
    # Expected ciphertext
    expected_hex = "69c4e0d86a7b0430d8cdb78070b4c55a"

    block_int = int(plaintext_hex, 16)
    key_int = int(key_hex, 16)
    ciphertext = aes_reference.aes128_encrypt_block(block_int, key_int)
    assert isinstance(ciphertext, bytes)
    ciphertext_hex = binascii.hexlify(ciphertext).upper().decode('utf-8')
    print('ciphertext_hex = {}'.format(ciphertext_hex))
    assert ciphertext_hex == expected_hex.upper()


