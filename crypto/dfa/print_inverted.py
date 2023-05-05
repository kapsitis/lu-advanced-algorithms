from GF8 import *

def invert(arg):
    ZERO = GF8(0)
    ONE = GF8(1)
    if arg == ZERO:
        return ZERO
    for i in range(1, 256):
        x = GF8(i)
        if arg*x == ONE:
            return x
    print("XXXX: Cannot invert: {}".format(arg))
    return ONE


def main():
    print('[')
    for i in range(16):
        line = []
        print('[', end='')
        for j in range(16):
            num = 16*i + j
            numGF = invert(GF8(num))
            #numGF = GF8(num).inv()
            st = '{}'.format(numGF)
            line.append(st)
            if j < 15:
                print(st, end=", ")
            else:
                print(st, end="")
        print("], ")
    print("]")

if __name__ == '__main__':
    main()