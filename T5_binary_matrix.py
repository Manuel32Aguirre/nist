import numpy as np
from scipy.stats import chi2

def binary_matrix_rank_test(e, M, Q):
    # Paso 1: Dividir la secuencia en bloques de M*Q bits
    n = len(e)
    N = n // (M * Q)
    sequence = [int(bit) for bit in e[:N * M * Q]]  # Ignorar bits sobrantes

    # Crear matrices de MxQ
    matrices = []
    for i in range(N):
        matrix = np.array(sequence[i * M * Q: (i + 1) * M * Q]).reshape(M, Q)
        matrices.append(matrix)
    
    # Paso 2: Calcular el rango de cada matriz
    ranks = []
    for matrix in matrices:
        rank = np.linalg.matrix_rank(matrix)
        ranks.append(rank)
    
    # Contar la frecuencia de cada rango
    F_M = ranks.count(M)      # Número de matrices con rango completo M
    F_M1 = ranks.count(M - 1)  # Número de matrices con rango completo M-1
    F_other = N - F_M - F_M1   # Resto de matrices

    # Paso 4: Calcular estadístico chi-cuadrado
    chi_square_obs = ((F_M - 0.2888 * N) ** 2) / (0.2888 * N) + \
                     ((F_M1 - 0.5776 * N) ** 2) / (0.5776 * N) + \
                     ((F_other - 0.1336 * N) ** 2) / (0.1336 * N)
    
    # Valor crítico de chi-cuadrado para 2 grados de libertad y nivel de significancia del 1%
    p_value = 1 - chi2.cdf(chi_square_obs, df=2)
    
    return p_value, p_value >= 0.01


if __name__ == '__main__':
    # Example usage
    binary_string = "01011001001010101101"
    
    binary_sequence = list(map(int, binary_string))

    print(f"Binary sequence: {len(binary_sequence)} bits")

    p_value, passes = binary_matrix_rank_test(binary_sequence, 3, 3)
    print(f"P-value: {p_value}, Passes test: {passes}")