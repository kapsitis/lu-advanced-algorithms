# ECB, CBC, CTR modes

from myaes_key_sch import *
from myaes_state import *

class AesUtility:
    def __init__(self, key_bytes):
        self.key_bytes = key_bytes


    def encode_block(self, block_bytes):
        # expected_output_hex = "69c4e0d86a7b0430d8cdb78070b4c55a"
        # block_int = int(block_hex, 16)
        # block_bytes = block_int.to_bytes(16, 'big', signed = False)
        #key_int = int(key_hex, 16)
        #key_bytes = key_int.to_bytes(16, 'big', signed = False)

        assert len(block_bytes) == 16
        # assert len(key_bytes) == numBits//8
        numBits = len(self.key_bytes)*8
        assert numBits in [128, 192, 256]    


        #keyScheduler = KeySchWord(key_bytes)
        keyScheduler = KeyScheduler([self.key_bytes[0:4], self.key_bytes[4:8], self.key_bytes[8:12], self.key_bytes[12:16]], numBits)
        #for i in range(11):
        #    roundKey = keyScheduler.getRoundKey(i)
        #    print("Key for round {} is {}".format(i, binascii.hexlify(roundKey)))

        # TODO - add this as a constant to State class?
        mixColMatrix = State(b'\x02\x01\x01\x03\x03\x02\x01\x01\x01\x03\x02\x01\x01\x01\x03\x02')

        state = State(block_bytes)
        roundKey = keyScheduler.getRoundKey(0)
        state.addRoundKey(roundKey)

        for round in range(1,11):
            print('round[{}].start {}'.format(round, state))
            state.SubBytes()
            print('round[{}].s_box {}'.format(round, state))
            state.ShiftRows()
            print('round[{}].s_row {}'.format(round, state))
            if round < 10:
                state.MixColumns(mixColMatrix)
                print('round[{}].m_col {}'.format(round, state))
            roundKey = keyScheduler.getRoundKey(round)
            print('round[{}].k_sch {}'.format(round, binascii.hexlify(roundKey)))
            state.addRoundKey(roundKey)    
            print()

        return state.getBytes()
        # print('round[10].output {}'.format(state))


