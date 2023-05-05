from GF8 import *
import time


class DFAcand:
    def __init__(self, normal_output):
        self.out = normal_output
        # Two faults per each column (faults only insert into row = 0).
        self.fouts = [[] * 256, [] * 256, [] * 256, [] * 256]

        # For the given fault we store 4 dictionaries:
        # self.feasible_y = [dict(), dict(), dict(), dict()]

    def set_fault(self, col, value):
        if len(self.fouts[col]) < 2:
            if not value in self.fouts[col]:
                self.fouts[col].append(value)

    def print(self):
        print('DFAcand(out = {}, fouts = {})'.format(self.out, self.fouts))

    # col - which column receives fault before the last MixColumns (it's always the top row)
    # num - which fault in this column is it (multiple faults add 0x01, 0x02 or possibly even more)
    # offset - which output byte is analyzed (0-15). For col = 0 we analyze offsets [0,7,10,13]
    # ZLIST - which Z values to test

    # RETURN dictionary with feasible Z's and Yi's:
    # {z1: [[Y01,Y02],[Y11,Y12],[Y21,Y22],[Y31,Y32]], z2: [[Y01,Y02],[Y11,Y12],[Y21,Y22],[Y31,Y32]], ...}
    def filter_zlist(self, col, num, offset, ZLIST, PREV_DICT_LEVEL1):
        if col < 0 or col >= 1:  # need "4" instead of "1"
            raise ValueError("Only col=0,1,2,3 are supported")
        feasible_y_dict = dict()
        left = 2 * offset
        right = 2 * offset + 2
        OO = GF8(self.out[left:right]) + GF8(self.fouts[col][num][left:right])

        for Z in ZLIST:
            Z_MUL = Z
            if offset == 0:
                Z_MUL = GF8(0x02) * Z
            elif offset == 7:
                Z_MUL = GF8(0x03) * Z
            YLIST = list([GF8(z) for z in range(256)])
            for Yi in YLIST:
                if OO == Yi.sbox() + (Yi + Z_MUL).sbox():
                    if not Z in feasible_y_dict:
                        feasible_y_dict[Z] = [[], [], [], []]
                        for jj in range(offset // 4):
                            feasible_y_dict[Z][jj] += PREV_DICT_LEVEL1[Z][jj]
                    feasible_y_dict[Z][offset // 4].append(Yi)
        return feasible_y_dict

# Sample argument:
# dd = {0x01: [[0x5c, 0x5e], [0xdd, 0xde], [0x28, 0x29], [0x56, 0x57]], 0x02: [[0x40, 0x44], [], [], []], ... }
# Return a sorted list of those keys from dd which map to values containing 4 nonempty lists (or just the k-th nonempty list)
def feasible_z_keys(dd, k = -1):
    result = []
    for key, value in dd.items():
        if k == -1 and all(value[i] for i in range(4)):
            result.append(key)
        elif value[k]:
            result.append(key)
    return result


# Sample input:
# DD = [{0x01: [[0x5c, 0x5e], [0xdd, 0xde], [0x28, 0x29], [0x56, 0x57]],
#   0x1b: [[0xd5, 0xe3], [0x0b, 0x26], [0x64, 0x7f], [0x47, 0x5c]],
#   0x27: [[0x3a, 0x74], [0x35, 0x5c], [0x80, 0xa7], [0x4a, 0x6d]]},
# {0x02: [[0x58, 0x5c], [0xdb, 0xdd], [0x29, 0x2b], [0x55, 0x57]],
#    0x0a: [[0xc3, 0xd7], [0x22, 0x3c], [0x17, 0x1d], [0x22, 0x28]],
#    0x32: [[0x00, 0x1c, 0x64, 0x78], [0x8e, 0xd8], [0xd2, 0xe0], [0xdb, 0xe9]]}]
# Iterate over all key/value pairs `(k, [L1,L2,L3,L4])` in DD[0] and also over all
# `(kk, [LL1,LL2,LL3,LL4])` in DD[1], and build a list of 4-tuples:
# [(y1,y2,y3,y4),...] where `y1` belongs to the intersection of L1 and LL1, and so on.
def valid_overlap(DD):
    result = []
    dict1, dict2 = DD

    for k, [L1, L2, L3, L4] in dict1.items():
        for kk, [LL1, LL2, LL3, LL4] in dict2.items():
            intersect1 = list(set(L1) & set(LL1))
            intersect2 = list(set(L2) & set(LL2))
            intersect3 = list(set(L3) & set(LL3))
            intersect4 = list(set(L4) & set(LL4))

            if intersect1 and intersect2 and intersect3 and intersect4:
                result.append((intersect1[0], intersect2[0], intersect3[0], intersect4[0]))

    return result


def main():
    start_time = time.time()

    cand = DFAcand('e80027fcb3f4107706845341cc1d371c')
    cand.set_fault(0, 'fa0027fcb3f410ab0684c241ccf7371c')
    cand.set_fault(0, 'c80027fcb3f4100f06840741ccba371c')
    offsets = [[0, 7, 10, 13], [0, 7, 10, 13]]

    # Will make faults in all columns (but for now just COL = 0).
    Y_DICT_LEVEL3 = []
    for COL in range(1):
        Y_DICT_LEVEL2 = []
        # Visit all faults for that column:
        for num in range(0, len(cand.fouts[COL])):
            ZLIST = [GF8(i) for i in range(256)]
            Y_DICT_LEVEL1 = dict()
            for Z in ZLIST:
                Y_DICT_LEVEL1[Z] = [[], [], [], []]
            for idx, offset in enumerate(offsets[COL]):
                Y_DICT_LEVEL1 = cand.filter_zlist(COL, num, offset, ZLIST, Y_DICT_LEVEL1)
                ZLIST = feasible_z_keys(Y_DICT_LEVEL1, idx)
                print("ZLIST == {}".format(ZLIST))
                print("Y_DICT_LEVEL1 == {}".format(Y_DICT_LEVEL1))



            Y_DICT_LEVEL2.append(Y_DICT_LEVEL1)

        Y_DICT_LEVEL3.append(Y_DICT_LEVEL2)

    print("Y_DICT_LEVEL3 = {}".format(Y_DICT_LEVEL3))

    result = valid_overlap(Y_DICT_LEVEL3[0])

    print(result)

    the_key = "******** ******** ******** ********"
    for tuple4 in result:
        for idx, offset in enumerate([0,7,10,13]):
            left = 2 * offset
            right = 2 * offset + 2
            keybyte = GF8(cand.out[left:right]) - tuple4[idx].sbox()
            print("{}, {}".format(offset, keybyte))
            keybytestr = '{}'.format(keybyte)[2:]

            left2 = left + offset // 4
            right2 = right + offset // 4
            the_key = the_key[:left2] + keybytestr + the_key[right2:]
    print('the_key = {}'.format(the_key))

    end_time = time.time()
    print('--- {:.3f} seconds ---'.format(end_time - start_time))




if __name__ == '__main__':
    main()
