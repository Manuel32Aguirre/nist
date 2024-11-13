import math
import numpy as np
from math import sqrt, log
from scipy.special import erfc

def universal_test(epsilon, L, Q):
    # Asegurarse de que epsilon sea una cadena de caracteres '0' y '1'
    if not all(c in '01' for c in epsilon):
        raise ValueError("La secuencia epsilon debe ser una cadena de 0s y 1s.")

    # Calcular n automáticamente (longitud de la secuencia epsilon)
    n = len(epsilon)

    # Verificar que la longitud de epsilon sea suficiente para L y Q
    if n < Q * L:
        raise ValueError(f"Error: La longitud de epsilon es insuficiente. Se requiere al menos {Q * L} bits, pero se proporcionaron {n} bits.")

    # Definir los valores esperados y la varianza para cada valor de L
    expected_value = [0, 0, 0, 0, 0, 0, 5.2177052, 6.1962507, 7.1836656,
                      8.1764248, 9.1723243, 10.170032, 11.168765, 12.168070, 13.167693,
                      14.167488, 15.167379]
    variance = [0, 0, 0, 0, 0, 0, 2.954, 3.125, 3.238, 3.311, 3.356, 3.384,
                3.401, 3.410, 3.416, 3.419, 3.421]

    # Verificación de los parámetros de entrada
    p = int(math.pow(2, L))  # Número de posibles estados (2^L)

    # Calcular K y asegurarse de que sea positivo
    K = int(math.floor(n / L) - 10 * int(math.pow(2, L)))  # Número de bloques a probar
    if K <= 0:
        K = 1  # Asegurarse de que K sea al menos 1

    # Ajustar Q si es necesario (dependiendo de L)
    Q = 10 * int(math.pow(2, L))  # Ajuste de Q según L

    # Inicializar la tabla T de ceros
    T = np.zeros(p, dtype=int)

    # Cálculos previos
    c = 0.7 - 0.8 / L + (4 + 32 / L) * math.pow(K, -3 / L) / 15
    sigma = c * sqrt(variance[L] / K)

    # Asegurarse de que sigma no sea cero (prevención de división por cero)
    if sigma <= 0:
        sigma = 1e-10  # Evitar que sigma sea cero

    sqrt2 = sqrt(2)
    sum_log = 0.0

    # Inicializar la tabla T con los primeros Q bloques
    for i in range(1, Q + 1):
        decRep = 0
        for j in range(L):
            index = (i - 1) * L + j
            if index >= n:
                raise IndexError(f"Índice fuera de rango: {index}. La secuencia epsilon es demasiado corta.")
            decRep += int(epsilon[index]) * int(math.pow(2, L - 1 - j))
        T[decRep] = i

    # Procesar los siguientes K bloques
    for i in range(Q + 1, Q + K + 1):
        decRep = 0
        for j in range(L):
            index = (i - 1) * L + j
            if index >= n:
                raise IndexError(f"Índice fuera de rango: {index}. La secuencia epsilon es demasiado corta.")
            decRep += int(epsilon[index]) * int(math.pow(2, L - 1 - j))
        sum_log += log(i - T[decRep], 2)
        T[decRep] = i

    # Calcular phi y el valor p
    phi = sum_log / K
    expected_val = expected_value[L]
    variance_val = variance[L]

    # Calcular el valor 'arg' para la función de error complementaria
    arg = abs(phi - expected_val) / (sqrt2 * sigma)
    p_value = erfc(arg)

    # Verificar que el p_value esté en el rango esperado
    if p_value < 0 or p_value > 1:
        raise ValueError("p_value está fuera de rango.")

    # Determinar si la secuencia es aleatoria
    result = "SUCCESS" if p_value >= 0.01 else "FAILURE"

    # Mostrar los resultados
    print("\t\tUNIVERSAL STATISTICAL TEST")
    print("\t\t----------------------------")
    print(f"\t\t(a) L         = {L}")
    print(f"\t\t(b) Q         = {Q}")
    print(f"\t\t(c) K         = {K}")
    print(f"\t\t(d) sum       = {sum_log}")
    print(f"\t\t(e) sigma     = {sigma}")
    print(f"\t\t(f) variance  = {variance_val}")
    print(f"\t\t(g) exp_value = {expected_val}")
    print(f"\t\t(h) phi       = {phi}")
    print(f"\t\t(i) p_value   = {p_value}")
    print(f"\t\t(j) RESULT    = {result}")

    return p_value, p_value >= 0.01
