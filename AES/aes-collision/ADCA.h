#include <array>
#include <bitset>
#include <vector>

namespace ADCA {
    using namespace std;

    template<size_t N>
    vector<bool> run(const array<bitset<N + 64>, N>& input,
                     const vector<bitset<N + 64>>& targets) {
        array<uint64_t, N + 64> base;
        bitset<N + 64> base_mask;
        auto basis = input;
        for (int i = 0; i < N; i++) {
            if (basis[i].none()) {
                continue;
            }

            int j = 0;
            while (basis[i][j] == false) {
                j++;
            }

            base[j] = i;
            base_mask.set(j);

            for (int k = 0; k < N; k++)
                if (basis[k][j] && k != i) {
                    basis[k] ^= basis[i];
                }
        }

        auto extract_control_bits = [&base_mask](const bitset<N + 64>& column) {
            uint64_t mask = 0;
            for (int i = 0, j = 0; j < 64; i++)
                if (base_mask[i] == false) {
                    mask ^= (uint64_t)(column[i] ? 1 : 0) << j;
                    j++;
                }

            return mask;
        };

        for (int i = 0, j = 0; i < N + 64; i++)
            if (base_mask[i]) {
                base[i] = extract_control_bits(basis[base[i]]);
            }

        vector<bool> results;
        for (auto& target : targets) {
            uint64_t control = extract_control_bits(target);
            for (int i = 0; i < N + 64; i++)
                if (target[i] && base_mask[i]) {
                    control ^= base[i];
                }

            results.push_back(control == 0);
        }

        return results;
    }
}
