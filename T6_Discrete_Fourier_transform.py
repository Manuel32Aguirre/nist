import numpy as np
from scipy.fft import fft
from scipy.special import erfc

def nist_dft_test(sequence):
    # Convertir la lista binaria de 0 y 1 a -1 y 1
    sequence = np.array([1 if bit == 1 else -1 for bit in sequence])

    # Calcular la FFT
    fft_result = fft(sequence)

    # Calcular la magnitud de la FFT
    magnitude = np.abs(fft_result)[:len(sequence) // 2]

    # Calcular el umbral
    threshold = np.sqrt(np.log(1.0 / 0.05) * len(sequence))

    # Contar el número de frecuencias por debajo del umbral
    n0 = 0.95 * (len(sequence) / 2)
    n1 = np.sum(magnitude < threshold)

    # Calcular la estadística d
    d = (n1 - n0) / np.sqrt(len(sequence) * 0.95 * 0.05 / 4)

    # Calcular el valor p
    p_value = erfc(np.abs(d) / np.sqrt(2))

    # Decisión de rechazo
    is_random = p_value >= 0.01

    return p_value, is_random


if __name__ == '__main__':
    # Ejemplo de uso
    binary_string = "11001001000011111101101010100010001000010110100011" \
                    "00001000110100110001001100011001100010100010111000"
    
    binary_sequence = list(binary_string)

    print(f"Binary sequence: {len(binary_sequence)} bits")

    p_value, passes = nist_dft_test(binary_sequence)
    print(f"P-value: {p_value}, Passes test: {passes}")