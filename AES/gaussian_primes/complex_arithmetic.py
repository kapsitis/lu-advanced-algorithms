def multiply_gaussian(a, b):
    return a * b

def divide_gaussian(dividend, divisor):
    quotient = dividend / divisor
    round_quotient = complex(round(quotient.real), round(quotient.imag))
    remainder = dividend - round_quotient * divisor
    return round_quotient, remainder

def gcd_gaussian(a, b):
    while b != 0:
        _, remainder = divide_gaussian(a, b)
        a, b = b, remainder
    return a


def main():
    # Examples
    z1 = complex(3, 2)  # This represents the Gaussian integer 3 + 2i
    z2 = complex(1, 4)  # This represents the Gaussian integer 1 + 4i

    product = multiply_gaussian(z1, z2)
    print(f"The product of {z1} and {z2} is {product}")

    z1 = complex(7, 1)   # Represents the Gaussian integer 7 + i
    z2 = complex(3, -2)  # Represents the Gaussian integer 3 - 2i

    quotient, remainder = divide_gaussian(z1, z2)
    print(f"When dividing {z1} by {z2}, quotient is {quotient} and remainder is {remainder}")

    z1 = complex(35, 13)
    z2 = complex(1, 15)

    gcd = gcd_gaussian(z1, z2)
    print(f"The greatest common divisor of {z1} and {z2} is {gcd}")


if __name__ == '__main__': 
    main()
