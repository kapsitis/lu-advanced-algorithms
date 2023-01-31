import binascii

import os

from Crypto.Cipher import AES


# This class uses an external library implementations of AES (to check consistency with AesUtility)
def aes128_encrypt_block(block_int, key_int):
    block_bytes = block_int.to_bytes(16, 'big', signed = False)
    key_bytes = key_int.to_bytes(16, 'big', signed = False)
    zero = 0
    iv_bytes = zero.to_bytes(16, 'big', signed = False)
    encryptor = AES.new(key_bytes, AES.MODE_ECB)
    ciphertext = encryptor.encrypt(block_bytes)
    return ciphertext


def main():
    key = binascii.unhexlify('1F61ECB5ED5D6BAF8D7A7068B28DCC8E')
    IV = os.urandom(16)
    iv_bytes = binascii.hexlify(IV).upper()
    print("iv_bytes = {}".format(iv_bytes))
    # b'3C118E12E1677B8F21D4922BE4B2398E'
    
    encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
    text = binascii.unhexlify('020ABC00ABCDEFf8d500000123456789')
    ciphertext = encryptor.encrypt(text)
    print(binascii.hexlify(ciphertext).upper())

if __name__ == '__main__':
    main()
