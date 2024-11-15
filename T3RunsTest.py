
from __future__ import print_function
import math
from fractions import Fraction
#from scipy.special import gamma, gammainc, gammaincc
from gamma_functions import *
import numpy
import cmath
import random

#ones_table = [bin(i)[2:].count('1') for i in range(256)]
def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes,ones)

def runs_test(bits):
    n = len(bits)
    zeroes, ones = count_ones_zeroes(bits)

    prop = float(ones) / float(n)
    print("  prop ", prop)

    tau = 2.0 / math.sqrt(n)
    print("  tau ", tau)

    if abs(prop - 0.5) > tau:
        return 0.0, False  # Solo dos valores

    vobs = 1.0
    for i in range(n - 1):
        if bits[i] != bits[i + 1]:
            vobs += 1.0

    print("  vobs ", vobs)
    p = math.erfc(abs(vobs - (2.0 * n * prop * (1.0 - prop))) / (2.0 * math.sqrt(2.0 * n) * prop * (1 - prop)))
    success = (p >= 0.01)

    return p, success  # Solo dos valores


