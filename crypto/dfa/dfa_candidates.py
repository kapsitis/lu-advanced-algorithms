from GF8 import *
import time


class DFAcand:
    def __init__(self, normal_output):
        self.out = normal_output
        # Two faults per each column (faults only insert into row = 0).
        self.fouts = [[] * 256, [] * 256, [] * 256, [] * 256]
        # For the given fault we store 4 dictionaries:
        self.feasible_y = [dict(), dict(), dict(), dict()]

    def set_fault(self, col, value):
        if len(self.fouts[col]) < 2:
            if not value in self.fouts[col]:
                self.fouts[col].append(value)

    def print(self):
        print('DFAcand(out = {}, fouts = {})'.format(self.out, self.fouts))

    # Assume that col == 0
    # Z is the "X+A" value that we are currently testing
    # col - which column receives fault before the last MixColumns (it's always the top row)
    # num - which fault in this column is it (multiple faults add 0x01, 0x02 or possibly even more)
    # offset - which output byte is analyzed (0-15). For col = 0 we analyze offsets [0,7,10,13]
    # ZLIST - which ZLIST values were feasible so far.
    def filter_zlist(self, col, num, offset, ZLIST):
        if col < 0 or col >= 1:  # need "4" instead of "1"
            raise ValueError("Only col=0,1,2,3 are supported")
        left = 2 * offset
        right = 2 * offset + 2
        OO = GF8(self.out[left:right]) + GF8(self.fouts[col][num][left:right])
        new_zlist = []
        for Z in ZLIST:
            Z_MUL = Z
            if offset == 0:
                Z_MUL = GF8(0x02) * Z
            elif offset == 7:
                Z_MUL = GF8(0x03) * Z
            valid_ylist = list([GF8(z) for z in range(256)])
            for Yi in valid_ylist:
                if OO == Yi.sbox() + (Yi + Z_MUL).sbox():
                    if len(new_zlist) == 0 or new_zlist[-1] != Z:
                        new_zlist.append(Z)
                    if not Z in self.feasible_y[col]:
                        self.feasible_y[col][Z] = [[], [], [], []]
                    self.feasible_y[col][Z][offset // 4].append(Yi)

        return new_zlist


def main():
    start_time = time.time()

    cand = DFAcand('e80027fcb3f4107706845341cc1d371c')
    cand.set_fault(0, 'fa0027fcb3f410ab0684c241ccf7371c')
    cand.set_fault(0, 'c80027fcb3f4100f06840741ccba371c')
    offsets = [0, 7, 10, 13]

    # Will make faults in all columns (but for now just COL = 0).
    for COL in range(1):
        # We c
        FEASIBLE_Y = []
    # Will store feasible Y_i for all rows (one list of sets is for Y0, next for Y1, etc.)
    All_Sets_Y = [[], [], [], []]
    # Visit all faults for that column:
    for num in range(0, 2):
        # 4 separate dictionaries to cover all 4 offsets in that column
        cand.feasible_y = [dict(), dict(), dict(), dict()]
        # For the given fault and the given offset, compute feasible values of Z
        ZLIST = [GF8(i) for i in range(256)]
        for offset in offsets:
            ZLIST = cand.filter_zlist(COL, num, offset, ZLIST)
            # For increasing offsets this list is filtered down.
            print('ZLIST = {}'.format(ZLIST))
        FEASIBLE_Y.append(cand.feasible_y)

        for row in range(4):
            all_bytes_y = []
            dd = cand.feasible_y[row]
            # Iterate over all Z having at least one feasible Y in every row/offset
            for Z in cand.feasible_y[row]:
                if dd[Z][0] != [] and dd[Z][1] != [] and dd[Z][2] != [] and dd[Z][3] != []:
                    all_bytes_y += dd[Z][row]
            All_Sets_Y[row].append(set(all_bytes_y))

    print("All_Sets_Y = {}".format(All_Sets_Y))

    Set_Y = []
    for row in range(4):
        Set_Y.append(set([GF8(Yi) for Yi in range(256)]))
        for Set_i in All_Sets_Y[row]:
            Set_Y[row] = Set_Y[row].intersection(Set_i)
        print('Set_Y[{}] = {}'.format(row, Set_Y[row]))


    end_time = time.time()
    print('--- {:.3f} seconds ---'.format(end_time - start_time))


    # print(FEASIBLE_Y)




if __name__ == '__main__':
    main()
