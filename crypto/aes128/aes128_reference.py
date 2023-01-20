from Crypto.Cipher import AES

import binascii

import os


def some():
    return 3

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
