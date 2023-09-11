import os
import sys

import aes_reference

from myaes_gfbyte import *
from myaes_key_sch import *
from myaes_state import *

import binascii

class AesTracer: 
    def __init__(self, file_name, is_verbose):
        self.file_name = file_name
        self.state_vectors = []
        self.column_names = []
        self.all_blocks = []
        self.is_verbose = is_verbose


    def delete_file(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    # Reset state to prepare for next block of 256 encryptions
    def reset(self): 
        self.state_vectors = []
        self.all_blocks = []

    # def set_block(self, block):
    #     self.block = block

    
    # Write state vectors to a file
    def to_file(self):
        with open(self.file_name, 'a') as file_object:
            if self.is_verbose:
                file_object.write('{:<34}'.format('block'))
                for col in self.column_names: 
                    file_object.write('{:<33}'.format(col))
                file_object.write('\n')

            # Write out traces (typically a batch of 256)
            for i in range(len(self.state_vectors)):
                if self.is_verbose:
                    file_object.write(self.all_blocks[i])
                    file_object.write(': ')

                message = ' '.join(self.state_vectors[i])
                file_object.write(message)
                file_object.write('\n')

    # Return all 256 vectors (length 40 each - containing 16-byte blocks in hex notation)
    def get_vectors(self):
        return self.state_vectors


    # The input of 16 GfByte values - in column major order.
    @staticmethod
    def shift_rows(state):
        result = []
        for col in range(4):
            for row in range(4):
                new_col = (col + row) % 4
                result.append(state[4*new_col + row])
        return result

    # encode and record
    def record(self,block_hex, key_hex):
        self.column_names = []
        self.all_blocks.append(block_hex)
        numBits = 128

        block_int = int(block_hex, 16)
        block_bytes = block_int.to_bytes(16, 'big', signed = False)
        key_int = int(key_hex, 16)
        key_bytes = key_int.to_bytes(16, 'big', signed = False)

        assert numBits in [128, 192, 256]    
        assert len(block_bytes) == 16
        assert len(key_bytes) == numBits//8

        keyScheduler = KeyScheduler([key_bytes[0:4], key_bytes[4:8], key_bytes[8:12], key_bytes[12:16]], numBits)

        mixColMatrix = State(b'\x02\x01\x01\x03\x03\x02\x01\x01\x01\x03\x02\x01\x01\x01\x03\x02')

        state = State(block_bytes)
        roundKey = keyScheduler.getRoundKey(0)
        state.addRoundKey(roundKey)

        current_vector = []
        for round in range(1,11):
            # self.stateVectors.record(round, 'start', state)
            current_vector.append('{}'.format(state))
            self.column_names.append('round[{}].{}'.format(round, 'start'))


            state.SubBytes()
            # self.stateVectors.record(round, 's_box', state)
            current_vector.append('{}'.format(state))
            self.column_names.append('round[{}].{}'.format(round, 's_box'))


            state.ShiftRows()
            # self.stateVectors.record(round, 's_row', state)
            current_vector.append('{}'.format(state))
            self.column_names.append('round[{}].{}'.format(round, 's_row'))

            if round < 10:
                state.MixColumns(mixColMatrix)
                # self.stateVectors.record(round, 'm_col', state)
                current_vector.append('{}'.format(state))
                self.column_names.append('round[{}].{}'.format(round, 'm_col'))

            roundKey = keyScheduler.getRoundKey(round)
            # print('round[{}].k_sch {}'.format(round, binascii.hexlify(roundKey)))
            state.addRoundKey(roundKey)    

        # self.stateVectors.record(10, 'output', state)
        current_vector.append('{}'.format(state))
        self.column_names.append('round[{}].{}'.format(round, 'output'))

        # print("******************* CALL CRYPTO API ************************")
    
        # key_int = int(key_hex, 16)
        # ciphertext = aes_reference.aes128_encrypt_block(block_int, key_int)
        # print('type(ciphertext) = {}'.format(type(ciphertext)))
        # print(binascii.hexlify(ciphertext).upper())
        # print('ciphertext = {}'.format(ciphertext.hex()))
        # print('expected   = {}'.format(expected_output_hex))

        # return self.stateVectors.get_vectors()
        self.state_vectors.append(current_vector)


if __name__ == '__main__':
    block_hex = "00112233445566778899aabbccddeeff"
    key_hex = "000102030405060708090a0b0c0d0e0f"
    # expected_output_hex = "69c4e0d86a7b0430d8cdb78070b4c55a"

    aesTracer = AesTracer('../dca/input.txt', True)
    aesTracer.delete_file()

    aesTracer.record(block_hex, key_hex)
    aesTracer.record("00000000000000000000000000000000", key_hex)

    aesTracer.to_file()


