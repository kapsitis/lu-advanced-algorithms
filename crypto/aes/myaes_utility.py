# ECB, CBC, CTR modes

from myaes_key_sch import *
from myaes_state import *
import logging

class AesUtility:
    def __init__(self, key_bytes, iv=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'):
        self.key_bytes = key_bytes
        self.numBits = len(key_bytes)*8
        # print('***************************** __myaes_utility.__init__(..) ******************************')
        logging.basicConfig(filename='my_aes.log',
                            format='%(message)s',
                            encoding='utf-8', level=logging.DEBUG)


    def encode_block(self, block_bytes):
        assert len(block_bytes) == 16
        assert self.numBits in [128, 192, 256]    

        keyScheduler = KeyScheduler([self.key_bytes[0:4], self.key_bytes[4:8], self.key_bytes[8:12], self.key_bytes[12:16]], self.numBits)

        # TODO - add this as a constant to State class?
        mixColMatrix = State(b'\x02\x01\x01\x03\x03\x02\x01\x01\x01\x03\x02\x01\x01\x01\x03\x02')

        state = State(block_bytes)
        logging.info('round[{}].input {}'.format(0, state))
        roundKey = keyScheduler.getRoundKey(0)
        logging.info('round[{}].ik_sch {}'.format(0, binascii.hexlify(roundKey)))
        state.addRoundKey(roundKey)
        logging.info('')

        for round in range(1,11):
            # logging.warning('Round sth {}'.format(round))
            logging.info('round[{}].istart {}'.format(round, state))
            state.SubBytes()
            logging.info('round[{}].is_box {}'.format(round, state))
            state.ShiftRows()
            logging.info('round[{}].is_row {}'.format(round, state))
            if round < 10:
                if round == 9:
                    print('DFA normal state[9] = {}'.format(state))
                    print(state.pretty_print())
                    # Inject fault
                    # state.matrix[0][0] = state.matrix[0][0] + GfByte(0x01)
                    print('DFA faulty state[9] = {}'.format(state))
                    print(state.pretty_print())
                state.MixColumns(mixColMatrix)
                logging.info('round[{}].im_col {}'.format(round, state))
            roundKey = keyScheduler.getRoundKey(round)
            logging.info('round[{}].ik_sch {}'.format(round, binascii.hexlify(roundKey)))
            state.addRoundKey(roundKey)
            logging.info('')

        print('Returning ciphertext: ')
        print(state.pretty_print())
        return state.getBytes()


    def decode_block(self, block_bytes):
        assert len(block_bytes) == 16
        assert self.numBits in [128, 192, 256]    

        keyScheduler = KeyScheduler([self.key_bytes[0:4], self.key_bytes[4:8], self.key_bytes[8:12], self.key_bytes[12:16]], self.numBits)

        # TODO - add this as a constant to State class?

        m2 = "0e090d0b0b0e090d0d0b0e09090d0b0e"
        m2_int = int(m2, 16)
        m2_bytes = m2_int.to_bytes(16, 'big', signed=False)
        invMixColMatrix = State(m2_bytes)

        # invMixColMatrix = State(b'\x14\x09\x13\x11\x11\x14\x09\x13\x13\x11\x14\x09\x09\x13\x11\x14')

        state = State(block_bytes)
        roundKey = keyScheduler.getInverseRoundKey(0)
        state.addRoundKey(roundKey)

        for round in range(1,11):
            print('round[{}].istart {}'.format(round, state))
            state.InvSubBytes()
            print('round[{}].is_box {}'.format(round, state))
            state.InvShiftRows()
            print('round[{}].is_row {}'.format(round, state))
            if round < 10:
                state.MixColumns(invMixColMatrix)
                print('round[{}].im_col {}'.format(round, state))
            # roundKey = keyScheduler.getRoundKey(10 - round)
            roundKey = keyScheduler.getInverseRoundKey(round)
            print('round[{}].ik_sch {}'.format(round, binascii.hexlify(roundKey)))
            state.addRoundKey(roundKey)   
            print()

        return state.getBytes()
 
    def encode_cbc(self, plaintext):
        length = len(plaintext)
        num_blocks = length//16
        print('length={}, num_blocks = {}'.format(length, num_blocks))

        result = '72ab5aabc347e1daba8c3cb45660760b4b00155a5c0340d7488423c84832e6b3'
        return binascii.unhexlify(result)
