import math
from scipy.stats import norm  # Para usar la función de distribución normal acumulativa (CDF)

ALPHA = 0.01  # Nivel de significancia

def cumulative_sums(epsilon):
    n = len(epsilon)
    S, sup, inf = 0, 0, 0
    z, zrev = 0, 0
    
    # Calcular S, sup, inf, z y zrev en el sentido hacia adelante
    for k in range(n):
        S += 1 if epsilon[k] == '1' else -1
        if S > sup:
            sup += 1
        if S < inf:
            inf -= 1
        z = max(sup, -inf)
        zrev = max(sup - S, S - inf)
    
    # Función auxiliar para calcular sum1 y sum2
    def compute_sums(z_val, n):
        sum1 = sum(
            norm.cdf((4 * k + 1) * z_val / math.sqrt(n)) - norm.cdf((4 * k - 1) * z_val / math.sqrt(n))
            for k in range(int((-n / z_val + 1) / 4), int((n / z_val - 1) / 4) + 1)
        )
        sum2 = sum(
            norm.cdf((4 * k + 3) * z_val / math.sqrt(n)) - norm.cdf((4 * k + 1) * z_val / math.sqrt(n))
            for k in range(int((-n / z_val - 3) / 4), int((n / z_val - 1) / 4) + 1)
        )
        return sum1, sum2

    # Prueba en la dirección hacia adelante
    sum1, sum2 = compute_sums(z, n)
    p_value_forward = 1.0 - sum1 + sum2
    is_random_forward = p_value_forward >= ALPHA

    # Prueba en la dirección hacia atrás
    sum1, sum2 = compute_sums(zrev, n)
    p_value_reverse = 1.0 - sum1 + sum2
    is_random_reverse = p_value_reverse >= ALPHA

    # Retornar los p-values y si cumple la aleatoriedad en ambas direcciones
    return p_value_forward, p_value_reverse, is_random_forward, is_random_reverse
