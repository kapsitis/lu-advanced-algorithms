import sys

import aes_reference

from myaes_gfbyte import *
from myaes_key_sch import *
from myaes_state import *

import binascii


# The input of 16 GfByte values - in column major order.
def shift_rows(state):
    result = []
    for col in range(4):
        for row in range(4):
            new_col = (col + row) % 4
            result.append(state[4*new_col + row])
    return result


def main():
    if not (len(sys.argv) in [1,4]):
        print('Usage: python myaes_main.py [<hex-block> <hex-key> <numbits>]')
        return 1
    
    # default values
    block_hex = "00112233445566778899aabbccddeeff"
    key_hex = "000102030405060708090a0b0c0d0e0f"
    numBits = 128
    expected_output_hex = "69c4e0d86a7b0430d8cdb78070b4c55a"
    block_int = int(block_hex, 16)
    block_bytes = block_int.to_bytes(16, 'big', signed = False)
    key_int = int(key_hex, 16)
    key_bytes = key_int.to_bytes(16, 'big', signed = False)

    if len(sys.argv) == 3:
        block_hex = sys.argv[1]
        key_hex = sys.argv[2]
        numBits = int(sys.arv[3])
    assert numBits in [128, 192, 256]    
    assert len(block_bytes) == 16
    assert len(key_bytes) == numBits//8


    #keyScheduler = KeySchWord(key_bytes)
    keyScheduler = KeyScheduler([key_bytes[0:4], key_bytes[4:8], key_bytes[8:12], key_bytes[12:16]], numBits)
    #for i in range(11):
    #    roundKey = keyScheduler.getRoundKey(i)
    #    print("Key for round {} is {}".format(i, binascii.hexlify(roundKey)))

    state = State(block_bytes)
    roundKey = keyScheduler.getRoundKey(0)
    state.addRoundKey(roundKey)
    print('s1.start bytes are {}'.format(state))

    state.SubBytes()
    print('s1.s_box bytes are {}'.format(state))


    
    

    print("******************* CALL CRYPTO API ************************")
    
    key_int = int(key_hex, 16)
    ciphertext = aes_reference.aes128_encrypt_block(block_int, key_int)
    print('type(ciphertext) = {}'.format(type(ciphertext)))
    print(binascii.hexlify(ciphertext).upper())
    print('ciphertext = {}'.format(ciphertext.hex()))
    print('expected   = {}'.format(expected_output_hex))

if __name__ == '__main__':
    main()
