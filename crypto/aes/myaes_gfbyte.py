import binascii

# Initialize with integers in range [0;255]. May need to change to 'bytes' or something else. 
# See https://stackoverflow.com/questions/41274864/declaring-a-single-byte-variable-in-python for options
class GfByte:
    def __init__(self, b=0):
        # print('arg type in gfbyte is {}'.format(type(b)))
        assert isinstance(b, int)
        self.b = b

    def __str__(self):
        hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        return "{}{}.".format(hex[self.b//16], hex[self.b%16])

    def __repr__(self):
        return "({})".format(self.b)

    def getB(self):
        return self.b.to_bytes(1, 'big', signed = False)

    def __add__(self, other):
        #print('other type is {}'.format(type(other)))
        #print('other = {}'.format(other))
        assert isinstance(other, GfByte)
        x = self.b ^ other.b
        return GfByte(x)

    def __sub__(self, other):
        x = self.b ^ other.b
        return GfByte(x)

         
    def __mul__(self, other):
        bit_masks = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        total = 0
        for i in range(8):
            if self.b & bit_masks[i] != 0:
                total = total ^ (other.b << i)        
        reduction = 0x011B
        extended_masks = [0x4000, 0x2000, 0x1000, 0x0800, 0x0400, 0x0200, 0x0100]
        for i in range(len(extended_masks)):
            if total & extended_masks[i] != 0:
                total = total ^ (reduction << (6 - i))
        return GfByte(total)


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.b == other.b
        else:
            return False

    def __hash__(self):
        return hash(self.b)

    def __ne__(self, other):
        return not self.__eq__(other)


    def inverse(self):
        ZERO = GfByte(0)
        ONE = GfByte(1)
        if self == ZERO:
            return ZERO
        for i in range(1, 256):
            x = GfByte(i)
            if self*x == ONE:
                return x
        print("XXXX: Cannot invert: {}".format(self))
        return ONE


    def leftRotate(self, d):
        return GfByte(((self.b << d) | (self.b >> (8 - d))) & 0xFF)

    def sbox(self):
        bb = self.inverse()
        result = bb + bb.leftRotate(1) + bb.leftRotate(2) + bb.leftRotate(3) + bb.leftRotate(4) + GfByte(0x63)
        # print("self = {}, bb = {}, sbox = {}".format(self, bb, result))
        return result

    def inv_sbox(self):
        bb = self.leftRotate(1) + self.leftRotate(3) + self.leftRotate(6) + GfByte(0x05)
        result = bb.inverse()
        # print("self = {}, bb = {}, sbox = {}".format(self, bb, result))
        return result

# if __name__ == '__main__':
# #    a = GfByte(0xb8)
# #    cc = a.s_box()
#     a = GfByte(0xb8)
#     cc = a.inv_sbox()
#     expected = GfByte(0x9a)
#     print("a = {}, cc = {}, expected = {}".format(a, cc, expected))

#     for i in range(10):
#         ii = GfByte(i)
#         jj = ii.inverse()
#         print("ii = {}, jj = {}".format(ii, jj))