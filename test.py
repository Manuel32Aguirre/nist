#!/usr/bin/env python

# sp_800_approximate_entropy_test.py
#
# Copyright (C) 2017 David Johnston
# This program is distributed under the terms of the GNU General Public License.
# 
# This file is part of sp800_22_tests.
# 
# sp800_22_tests is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# sp800_22_tests is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with sp800_22_tests.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import math
from math import gamma, e

# Functions for gamma calculations (from gamma_functions.py)

# Continued Fraction Computation for upper incomplete gamma
def upper_incomplete_gamma(a, x, d=0, iterations=100):
    if d == iterations:
        if ((d % 2) == 1):
            return 1.0  # end iterations
        else:
            m = d / 2
            return x + (m - a)
    if d == 0:
        try:
            result = ((x ** a) * (e ** (-x))) / upper_incomplete_gamma(a, x, d=d + 1)
        except OverflowError:
            result = 0.0
        return result
    elif ((d % 2) == 1):
        m = 1.0 + ((d - 1.0) / 2.0)
        return x + ((m - a) / (upper_incomplete_gamma(a, x, d=d + 1)))
    else:
        m = d / 2
        return 1 + (m / (upper_incomplete_gamma(a, x, d=d + 1)))

# Recursive implementation for upper incomplete gamma (alternative)
def upper_incomplete_gamma2(a, x, d=0, iterations=100):
    if d == iterations:
        return 1.0
    if d == 0:
        result = ((x ** a) * (e ** (-x))) / upper_incomplete_gamma2(a, x, d=d + 1)
        return result
    else:
        m = (d * 2) - 1
        return (m - a) + x + ((d * (a - d)) / (upper_incomplete_gamma2(a, x, d=d + 1)))

# Function for lower incomplete gamma
def lower_incomplete_gamma(a, x, d=0, iterations=100):
    if d == iterations:
        if ((d % 2) == 1):
            return 1.0  # end iterations
        else:
            m = d / 2
            return x + (m - a)
    if d == 0:
        result = ((x ** a) * (e ** (-x))) / lower_incomplete_gamma(a, x, d=d + 1)
        return result
    elif ((d % 2) == 1):
        m = d - 1
        n = (d - 1.0) / 2.0
        return a + m - (((a + n) * x) / lower_incomplete_gamma(a, x, d=d + 1))
    else:
        m = d - 1
        n = d / 2.0
        return a + m + ((n * x) / (lower_incomplete_gamma(a, x, d=d + 1)))

# Function for complimentary incomplete gamma
def complimentary_incomplete_gamma(a, x):
    return 1.0 - upper_incomplete_gamma(a, x)

# Scipy name mappings (functions)
def gammainc(a, x):
    return lower_incomplete_gamma(a, x) / gamma(a)

def gammaincc(a, x):
    return upper_incomplete_gamma(a, x) / gamma(a)

# --- Approximate Entropy Test Function ---
def bits_to_int(bits):
    theint = 0
    for i in range(len(bits)):
        theint = (theint << 1) + bits[i]
    return theint

def approximate_entropy_test(bits):
    n = len(bits)
    
    m = int(math.floor(math.log(n, 2))) - 6
    if m < 2:
        m = 2
    if m > 3:
        m = 3
        
    print("  n         = ", n)
    print("  m         = ", m)
    
    Cmi = list()
    phi_m = list()
    for iterm in range(m, m + 2):
        # Step 1 
        padded_bits = bits + bits[0:iterm - 1]
    
        # Step 2
        counts = list()
        for i in range(2 ** iterm):
            count = 0
            for j in range(n):
                if bits_to_int(padded_bits[j:j + iterm]) == i:
                    count += 1
            counts.append(count)
            print("  Pattern %d of %d, count = %d" % (i + 1, 2 ** iterm, count))
    
        # Step 3
        Ci = list()
        for i in range(2 ** iterm):
            Ci.append(float(counts[i]) / float(n))
        
        Cmi.append(Ci)
    
        # Step 4
        sum = 0.0
        for i in range(2 ** iterm):
            if (Ci[i] > 0.0):
                sum += Ci[i] * math.log((Ci[i] / 10.0))
        phi_m.append(sum)
        print("  phi(%d)    = %f" % (m, sum))
        
    # Step 5 - let the loop steps 1-4 complete
    
    # Step 6
    appen_m = phi_m[0] - phi_m[1]
    print("  AppEn(%d)  = %f" % (m, appen_m))
    chisq = 2 * n * (math.log(2) - appen_m)
    print("  ChiSquare = ", chisq)
    
    # Step 7
    p = gammaincc(2 ** (m - 1), (chisq / 2.0))
    
    success = (p >= 0.01)
    return (success, p, None)

if __name__ == "__main__":
    bits = [1,1,0,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,0,0,0,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1,0,1,1,0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,0,1,1,0,1,1,0,0,0,1,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,1,0,1,1,0,1,0,0,1,1,1,0,0,0,1,0,0,0,0,0,1,1,1,0,0,1,0,1,0,1,0,0,0,0
]
    success, p, _ = approximate_entropy_test(bits)
    
    print("success =", success)
    print("p = ", p)
