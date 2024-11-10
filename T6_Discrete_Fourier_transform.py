import numpy as np
from scipy.fftpack import fft
from scipy.special import erfc
def transformada_fourier_discreta_nist(lista_datos_binarios):
    datos_binarios = ''.join(map(str, lista_datos_binarios))
    n = len(datos_binarios)
    X = np.array([1 if bit == '1' else -1 for bit in datos_binarios])
    
    S = np.abs(fft(X))**2
    
    T = np.sqrt(np.log(1/0.05) * n)
    
    N0 = 0.95 * n / 2
    N1 = np.sum(S[1:n//2] < T)
    
    d = N1 - N0
    valor_p = erfc(np.abs(d) / np.sqrt(2))
    
    pasa_prueba = valor_p >= 0.01

    return valor_p, pasa_prueba

if __name__ == '__main__':
    # Test the function
    binary_data = '11001001000011111101101010100010001000010110100011'
    p_value, passes_test = transformada_fourier_discreta_nist(binary_data)
    print(f"P-value: {p_value}, passes test: {passes_test}")