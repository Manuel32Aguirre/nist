import numpy as np
from scipy.special import gammaincc

from decimal import Decimal, getcontext

def calculate_binary_digits_of_e(num_digits):
    # Aumentar la precisión para asegurar suficientes dígitos
    getcontext().prec = num_digits * 4  # Ajustar para asegurarse de cubrir la longitud en binario

    # Calcular e usando la serie de Taylor
    e = Decimal(0)
    factorial = 1
    for i in range(num_digits * 2):  # Iterar suficientes términos para precisión requerida
        if i > 0:
            factorial *= i
        e += Decimal(1) / Decimal(factorial)

    # Convertir a binario y extraer los dígitos después del punto decimal
    binary_digits = []
    e_fractional = e % 1  # Solo la parte fraccionaria
    for _ in range(num_digits):
        e_fractional *= 2
        binary_digits.append(int(e_fractional))
        e_fractional %= 1

    return binary_digits

def berlekamp_massey(sequence):
    n = len(sequence)
    c = [0] * n
    b = [0] * n
    c[0], b[0] = 1, 1
    l, m, i = 0, -1, 0
    
    for i in range(n):
        discrepancy = sequence[i]
        for j in range(1, l + 1):
            discrepancy ^= c[j] & sequence[i - j]
        
        if discrepancy == 1:
            temp = c[:]
            for j in range(n - i + m):
                c[i - m + j] ^= b[j]
            if l <= i // 2:
                l = i + 1 - l
                m = i
                b = temp
    return l

def nist_linear_complexity_test(sequence, M=500):
    N = len(sequence) // M
    if N == 0:
        raise ValueError("La longitud de la secuencia debe ser al menos igual a M.")
    
    # Dividir la secuencia en bloques de longitud M
    blocks = [sequence[i * M:(i + 1) * M] for i in range(N)]

    # Calcular la complejidad lineal de cada bloque
    complexities = [berlekamp_massey(block) for block in blocks]
    
    # Calcular el valor esperado y la desviación estándar
    mean = M / 2.0 + (9 + (-1) ** (M + 1)) / 36.0 - (M / 3.0 + 2 / 9.0) / 2 ** M
    variance = M * (1 / 2.0 + (9 + (-1) ** (M + 1)) / 36.0 - (M / 3.0 + 2 / 9.0) / 2 ** M) / 2
    
    # Calcular la estadística de prueba T para cada bloque
    T = np.array([(complexity - mean) / np.sqrt(variance) for complexity in complexities])
    
    # Calcular el valor Chi-cuadrado
    v = [np.sum((T >= -2.5 + 0.5 * i) & (T < -2.5 + 0.5 * (i + 1))) for i in range(6)]
    pi = [0.10, 0.25, 0.30, 0.20, 0.10, 0.05]  # probabilidades teóricas
    chi_squared = np.sum([(v[i] - N * pi[i]) ** 2 / (N * pi[i]) for i in range(6)])
    
    # Calcular el valor p
    p_value = gammaincc(5 / 2.0, chi_squared / 2.0)

    # Decisión de rechazo
    is_random = p_value >= 0.01

    return p_value, is_random

if __name__ == '__main__':
    # Ejemplo para los primeros 1,000,000 dígitos binarios
    binary_digits_of_e = calculate_binary_digits_of_e(1000000)
    
    p_value, is_random = nist_linear_complexity_test(list(map(int, binary_digits_of_e)))
    
    print(f"P-value: {p_value}")