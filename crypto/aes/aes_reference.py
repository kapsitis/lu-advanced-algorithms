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
    key = binascii.unhexlify('e6aa51d07d884db2cfc83c6e7b198141')
    IV = binascii.unhexlify('e4e85bb6fd7e2b05175e111a4e33bbc4')
    print("iv_bytes = {}".format(binascii.hexlify(IV).decode('utf-8')))
    
    encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
    plaintext = binascii.unhexlify('49572d5477f0aca72576e50d8372c4b9759f79adf0a6a3d0ccc409355d4b3c9d')
    ciphertext = encryptor.encrypt(plaintext)
    print('CipherText is {}'.format(binascii.hexlify(ciphertext).decode('utf-8')))



if __name__ == '__main__':
    main()
