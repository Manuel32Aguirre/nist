import numpy as np
from scipy.fftpack import fft
from scipy.special import erfc

def nist_discrete_fourier_transform(binary_data):
    n = len(binary_data)
    # Convert binary data to +1, -1
    X = np.array([1 if bit == '1' else -1 for bit in binary_data])
    
    # Perform FFT
    S = np.abs(fft(X))**2
    
    # Calculate T
    T = np.sqrt(np.log(1/0.05) * n)
    
    # Count peaks
    N0 = 0.95 * n / 2
    N1 = np.sum(S[1:n//2] < T)
    
    # Calculate P-value
    d = N1 - N0
    p_value = erfc(np.abs(d) / np.sqrt(2))
    
    return p_value

if __name__ == '__main__':
    # Test the function
    binary_data = '11001001000011111101101010100010001000010110100011'
    p_value = nist_discrete_fourier_transform(binary_data)
    print(f"P-value: {p_value}")