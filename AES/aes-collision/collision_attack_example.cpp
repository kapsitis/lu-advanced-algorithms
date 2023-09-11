#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fstream>
#include <vector>

#include "collision_attack.h"

#define ATTACK_FROM_OUTPUT 0

using namespace std;

static const unsigned char Sbox[256] = {
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
};

void ExpandKey(const unsigned char* key, unsigned char* expanded_key)
{
    memcpy(expanded_key, key, 16);

    unsigned char rCon[10] = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36 };
    for (unsigned int i = 16; i < 16 * 11; i += 16)
    {
        expanded_key[i + 0] = expanded_key[(i - 16) + 0] ^ Sbox[expanded_key[(i - 4) + 1]] ^ rCon[(i / 16) - 1];
        expanded_key[i + 1] = expanded_key[(i - 16) + 1] ^ Sbox[expanded_key[(i - 4) + 2]];
        expanded_key[i + 2] = expanded_key[(i - 16) + 2] ^ Sbox[expanded_key[(i - 4) + 3]];
        expanded_key[i + 3] = expanded_key[(i - 16) + 3] ^ Sbox[expanded_key[(i - 4) + 0]];

        expanded_key[i + 4] = expanded_key[(i - 16) + 4] ^ expanded_key[i + 0];
        expanded_key[i + 5] = expanded_key[(i - 16) + 5] ^ expanded_key[i + 1];
        expanded_key[i + 6] = expanded_key[(i - 16) + 6] ^ expanded_key[i + 2];
        expanded_key[i + 7] = expanded_key[(i - 16) + 7] ^ expanded_key[i + 3];

        expanded_key[i +  8] = expanded_key[(i - 16) +  8] ^ expanded_key[i + 4];
        expanded_key[i +  9] = expanded_key[(i - 16) +  9] ^ expanded_key[i + 5];
        expanded_key[i + 10] = expanded_key[(i - 16) + 10] ^ expanded_key[i + 6];
        expanded_key[i + 11] = expanded_key[(i - 16) + 11] ^ expanded_key[i + 7];

        expanded_key[i + 12] = expanded_key[(i - 16) + 12] ^ expanded_key[i +  8];
        expanded_key[i + 13] = expanded_key[(i - 16) + 13] ^ expanded_key[i +  9];
        expanded_key[i + 14] = expanded_key[(i - 16) + 14] ^ expanded_key[i + 10];
        expanded_key[i + 15] = expanded_key[(i - 16) + 15] ^ expanded_key[i + 11];
    }
}
template<class T> static void AddRoundKey(T* state, T* key)
{
    for (unsigned i = 0; i < 16; i++)
        state[i] ^= key[i];
}
template<class T> void ShiftRows(T* state)
{
    T shifted_state[16];
    // 0 row
    shifted_state[ 0] = Sbox[state[ 0]];
    shifted_state[ 4] = Sbox[state[ 4]];
    shifted_state[ 8] = Sbox[state[ 8]];
    shifted_state[12] = Sbox[state[12]];
    // 1 row
    shifted_state[ 1] = Sbox[state[ 5]];
    shifted_state[ 5] = Sbox[state[ 9]];
    shifted_state[ 9] = Sbox[state[13]];
    shifted_state[13] = Sbox[state[ 1]];
    // 2 row
    shifted_state[ 2] = Sbox[state[10]];
    shifted_state[ 6] = Sbox[state[14]];
    shifted_state[10] = Sbox[state[ 2]];
    shifted_state[14] = Sbox[state[ 6]];
    // 3 row
    shifted_state[ 3] = Sbox[state[15]];
    shifted_state[ 7] = Sbox[state[ 3]];
    shifted_state[11] = Sbox[state[ 7]];
    shifted_state[15] = Sbox[state[11]];
    memcpy(state, shifted_state, sizeof(shifted_state));
}
template<class T> T GfMul(T x, unsigned char y)
{
    T tmp = x;
    T res = 0;
    if ((y & 1) != 0)
        res ^= tmp;
    if ((y & 2) != 0) {
        tmp <<= 1;
        if (x >= (1 << 7)) {
            tmp ^= (283); // 283 = 0b100011011
        }
        res ^= tmp;
    }
    return res;
}
template<class T> void MixColumn(T* column)
{
    T result[4];
    result[0] = GfMul(column[0], 2) ^ GfMul(column[1], 3) ^ column[2] ^ column[3];
    result[1] = column[0] ^ GfMul(column[1], 2) ^ GfMul(column[2], 3) ^ column[3];
    result[2] = column[0] ^ column[1] ^ GfMul(column[2], 2) ^ GfMul(column[3], 3);
    result[3] = GfMul(column[0], 3) ^ column[1] ^ column[2] ^ GfMul(column[3], 2);
    memcpy(column, result, sizeof(result));
}
template<class T> void MixColumns(T* state)
{
    MixColumn(state +  0);
    MixColumn(state +  4);
    MixColumn(state +  8);
    MixColumn(state + 12);
}
template <class T> void PlainAesEncrypt(const T* input, const unsigned char* key, T* output)
{
    unsigned char tmp[11 * 16];
    ExpandKey(key, tmp);
    T expanded_key[11 * 16];
    for (unsigned int i = 0; i < 11 * 16; i++)
        expanded_key[i] = tmp[i];

    T state[16];
    memcpy(state, input, sizeof(state));

    AddRoundKey(state, expanded_key);

    for (unsigned int i = 0; i < 9; i++)
    {
#if !ATTACK_FROM_OUTPUT
        if (i == 1)
        {
            for (int j = 0; j < 16; j++)
            {
                collision_attack::add_to_trace(state[j]);
            }
        }
#endif

        ShiftRows(state);

#if ATTACK_FROM_OUTPUT
        if (i == 8)
        {
            for (int j = 0; j < 16; j++)
            {
                collision_attack::add_to_trace(state[j]);
            }
        }
#endif

        MixColumns(state);
        AddRoundKey(state, expanded_key + 16 + 16 * i);
    }

    ShiftRows(state);
    AddRoundKey(state, expanded_key + 160);
    memcpy(output, state, sizeof(state));
}

//////////////////// PLEASE DO NOT MODIFY THIS /////////////////////////////
unsigned char hex(char c) {
    if (c >= '0' && c <= '9') return (c - '0');
    if (c == 'a' || c == 'A') return 10;
    if (c == 'b' || c == 'B') return 11;
    if (c == 'c' || c == 'C') return 12;
    if (c == 'd' || c == 'D') return 13;
    if (c == 'e' || c == 'E') return 14;
    if (c == 'f' || c == 'F') return 15;
    return 0;
}

//////////////////// PLEASE DO NOT MODIFY THIS /////////////////////////////
void hex_to_16bytes(const char* argv, unsigned char* out, bool print = true) {
    unsigned len = strlen(argv);
    unsigned char buffer[33];
    buffer[32] = 0;
    for (int i = 0; i < 32; i++) {
        if (len >= 32) 
            buffer[i] = argv[(len-32)+i];
        else
            if (32 - len > i)
                buffer[i] = '0';
            else
                buffer[i] = argv[i-(32-len)];
    }
    //printf("[%s] len=%lu\n", buffer, strlen((const char*)buffer));
    for (int i = 0; i < 16; i++) {
        out[i] = hex(buffer[i*2]) * 16 + hex(buffer[i*2+1]);
        if (print) printf("%02x ", out[i]);
    }
    if (print) printf("\n");
}

int main(int argc, char**argv) {
    unsigned char key[16], in[16], out[16];

    if (argc != 3) {
        printf("usage: %s key_hex number_of_traces\n", argv[0]);
        return 1;
    }

    hex_to_16bytes(argv[1], key);

    srand(42);

    collision_attack::init();

    int K = atoi(argv[2]);

    for (int j = 0; j < K; j++) {
        vector<int> aes_input;
        for (int i = 0; i < 16; i++) {
            in[i] = rand() & 0xFF;
            aes_input.push_back(in[i]);
        }

        collision_attack::start_new_trace(aes_input);

        PlainAesEncrypt(in, key, out);

        collision_attack::finish_trace(vector<int>(out, out + 16));
    }

#if ATTACK_FROM_OUTPUT
    auto result = collision_attack::run_from_output();
#else
    auto result = collision_attack::run_from_input();
#endif

    printf("\nKey: ");
    for (int x : result) printf("%02X", x);
    printf("\n");

    return 0;
}
