import math
from scipy.special import gammaincc

def nist_longest_run_test(binary_sequence, block_size):
    n = len(binary_sequence)
    N = n // block_size
    if N == 0:
        raise ValueError("Block size is too large for the given binary sequence length.")

    # Define the expected values and probabilities for different block sizes
    if block_size == 8:
        K = 3
        v_values = [1, 2, 3, 4]
        pi_values = [0.2148, 0.3672, 0.2305, 0.1875]
    elif block_size == 128:
        K = 5
        v_values = [4, 5, 6, 7, 8, 9]
        pi_values = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    elif block_size == 512:
        K = 6
        v_values = [10, 11, 12, 13, 14, 15, 16]
        pi_values = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    else:
        raise ValueError("Unsupported block size. Supported sizes are 8, 128, and 512.")

    # Count the longest run of ones in each block
    longest_runs = []
    for i in range(N):
        block = binary_sequence[i * block_size:(i + 1) * block_size]
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0
        longest_runs.append(max_run)

    # Count the frequencies of the longest runs
    frequencies = [0] * (K + 1)
    for run in longest_runs:
        if run <= v_values[0]:
            frequencies[0] += 1
        elif run >= v_values[-1]:
            frequencies[K] += 1
        else:
            for j in range(1, K):
                if v_values[j - 1] < run <= v_values[j]:
                    frequencies[j] += 1
                    break

    # Compute the chi-squared statistic
    chi_squared = 0
    for i in range(K + 1):
        chi_squared += ((frequencies[i] - N * pi_values[i]) ** 2) / (N * pi_values[i])

    # Compute the p-value
    p_value = gammaincc(K / 2.0, chi_squared / 2.0)

    # Determine if the sequence passes the test
    passes_test = p_value >= 0.01

    return p_value, passes_test

if __name__ == '__main__':
    # Example usage
    binary_string = "11001100000101010110110001001100111000000000001001" \
                    "00110101010001000100111101011010000000110101111100" \
                    "1100111001101101100010110010"
    
    binary_sequence = list(binary_string)

    print(f"Binary sequence: {binary_sequence.__len__()} bits")

    p_value, passes_test = nist_longest_run_test(binary_sequence, 8)
    print(f"P-value: {p_value}, Passes test: {passes_test}")

    #0.180609