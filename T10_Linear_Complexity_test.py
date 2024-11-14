import random
from scipy.special import gammaincc
import numpy as np

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

def berlekamp_massey_algorithm(sequence):
    # Implementación del algoritmo de Berlekamp-Massey para calcular la complejidad lineal de una secuencia
    n = len(sequence)
    L = 0
    m = -1
    C = [0] * n
    B = [0] * n
    C[0] = 1
    B[0] = 1
    for i in range(n):
        discrepancy = (sequence[i] + sum(C[1:L+1][j] * sequence[i-L+j] for j in range(L))) % 2
        if discrepancy == 1:
            T = C[:]
            for j in range(i - m, n):
                C[j] = (C[j] + B[j - (i - m)]) % 2
            if L <= i / 2:
                L = i + 1 - L
                m = i
                B = T
    return L

def linear_complexity_test(epsilon, M):
    # Asegúrate de que la secuencia sea una lista de enteros
    epsilon = [int(bit) for bit in epsilon]
    
    # Paso 1: Dividir la secuencia en bloques
    n = len(epsilon)
    N = n // M
    blocks = [epsilon[i * M:(i + 1) * M] for i in range(N)]
    
    # Paso 2: Calcular la complejidad lineal para cada bloque
    complexities = [berlekamp_massey_algorithm(block) for block in blocks]
    
    # Paso 3: Calcular el valor teórico esperado de la complejidad media
    mu = M / 2 + (9 + (-1)**(M + 1)) / 36 - (M / (2**(M - 1)))
    
    # Paso 4: Calcular Ti para cada bloque
    T = [(complexity - mu) for complexity in complexities]
    
    # Paso 5: Clasificar valores de Ti en categorías
    v = [0] * 7
    for t in T:
        if t <= -2.5:
            v[0] += 1
        elif -2.5 < t <= -1.5:
            v[1] += 1
        elif -1.5 < t <= -0.5:
            v[2] += 1
        elif -0.5 < t <= 0.5:
            v[3] += 1
        elif 0.5 < t <= 1.5:
            v[4] += 1
        elif 1.5 < t <= 2.5:
            v[5] += 1
        else:
            v[6] += 1
    
    # Paso 6: Calcular el estadístico de prueba chi-cuadrado
    pi = [0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]
    chi_squared = sum([(v[i] - N * pi[i])**2 / (N * pi[i]) for i in range(7)])
    
    # Paso 7: Calcular el valor p usando la función gamma incompleta regularizada
    p_value = gammaincc(3, chi_squared / 2)
    
    return p_value, p_value >= 0.01


if __name__ == '__main__':
    # Ejemplo para los primeros 1,000,000 dígitos binarios
    # binary_digits_of_e = calculate_binary_digits_of_e(1000000)
    binary_digits_of_e = [str(random.randint(0, 1)) for _ in range(100)]
    
    p_value, is_random = linear_complexity_test(binary_digits_of_e, 2)
    
    print(f"P-value: {p_value}")