import math

def prueba_monobit(binary_sequence):
    n = len(binary_sequence)
    count = binary_sequence.count('1')
    s_obs = abs(count - (n - count))
    s_obs = s_obs / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    passes_test = p_value >= 0.01
    return p_value, passes_test

# Example usage
if __name__ == '__main__':

    # Texto binario extraído y limpio
    binary_string = "11001001000011111101101010100010001000010110100011" \
                    "00001000110100110001001100011001100010100010111000"

    binary_sequence = list(binary_string)

    print(f"Binary sequence: {binary_sequence.__len__()} bits")

    p_value, passes_test = prueba_monobit(binary_sequence)
    print(f"p-value: {p_value}, Passes test: {passes_test}")