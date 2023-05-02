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

    def __eq__(self, other):
        return isinstance(other, GF8) and self.value == other.value

    def __repr__(self):
        return f"GF8({hex(self.value)})"


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
    def inverse(self):
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
        ZERO = GF8(0)
        ONE = GF8(1)
        if self == ZERO:
            return ZERO
        for i in range(1, 256):
            x = GF8(i)
            if self*x == ONE:
                return x
        print("XXXX: Cannot invert: {}".format(self))
        return ONE


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

    # def get_double(self):
    #     if self.value < 0x80:
    #         x = 2*self.value
    #     else:
    #         x = 2*self.value ^ 0x011b
    #     return GF8(x)

    # def get_double(self):
    #     return GF8(2)*self

