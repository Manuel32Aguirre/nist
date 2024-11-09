import math
from scipy.special import gammaincc

def longest_run_ones_test(bits, block_size=8):
    n = len(bits)
    if n < block_size:
        raise ValueError("The length of the bit string must be at least as large as the block size.")

    # Determine the number of blocks
    num_blocks = n // block_size

    # Define the expected probabilities for the longest run of ones in a block
    if block_size == 8:
        v = [1, 2, 3, 4]
        pi = [0.2148, 0.3672, 0.2305, 0.1875]
    elif block_size == 128:
        v = [4, 5, 6, 7, 8, 9]
        pi = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    elif block_size == 10000:
        v = [10, 11, 12, 13, 14, 15, 16]
        pi = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    else:
        raise ValueError("Unsupported block size. Supported sizes are 8, 128, and 10000.")

    # Count the longest run of ones in each block
    counts = [0] * len(v)
    for i in range(num_blocks):
        block = bits[i * block_size:(i + 1) * block_size]
        max_run = max(map(len, ''.join(map(str, block)).split('0')))
        for j in range(len(v)):
            if max_run == v[j]:
                counts[j] += 1
                break
            elif max_run > v[-1]:
                counts[-1] += 1
                break

    # Calculate the chi-squared statistic
    chi_squared = sum([(counts[i] - num_blocks * pi[i]) ** 2 / (num_blocks * pi[i]) for i in range(len(v))])

    # Calculate the p-value
    p_value = gammaincc(len(v) / 2.0, chi_squared / 2.0)

    return p_value

if __name__ == '__main__':
    # Example usage
    bits = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
    p_value = longest_run_ones_test(bits)
    print(f"P-value: {p_value}")