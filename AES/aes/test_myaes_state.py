import pytest

from myaes_state import *
from myaes_key_sch import *

import binascii


def test_mix_columns_matrices():
    m1 = "02010103030201010103020101010302"
    m2 = "0e090d0b0b0e090d0d0b0e09090d0b0e"
    m1_int = int(m1, 16)
    m1_bytes = m1_int.to_bytes(16, 'big', signed=False)
    m2_int = int(m2, 16)
    m2_bytes = m2_int.to_bytes(16, 'big', signed=False)

    state_m1 = State(m1_bytes)
    state_m2 = State(m2_bytes)
    assert binascii.hexlify(state_m1.getBytes()).decode('utf-8') == "02010103030201010103020101010302"

    state_m1.MixColumns(state_m2)
    assert binascii.hexlify(state_m1.getBytes()).decode('utf-8') == "01000000000100000000010000000001"


def test_aes128_encrypt_round0():
    input_hex = "00112233445566778899aabbccddeeff"
    round_hex = "000102030405060708090a0b0c0d0e0f"
    expected_hex = "00102030405060708090a0b0c0d0e0f0"

    input_int = int(input_hex, 16)
    input_bytes = input_int.to_bytes(16, 'big', signed = False)
    round_int = int(round_hex, 16)
    round_bytes = round_int.to_bytes(16, 'big', signed = False)
    expected_int = int(expected_hex, 16)
    expected_bytes = expected_int.to_bytes(16, 'big', signed = False)

    s1 = State(input_bytes)
    s1.addRoundKey(round_bytes)
    assert s1.getBytes() == expected_bytes



def test_aes128_encrypt_roundNN():
    expected = [
        {
            'start': '00112233445566778899aabbccddeeff', 
            'k_sch': '000102030405060708090a0b0c0d0e0f'
        },         
        {
            'start': '00102030405060708090a0b0c0d0e0f0', 
            's_box': '63cab7040953d051cd60e0e7ba70e18c', 
            's_row': '6353e08c0960e104cd70b751bacad0e7',
            'm_col': '5f72641557f5bc92f7be3b291db9f91a',
            'k_sch': 'd6aa74fdd2af72fadaa678f1d6ab76fe'
        }, 
        {
            'start': '89d810e8855ace682d1843d8cb128fe4', 
            's_box': 'a761ca9b97be8b45d8ad1a611fc97369', 
            's_row': 'a7be1a6997ad739bd8c9ca451f618b61',
            'm_col': 'ff87968431d86a51645151fa773ad009',
            'k_sch': 'b692cf0b643dbdf1be9bc5006830b3fe'
        }
    ]

    startState_hex = '00102030405060708090a0b0c0d0e0f0'
    startState_int = int(startState_hex, 16)
    startState_bytes = startState_int.to_bytes(16, 'big', signed=False)
    mixColMatrix = State(b'\x02\x01\x01\x03\x03\x02\x01\x01\x01\x03\x02\x01\x01\x01\x03\x02')

    key_hex = "000102030405060708090a0b0c0d0e0f"
    key_int = int(key_hex, 16)
    key_bytes = key_int.to_bytes(16, 'big', signed = False)
    numBits = 128
    keyScheduler = KeyScheduler([key_bytes[0:4], key_bytes[4:8], key_bytes[8:12], key_bytes[12:16]], numBits)

    state = State(startState_bytes)
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected[1]['start']
    state.SubBytes()
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected[1]['s_box']
    state.ShiftRows()
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected[1]['s_row']
    state.MixColumns(mixColMatrix)
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected[1]['m_col']
    roundKey = keyScheduler.getRoundKey(1)
    assert binascii.hexlify(roundKey).decode('utf-8') == expected[1]['k_sch']

    state.addRoundKey(roundKey)
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected[2]['start']
    state.SubBytes()
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected[2]['s_box']
    state.ShiftRows()
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected[2]['s_row']
    state.MixColumns(mixColMatrix)
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected[2]['m_col']
    roundKey = keyScheduler.getRoundKey(2)
    assert binascii.hexlify(roundKey).decode('utf-8') == expected[2]['k_sch']


def test_aes128_encrypt_round10():
    expected10 = {
        'start': 'bd6e7c3df2b5779e0b61216e8b10b689', 
        's_box': '7a9f102789d5f50b2beffd9f3dca4ea7', 
        's_row': '7ad5fda789ef4e272bca100b3d9ff59f',
        'k_sch': '13111d7fe3944a17f307a78b4d2b30c5'
    }
    expected_output = '69c4e0d86a7b0430d8cdb78070b4c55a'

    startState_hex = expected10['start']
    startState_int = int(startState_hex, 16)
    startState_bytes = startState_int.to_bytes(16, 'big', signed=False)
    mixColMatrix = State(b'\x02\x01\x01\x03\x03\x02\x01\x01\x01\x03\x02\x01\x01\x01\x03\x02')

    key_hex = '000102030405060708090a0b0c0d0e0f'
    key_int = int(key_hex, 16)
    key_bytes = key_int.to_bytes(16, 'big', signed = False)
    numBits = 128
    keyScheduler = KeyScheduler([key_bytes[0:4], key_bytes[4:8], key_bytes[8:12], key_bytes[12:16]], numBits)

    state = State(startState_bytes)
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected10['start']
    state.SubBytes()
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected10['s_box']
    state.ShiftRows()
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected10['s_row']
    roundKey = keyScheduler.getRoundKey(10)
    assert binascii.hexlify(roundKey).decode('utf-8') == expected10['k_sch']
    state.addRoundKey(roundKey)
    assert binascii.hexlify(state.getBytes()).decode('utf-8') == expected_output



def test_modified_decryption_keys():
    m2 = "0e090d0b0b0e090d0d0b0e09090d0b0e"
    m2_int = int(m2, 16)
    m2_bytes = m2_int.to_bytes(16, 'big', signed=False)
    invMatrix = State(m2_bytes)

    print("Before InvMixColumns matrix is applied")    
    roundkey09_hex = "549932d1f08557681093ed9cbe2c974e"
    roundkey09_int = int(roundkey09_hex, 16)
    roundkey09_bytes = roundkey09_int.to_bytes(16, 'big', signed=False)
    s1 = State(roundkey09_bytes)
    print("s1 = {}".format(s1))    

    print("After InvMixColumns matrix is applied")
    s1.MixColumns(invMatrix)
    print("s1 = {}".format(s1)) 
    print("Done")



def test_mix_columns_matrices():
    m1 = "02010103030201010103020101010302"
    m2 = "0e090d0b0b0e090d0d0b0e09090d0b0e"
    m1_int = int(m1, 16)
    m1_bytes = m1_int.to_bytes(16, 'big', signed=False)
    m2_int = int(m2, 16)
    m2_bytes = m2_int.to_bytes(16, 'big', signed=False)

    state_m1 = State(m1_bytes)
    state_m2 = State(m2_bytes)
    assert binascii.hexlify(state_m1.getBytes()).decode('utf-8') == "02010103030201010103020101010302"

    state_m1.MixColumns(state_m2)
    assert binascii.hexlify(state_m1.getBytes()).decode('utf-8') == "01000000000100000000010000000001"

