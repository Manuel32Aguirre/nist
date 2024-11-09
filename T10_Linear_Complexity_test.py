import numpy as np
from scipy.special import gammaincc

def berlekamp_massey_algorithm(sequence):
    n = len(sequence)
    b = [0] * n
    c = [0] * n
    b[0] = 1
    c[0] = 1
    l = 0
    m = -1
    for i in range(n):
        discrepancy = sequence[i]
        for j in range(1, l + 1):
            discrepancy ^= c[j] & sequence[i - j]
        if discrepancy == 1:
            t = c[:]
            for j in range(i - m, n):
                c[j] ^= b[j - (i - m)]
            if l <= i // 2:
                l = i + 1 - l
                m = i
                b = t
    return l

def linear_complexity_test(sequence, block_size):
    n = len(sequence)
    num_blocks = n // block_size
    blocks = [sequence[i * block_size:(i + 1) * block_size] for i in range(num_blocks)]
    complexities = [berlekamp_massey_algorithm(block) for block in blocks]
    mean = block_size / 2 + (9 + (-1) ** (block_size + 1)) / 36 - (block_size / 3 + 2 / 9) / (2 ** block_size)
    t = [(complexity - mean) for complexity in complexities]
    chi_squared = sum([t_i ** 2 for t_i in t]) * 2 / block_size
    p_value = gammaincc(num_blocks / 2, chi_squared / 2)
    return p_value

if __name__ == '__main__':
    # Example usage
    sequence = np.random.randint(0, 2, 1000).tolist()
    block_size = 500
    p_value = linear_complexity_test(sequence, block_size)
    print(f"P-value: {p_value}")