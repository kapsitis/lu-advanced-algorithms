import numpy as np
from scipy.fftpack import dct, idct

def dct2(arr):
    return dct(dct(arr.T, norm='ortho').T, norm='ortho')

def idct2(arr):
    return idct(idct(arr.T, norm='ortho').T, norm='ortho')

# Create an 8x8 matrix with random values between 0 and 1
matrix = np.random.rand(8, 8)
print(matrix)
dct_coefficients = dct2(matrix)
print(dct_coefficients)
inverse_dct = idct2(dct_coefficients)
print(inverse_dct)


