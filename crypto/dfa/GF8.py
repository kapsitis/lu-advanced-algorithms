# Consider a finite field GF(2^8) used for Rijndael MixColumns:
# All of its values are polynomials over GF(2), there is a reducing polynomial
# $R(x) = x^8 + x^4 + x^3 + x + 1$.
# Can you create a Python class `GF8.py` which can store the values of GF(2^8).
# It should have 3 different constructors (with a single argument of
# type `string`, `bytes`, `int` respectively).
# In particular these three calls:
# ```
# a = GF8('7F')
# b = GF8(b'7F')
# c = GF(0x7F)
# ```
# Should result in equal elements.


class GF8:
    def __init__(self, value):
        if isinstance(value, str):
            self.value = int(value, 16)
        elif isinstance(value, bytes):
            self.value = int.from_bytes(value, 'big')
        elif isinstance(value, int):
            self.value = value
        else:
            raise ValueError("Invalid input type. Must be str, bytes, or int.")

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, GF8) and self.value == other.value

    def __repr__(self):
        return f"0x{(self.value):02x}"

    # Implement the methods `__add__(self, other)`, `__sub__(self, other)` and `__mul__(self, other)`
    # to add, subtract or multiply the elements from this finite field - with proper reduction using the reducing polynomial
    # $R(x) = x^8 + x^4 + x^3 + x + 1$.

    def __add__(self, other):
        if not isinstance(other, GF8):
            raise ValueError("Invalid input type. Must be GF8.")
        return GF8(self.value ^ other.value)

    def __sub__(self, other):
        # Subtraction in finite fields is the same as addition
        return self.__add__(other)

    def __mul__(self, other):
        if not isinstance(other, GF8):
            raise ValueError("Invalid input type. Must be GF8.")

        a = self.value
        b = other.value
        result = 0

        for _ in range(8):
            result ^= a * (b & 1)
            b >>= 1
            a <<= 1

            # Check if reduction is needed
            if a & 0x100:
                a ^= 0x11b  # Reducing polynomial: x^8 + x^4 + x^3 + x + 1

        return GF8(result)

    # This method uses the Extended Euclidean Algorithm to find the inverse.
    # It first checks if the element has an inverse (i.e., is not zero).
    # The `extended_gcd` function computes the coefficients for the linear combination
    # of the input values, and we take the first coefficient modulo 256
    # as the multiplicative inverse. The result is returned as a new GF8 object.
    def bad_inverse(self):
        def extended_gcd(a, b):
            x, last_x = 0, 1
            y, last_y = 1, 0
            while b:
                quotient = a // b
                a, b = b, a % b
                x, last_x = last_x - quotient * x, x
                y, last_y = last_y - quotient * y, y
            return last_x, last_y

        if self.value == 0:
            raise ValueError("Element has no multiplicative inverse.")

        s, _ = extended_gcd(self.value, 0x11b)
        return GF8(s % 256)

    def inv(self):
        INV = [
            [0x00, 0x01, 0x8d, 0xf6, 0xcb, 0x52, 0x7b, 0xd1, 0xe8, 0x4f, 0x29, 0xc0, 0xb0, 0xe1, 0xe5, 0xc7],
            [0x74, 0xb4, 0xaa, 0x4b, 0x99, 0x2b, 0x60, 0x5f, 0x58, 0x3f, 0xfd, 0xcc, 0xff, 0x40, 0xee, 0xb2],
            [0x3a, 0x6e, 0x5a, 0xf1, 0x55, 0x4d, 0xa8, 0xc9, 0xc1, 0x0a, 0x98, 0x15, 0x30, 0x44, 0xa2, 0xc2],
            [0x2c, 0x45, 0x92, 0x6c, 0xf3, 0x39, 0x66, 0x42, 0xf2, 0x35, 0x20, 0x6f, 0x77, 0xbb, 0x59, 0x19],
            [0x1d, 0xfe, 0x37, 0x67, 0x2d, 0x31, 0xf5, 0x69, 0xa7, 0x64, 0xab, 0x13, 0x54, 0x25, 0xe9, 0x09],
            [0xed, 0x5c, 0x05, 0xca, 0x4c, 0x24, 0x87, 0xbf, 0x18, 0x3e, 0x22, 0xf0, 0x51, 0xec, 0x61, 0x17],
            [0x16, 0x5e, 0xaf, 0xd3, 0x49, 0xa6, 0x36, 0x43, 0xf4, 0x47, 0x91, 0xdf, 0x33, 0x93, 0x21, 0x3b],
            [0x79, 0xb7, 0x97, 0x85, 0x10, 0xb5, 0xba, 0x3c, 0xb6, 0x70, 0xd0, 0x06, 0xa1, 0xfa, 0x81, 0x82],
            [0x83, 0x7e, 0x7f, 0x80, 0x96, 0x73, 0xbe, 0x56, 0x9b, 0x9e, 0x95, 0xd9, 0xf7, 0x02, 0xb9, 0xa4],
            [0xde, 0x6a, 0x32, 0x6d, 0xd8, 0x8a, 0x84, 0x72, 0x2a, 0x14, 0x9f, 0x88, 0xf9, 0xdc, 0x89, 0x9a],
            [0xfb, 0x7c, 0x2e, 0xc3, 0x8f, 0xb8, 0x65, 0x48, 0x26, 0xc8, 0x12, 0x4a, 0xce, 0xe7, 0xd2, 0x62],
            [0x0c, 0xe0, 0x1f, 0xef, 0x11, 0x75, 0x78, 0x71, 0xa5, 0x8e, 0x76, 0x3d, 0xbd, 0xbc, 0x86, 0x57],
            [0x0b, 0x28, 0x2f, 0xa3, 0xda, 0xd4, 0xe4, 0x0f, 0xa9, 0x27, 0x53, 0x04, 0x1b, 0xfc, 0xac, 0xe6],
            [0x7a, 0x07, 0xae, 0x63, 0xc5, 0xdb, 0xe2, 0xea, 0x94, 0x8b, 0xc4, 0xd5, 0x9d, 0xf8, 0x90, 0x6b],
            [0xb1, 0x0d, 0xd6, 0xeb, 0xc6, 0x0e, 0xcf, 0xad, 0x08, 0x4e, 0xd7, 0xe3, 0x5d, 0x50, 0x1e, 0xb3],
            [0x5b, 0x23, 0x38, 0x34, 0x68, 0x46, 0x03, 0x8c, 0xdd, 0x9c, 0x7d, 0xa0, 0xcd, 0x1a, 0x41, 0x1c]
        ]
        row = self.value // 16
        col = self.value % 16
        return GF8(INV[row][col])




    def leftRotate(self, d):
        return GF8(((self.value << d) | (self.value >> (8 - d))) & 0xFF)

    def sbox(self):
        bb = self.inv()
        result = bb + bb.leftRotate(1) + bb.leftRotate(2) + bb.leftRotate(3) + bb.leftRotate(4) + GF8(0x63)
        return result

    def inv_sbox(self):
        bb = self.leftRotate(1) + self.leftRotate(3) + self.leftRotate(6) + GF8(0x05)
        result = bb.inv()
        return result

    def mixcol_matrix(self):
        ONE = GF8(0x01)
        TWO = GF8(0x02)
        THREE = GF8(0x03)
        return [[TWO, THREE, ONE, ONE], [THREE, ONE, ONE, TWO], [ONE, ONE, TWO, THREE], [ONE, TWO, THREE, ONE]]

    # def get_double(self):
    #     if self.value < 0x80:
    #         x = 2*self.value
    #     else:
    #         x = 2*self.value ^ 0x011b
    #     return GF8(x)

    # def get_double(self):
    #     return GF8(2)*self
