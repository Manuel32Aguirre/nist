import numpy as np
from scipy.special import gammaincc

def linear_complexity_test(sequence, M=500):
    n = len(sequence)
    N = n // M
    if N == 0:
        raise ValueError("Sequence length must be at least M.")

    LC = []
    for i in range(N):
        block = sequence[i * M:(i + 1) * M]
        LC.append(berlekamp_massey(block))

    mu = M / 2.0 + (9.0 + (-1)**(M + 1)) / 36.0 - (M / 3.0 + 2.0 / 9.0) / 2.0
    T = []
    for lc in LC:
        T.append((-1)**M * (lc - mu) + 2.0 / 9.0)

    v = [0] * 7
    for t in T:
        if t <= -2.5:
            v[0] += 1
        elif t <= -1.5:
            v[1] += 1
        elif t <= -0.5:
            v[2] += 1
        elif t <= 0.5:
            v[3] += 1
        elif t <= 1.5:
            v[4] += 1
        elif t <= 2.5:
            v[5] += 1
        else:
            v[6] += 1

    pi = [0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]
    chi_squared = sum([(v[i] - N * pi[i])**2 / (N * pi[i]) for i in range(7)])
    p_value = gammaincc(3.0, chi_squared / 2.0)


    passes_test = p_value >= 0.01

    return p_value, passes_test

def berlekamp_massey(block):
    n = len(block)
    c = [0] * n
    b = [0] * n
    c[0] = 1
    b[0] = 1
    L = 0
    m = -1
    N = 0

    while N < n:
        d = block[N]
        for i in range(1, L + 1):
            d ^= c[i] * block[N - i]
        if d == 1:
            t = c[:]
            for i in range(N - m, n):
                c[i] ^= b[i - (N - m)]
            if L <= N / 2:
                L = N + 1 - L
                m = N
                b = t
        N += 1

    return L

if __name__ == '__main__':
    # Example sequence (binary)
    sequence = np.random.randint(0, 2, 10000)

    print(f"Binary sequence: {sequence}")
    
    # Perform the linear complexity test
    p_value = linear_complexity_test(sequence)
    
    print(f"P-value: {p_value}")