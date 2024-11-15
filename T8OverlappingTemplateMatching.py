from math import floor
from numpy import array, exp, zeros
from scipy.special import gammaincc, hyp1f1
from mpmath import mp

def overlappingTemplateMachine(binary_data: str, pattern: str):
    block_size = 1032
    verbose = False
    length_of_binary_data = len(binary_data)
    pattern_size = len(pattern)  # Usar el tamaño del patrón pasado

    number_of_block = floor(length_of_binary_data / block_size)

    # λ = (M-m+1)/pow(2, m)
    lambda_val = float(block_size - pattern_size + 1) / pow(2, pattern_size)
    # η = λ/2
    eta = lambda_val / 2.0

    pi = [get_prob(i, eta) for i in range(5)]
    diff = float(array(pi).sum())
    pi.append(1.0 - diff)

    pattern_counts = zeros(6)
    for i in range(number_of_block):
        block_start = i * block_size
        block_end = block_start + block_size
        block_data = binary_data[block_start:block_end]
        
        pattern_count = 0
        j = 0
        while j < block_size:
            sub_block = block_data[j:j + pattern_size]
            if sub_block == pattern:
                pattern_count += 1
            j += 1
        if pattern_count <= 4:
            pattern_counts[pattern_count] += 1
        else:
            pattern_counts[5] += 1

    xObs = 0.0
    for i in range(len(pattern_counts)):
        xObs += pow(pattern_counts[i] - number_of_block * pi[i], 2.0) / (number_of_block * pi[i])

    p_value = gammaincc(5.0 / 2.0, xObs / 2.0)
    print("Se esta retornando un p value de ", p_value)
    return (p_value, (p_value >= 0.01))

def get_prob(u, x):
    out = 1.0 * exp(-x)
    if u != 0:
        out = 1.0 * x * exp(2 * -x) * (2 ** -u) * hyp1f1(u + 1, 2, x)
    return out

def obtener_expansion_binaria_e(bits):
    mp.dps = bits + 2
    e = mp.e
    binario_e = bin(int(e * (2 ** bits)))[2:].zfill(bits)
    return binario_e
