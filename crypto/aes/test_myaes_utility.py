import pytest

from myaes_utility import *

# High-level test for AES128 encryption (single block)
def test_aes128_block_encrypt():
    # Start with hex representations
    block_hex = "00112233445566778899aabbccddeeff"
    key_hex = "000102030405060708090a0b0c0d0e0f"
    expected_ciphertext_hex = "69c4e0d86a7b0430d8cdb78070b4c55a"

    # Convert hex to bytes
    block_int = int(block_hex, 16)
    block_bytes = block_int.to_bytes(16, 'big', signed = False)
    key_int = int(key_hex, 16)
    key_bytes = key_int.to_bytes(16, 'big', signed = False)

    # Call the AesUtility.encode(...)
    aes_utility = AesUtility(key_bytes)
    ciphertext = aes_utility.encode_block(block_bytes)
    ciphertext_hex = binascii.hexlify(ciphertext).decode('utf-8')

    # Compare with expected value
    print('ciphertext_hex = {}'.format(ciphertext_hex))
    assert ciphertext_hex == expected_ciphertext_hex



def test_aes128_block_decrypt():
    # Start with hex representations
    block_hex = "69c4e0d86a7b0430d8cdb78070b4c55a"
    key_hex = "000102030405060708090a0b0c0d0e0f"
    expected_plaintext_hex = "00112233445566778899aabbccddeeff"

    # Convert hex to bytes
    block_int = int(block_hex, 16)
    block_bytes = block_int.to_bytes(16, 'big', signed = False)
    key_int = int(key_hex, 16)
    key_bytes = key_int.to_bytes(16, 'big', signed = False)

    # Call the AesUtility.encode(...)
    aes_utility = AesUtility(key_bytes)
    plaintext = aes_utility.decode_block(block_bytes)
    plaintext_hex = binascii.hexlify(plaintext).decode('utf-8')

    # Compare with expected value
    print('plaintext_hex = {}'.format(plaintext_hex))
    assert plaintext_hex == expected_plaintext_hex

    

