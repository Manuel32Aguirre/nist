import numpy as np
from scipy.special import gammaincc

def prueba_complejidad_lineal(secuencia, M=500):
    n = len(secuencia)
    N = n // M
    if N == 0:
        -1, False

    CL = []
    for i in range(N):
        bloque = secuencia[i * M:(i + 1) * M]
        CL.append(berlekamp_massey(bloque))

    mu = M / 2.0 + (9.0 + (-1)**(M + 1)) / 36.0 - (M / 3.0 + 2.0 / 9.0) / 2.0
    T = []
    for cl in CL:
        T.append((-1)**M * (cl - mu) + 2.0 / 9.0)

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
    chi_cuadrado = sum([(v[i] - N * pi[i])**2 / (N * pi[i]) for i in range(7)])
    valor_p = gammaincc(3.0, chi_cuadrado / 2.0)

    pasa_prueba = valor_p >= 0.01

    return valor_p, pasa_prueba

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
    sequence = np.random.randint(0, 2, 10000)

    print(f"Binary sequence: {sequence}")
    
    # Perform the linear complexity test
    p_value, passes_test = prueba_complejidad_lineal(sequence)
    
    print(f"P-value: {p_value}")