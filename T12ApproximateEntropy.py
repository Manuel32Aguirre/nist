import math
from scipy.special import gammaincc  # Aseguramos que la función de complemento regularizado de la gamma esté disponible

def approximate_entropy_test(epsilon, m):
    n = len(epsilon)  # Calcular n como la longitud de epsilon
    ApEn = [0.0, 0.0]

    for blockSize in range(m, m + 2):
        if blockSize == 0:
            ApEn[0] = 0.0
        else:
            numOfBlocks = float(n)
            powLen = (2 ** (blockSize + 1)) - 1
            P = [0] * powLen

            for i in range(n):
                k = 1
                for j in range(blockSize):
                    k <<= 1
                    if epsilon[(i + j) % n] == '1':
                        k += 1
                P[k - 1] += 1

            # Calcular la frecuencia y la entropía aproximada
            sum_val = 0.0
            index = 2 ** blockSize - 1
            for i in range(2 ** blockSize):
                if P[index] > 0:
                    sum_val += P[index] * math.log(P[index] / numOfBlocks)
                index += 1
            sum_val /= numOfBlocks
            ApEn[blockSize - m] = sum_val

    # Calcular ApEn, Chi cuadrado y p_value
    apen = ApEn[0] - ApEn[1]
    chi_squared = 2.0 * n * (math.log(2) - apen)
    p_value = gammaincc(2 ** (m - 1), chi_squared / 2.0)  # Calcular el p_value usando la función gamma regularizada

    # Decidir si es aleatorio o no, según el p_value
    is_random = p_value >= 0.01  # Consideramos aleatorio si el p-value es mayor o igual a 0.01

    # Retornar el p_value y si es aleatorio
    return p_value, is_random
