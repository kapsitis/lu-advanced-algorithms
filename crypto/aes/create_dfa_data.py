from myaes_utility import *

def main():
    # Start with hex representations
    # block_hex = "00112233445566778899aabbccddeeff"
    # key_hex = "000102030405060708090a0b0c0d0e0f"
    # expected_ciphertext_hex = "69c4e0d86a7b0430d8cdb78070b4c55a"

    block_hex = "48656c6c6f20776f726c642120202020";
    key_hex = "def4be2036b28d9cc8e4388452635414";
    expected_ciphertext_hex = "e80027fcb3f4107706845341cc1d371c";


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


if __name__ == '__main__':
    main()