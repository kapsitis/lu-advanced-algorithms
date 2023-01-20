import sys

import aes128_reference

import binascii

from Crypto.Cipher import AES


def encrypt_block(block_int, key_int):
    block_bytes = block_int.to_bytes(32, 'big', signed = False)
    key_bytes = key_int.to_bytes(32, 'big', signed = False)
    zero = 0
    iv_bytes = zero.to_bytes(32, 'big', signed = False)
    encryptor = AES.new(key_bytes, AES.MODE_ECB)
    ciphertext = encryptor.encrypt(block_bytes)
    # print(binascii.hexlify(ciphertext).upper())
    return ciphertext

def main():
    if not (len(sys.argv) in [1,3]):
        print('Usage: python oneblock_aes128.py [<hex-block-128bits> <hex-key-128bits>]')
        return
    
    # default values
    block_hex = "0x00112233445566778899aabbccddeeff"
    key_hex = "0x000102030405060708090a0b0c0d0e0f"
    output_hex = "0x69c4e0d86a7b0430d8cdb78070b4c55a"
    if len(sys.argv) == 3:
        block_hex = sys.argv[1]
        key_hex = sys.argv[2]

    block_int = int(block_hex, 16)
    key_int = int(key_hex, 16)
    ciphertext = encrypt_block(block_int, key_int)
    print('type(ciphertext) = {}'.format(type(ciphertext)))
    print(binascii.hexlify(ciphertext).upper())
    print(ciphertext.hex())

if __name__ == '__main__':
    main()
