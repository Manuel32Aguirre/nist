import math
import random
import scipy.stats as stats

def maurers_universal_statistical_test(binary_data):
    n = len(binary_data)
    L = 5  # Length of each block
    Q = 10  # Number of blocks to skip
    K = n // L - Q  # Number of blocks to test

    if K <= 0:
        return -1, False

    # Step 1: Initialization
    T = [0] * (2 ** L)
    for i in range(Q):
        block = binary_data[i * L:(i + 1) * L]
        T[int(''.join(map(str, block)), 2)] = i + 1

    # Step 2: Test
    sum_log = 0.0
    for i in range(Q, Q + K):
        block = binary_data[i * L:(i + 1) * L]
        dec_value = int(''.join(map(str, block)), 2)
        sum_log += math.log(i + 1 - T[dec_value], 2)
        T[dec_value] = i + 1

    # Step 3: Compute the test statistic
    fn = sum_log / K

    # Step 4: Compute the expected value and variance
    c = 0.7 - 0.8 / L + (4 + 32 / L) * (K ** (-3 / L)) / 15
    sigma = c * math.sqrt(2 / L)
    mu = math.log2(K)

    # Step 5: Compute the p-value
    p_value = math.erfc(abs((fn - mu) / (math.sqrt(2) * sigma)))

    # Determine if the sequence is random
    is_random = p_value >= 0.01

    return p_value, is_random
