import math
from scipy.special import gammaincc

def prueba_corrida_mas_larga(bits, tamano_bloque=8):
    n = len(bits)
    if n < tamano_bloque:
        return -1, False

    num_bloques = n // tamano_bloque

    if tamano_bloque == 8:
        v = [1, 2, 3, 4]
        pi = [0.2148, 0.3672, 0.2305, 0.1875]
    elif tamano_bloque == 128:
        v = [4, 5, 6, 7, 8, 9]
        pi = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    elif tamano_bloque == 10000:
        v = [10, 11, 12, 13, 14, 15, 16]
        pi = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    else:
        return -1, False

    conteos = [0] * len(v)
    for i in range(num_bloques):
        bloque = bits[i * tamano_bloque:(i + 1) * tamano_bloque]
        max_corrida = max(map(len, ''.join(map(str, bloque)).split('0')))
        for j in range(len(v)):
            if max_corrida == v[j]:
                conteos[j] += 1
                break
            elif max_corrida > v[-1]:
                conteos[-1] += 1
                break
    chi_cuadrado = sum([(conteos[i] - num_bloques * pi[i]) ** 2 / (num_bloques * pi[i]) for i in range(len(v))])

    valor_p = gammaincc(len(v) / 2.0, chi_cuadrado / 2.0)

    pasa_prueba = valor_p >= 0.01

    return valor_p, pasa_prueba

if __name__ == '__main__':
    # Example usage
    bits = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
    p_value, passes_test = prueba_corrida_mas_larga(bits)
    print(f"P-value: {p_value}, Passes test: {passes_test}")