#include <vector>
#include <cassert>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <tuple>

#include "collision_attack_core.h"

namespace AES {
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

    void ExpandKey(const std::vector<int>& key, unsigned char* expanded_key)
    {
        for (int i = 0; i < 16; i++) expanded_key[i] = key[i];

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

    std::vector<int> encrypt(const std::vector<int>& input, const std::vector<int>& key) {
        unsigned char expanded_key[11 * 16];
        ExpandKey(key, expanded_key);

        unsigned char state[16];
        for (int i = 0; i < 16; i++) state[i] = input[i];

        AddRoundKey(state, expanded_key);

        for (unsigned int i = 0; i < 9; i++) {
            ShiftRows(state);

            MixColumns(state);
            AddRoundKey(state, expanded_key + 16 + 16 * i);
        }

        ShiftRows(state);
        AddRoundKey(state, expanded_key + 160);

        std::vector<int> output(16);
        for (int i = 0; i < 16; i++) output[i] = state[i];

        return output;
    }
}

namespace collision_attack {
    std::vector<std::tuple<std::vector<int>, std::vector<int>, std::vector<int>>> traces(1);

    void add_to_trace(int x) {
        std::get<2>(traces.back()).push_back(x);
    }

    void init() {
        traces.clear();
    }

    void start_new_trace(const std::vector<int>& aes_input) {
        traces.emplace_back();
        std::get<0>(traces.back()) = aes_input;
    }

    void finish_trace(const std::vector<int>& aes_output) {
        std::get<1>(traces.back()) = aes_output;
    }

    std::vector<int> run_from_input() {
        std::vector<std::vector<int>> subkey_candidates[4];
        for (int diag = 0; diag < 4; diag++) {
            int e0 = ( 0 + 4 * diag) % 16;
            int e1 = ( 5 + 4 * diag) % 16;
            int e2 = (10 + 4 * diag) % 16;
            int e3 = (15 + 4 * diag) % 16;

            std::vector<std::pair<uint32_t, uint64_t>> data;
            for (auto& t : traces) {
                uint32_t x0 = std::get<0>(t)[e0];
                uint32_t x1 = std::get<0>(t)[e1];
                uint32_t x2 = std::get<0>(t)[e2];
                uint32_t x3 = std::get<0>(t)[e3];

                data.emplace_back(x0 + (x1 << 8) + (x2 << 16) + (x3 << 24), std::get<2>(t)[e0]);
            }

            std::fprintf(stderr, "\nProcessing subkey #%d\n", diag);

            auto result = run(data, 999, 1, false);

            for (int k = 2; result.empty(); k *= 2) {
                result = run(data, 999, k, false);
            }

            for (auto& cand : result) {
                if (cand.first == result.front().first) {
                    std::vector<int> subkey(16, 0);
                    uint32_t mask = cand.second;
                    subkey[e0] = mask & 0xFF;
                    subkey[e1] = (mask >> 8) & 0xFF;
                    subkey[e2] = (mask >> 16) & 0xFF;
                    subkey[e3] = (mask >> 24) & 0xFF;

                    subkey_candidates[diag].push_back(subkey);
                }
            }
        }

        size_t cand_cnt = 1;
        for (int i = 0; i < 4; i++) {
            cand_cnt *= subkey_candidates[i].size();
        }

        std::fprintf(stderr, "\nBrute-forcing %zu candidates\n", cand_cnt);

        for (auto& subkey0 : subkey_candidates[0])
            for (auto& subkey1 : subkey_candidates[1])
                for (auto& subkey2 : subkey_candidates[2])
                    for (auto& subkey3 : subkey_candidates[3]) {
                        std::vector<int> key(16);
                        for (auto& subkey : {subkey0, subkey1, subkey2, subkey3})
                            for (int i = 0; i < 16; i++) {
                                key[i] += subkey[i];
                            }

                        bool ok = true;
                        for (auto& tr : traces) {
                            auto& inp = std::get<0>(tr);
                            auto& out = std::get<1>(tr);

                            ok = ok && AES::encrypt(inp, key) == out;
                        }

                        if (ok) {
                            return key;
                        }
                    }

        return {};
    }

    void process_last_round_key(std::vector<int>& key)
    {
        for (uint8_t rCon : { 0x36, 0x1b, 0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01 }) {
            for (int i = 15; i >= 4; i--) {
                key[i] ^= key[i - 4];
            }

            for (int i = 0; i < 4; i++) {
                key[i] ^= Sbox1[key[12 + ((i + 1) & 3)]];
            }

            key[0] ^= rCon;
        }
    }

    std::vector<int> run_from_output() {
        std::vector<int> key(16, -1);
        for (int diag = 0; diag < 4; diag++) {
            int e0 = ( 0 + 4 * diag) % 16;
            int e1 = (13 + 4 * diag) % 16;
            int e2 = (10 + 4 * diag) % 16;
            int e3 = ( 7 + 4 * diag) % 16;

            std::vector<std::pair<uint32_t, uint64_t>> data;
            for (auto& t : traces) {
                uint32_t x0 = std::get<1>(t)[e0];
                uint32_t x1 = std::get<1>(t)[e1];
                uint32_t x2 = std::get<1>(t)[e2];
                uint32_t x3 = std::get<1>(t)[e3];

                data.emplace_back(x0 + (x1 << 8) + (x2 << 16) + (x3 << 24), std::get<2>(t)[e0]);
            }

            std::fprintf(stderr, "\nProcessing subkey #%d\n", diag);

            auto result = run(data, 999, 1, true);

            assert(result.empty() == false);

            uint32_t mask = result.front().second;
            key[e0] = mask & 0xFF;
            key[e1] = (mask >> 8) & 0xFF;
            key[e2] = (mask >> 16) & 0xFF;
            key[e3] = (mask >> 24) & 0xFF;
        }

        process_last_round_key(key);

        return key;
    }
}
