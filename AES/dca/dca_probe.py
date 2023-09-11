import sys
import math

sys.path.append('../aes')

from myaes_tracer import *
from myaes_gfbyte import *

ZERO_INPUT = "00000000000000000000000000000000"


KEY_HEX = "000102030405060708090a0b0c0d0e0f"



def getBitList(arg):
    result = []
    for i in range(8):
        result.append(arg % 2)
        arg = arg // 2
    result.reverse()
    return result


# [0,0,1,1,1,0,1,1]
# [0,1,0,0,1,1,0,0]
# 1/8 (neder, jo xors - tiira korelaacija)
# 1/3 (abaas ir nulles) - 2/3
# 1/5 (abas ir vieninieki) - 4/5

# Mutual information (Arturs P.)

# |1/3 - 1/5| - distance (delta)


# Phi (delta?); Pearson: Divas virknes (0 un 1) - vienu izvēlas kā galveno; skatāmies, kur abās ir nulles
# A = ({a[i] == 0 and b[i] == 0}) izdalaam ar to, cik nulles bija galvenajaa virknee
# B = |{a[i] == atrod
# A - B

# [0,1,0,1]
# [1,0,1,0]
# 0/2
# 0/2

# Mutual information
# Pearon correlation (max absolute value)

# 2048 input ([-0.05, 0.05])


# a, b are bit sequences
def pearsonAsBits(a,b):
    ss = 0
    sdA = 0
    sdB = 0
    avgA = sum(a)/len(a)
    avgB = sum(b)/len(b)
    for i in range(len(a)):
        ss += (a[i] - avgA)*(b[i] - avgB)
        sdA += (a[i] - avgA)**2
        sdB += (b[i] - avgB)**2
    return ss/math.sqrt(sdA*sdB)

def phiCoefficient(a,b):
    assert len(a) == len(b)
    M = [[0,0]]*2  # Confusion matrix 2*2
    for i in range(len(a)):
        M[a[i]][b[i]] += 1
    denom = (M[0][0]+M[0][1])*(M[1][0]+M[1][1])*(M[0][0]+M[1][0])*(M[0][1]+M[1][1])
    if denom == 0:
        return 0
    else:
        return (M[0][0]*M[1][1] - M[0][1]*M[1][0])/math.sqrt(denom)


# Return a list of 256 byte-vectors; each containing 256 bytes (as a vector of 2048 bits)
# result[keyByte][8*i + j] equals the j-th bit from the byte sbox(keyByte + i)
def get_sbox_vectors():
    result = []
    for cand_byte in range(0, 256):
        bit_list_sbox = []
        kGB = GfByte(cand_byte)
        for i in range(0,256):
            iGB = GfByte(i)
            sum = kGB + iGB
            sum_sbox = sum.sbox()
            bit_list_sbox += getBitList(sum_sbox.b)
        result.append(bit_list_sbox)
    assert len(result) == 256
    assert len(result[0]) == 2048
    assert len(set(result[0])) == 2        
    return result


# all_state_vectors contains 256 lists of length 40. 
# all_state_vectors[i] has 40 items - each one is 32-hex digits long (16 bytes). 
# Extract "pos" item out of all 40 traces.
# Also compute all Sbox values; return all 40 correlation coefficients.
def probe_keybyte(pos, all_state_vectors):

    # Largest correlation and best candidate byte observed so far
    corr_max = -1
    cand_max = -1
    # what state (out of 40 states) offers the best correlation with the sbox vector
    state_max = -1
    offset_max = -1

    sbox_vectors = get_sbox_vectors()

    # Do 40*16 probes in all_state_vectors.  
    # state is in [0;39]; offset is in [0;15]
    # The probe for the given "state" and "offset" extracts the sequence of bytes
    # (what does the byte for "state" and "offset" look like, as we apply encryption to 
    # various inputs, where one of the bytes changes from 00 to FF.)  
    for state in range(0, 40):
        for offset in range(0, 16):

            my_bit_list = []
            extracted_bytes = [int(state_vectors[state][(2*offset):(2*offset+2)], base=16) for state_vectors in all_state_vectors]
            for i in range(0,256):
                my_bit_list += getBitList(extracted_bytes[i])
            
            assert len(my_bit_list) == 2048

            for keyByte in range(0,256):
                corr = abs(phiCoefficient(sbox_vectors[keyByte], my_bit_list))
                if corr > corr_max:
                    corr_max = corr
                    cand_max = keyByte
                    state_max = state
                    offset_max = offset

    return (cand_max, corr_max, state_max, offset_max)
        


def main():

    aesTracer = AesTracer('../dca/input.txt', True)
    aesTracer.delete_file()

    # Guessing just the 1st byte
    for pos in range(2):
        # all_state_vectors = []
        aesTracer.reset()
        for j in range(256):
            jGB = GfByte(j)
            block_for_probe = ZERO_INPUT[0:(2*pos)] + jGB.__str__()[0:2] + ZERO_INPUT[(2*pos+2):32]
            aesTracer.record(block_for_probe, KEY_HEX)
        (best_keybyte, corr, state, offset) = probe_keybyte(pos, aesTracer.get_vectors())
        print("Keybyte in pos {} is {}, corr={}, state={}, offset={}".format(pos, GfByte(best_keybyte), corr, state, offset))
        aesTracer.to_file()


if __name__ == '__main__':
    main()    
