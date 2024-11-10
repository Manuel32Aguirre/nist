from math import floor
from numpy import array
from numpy import exp
from numpy import zeros
from scipy.special import gammaincc
from scipy.special import hyp1f1

def overlappingTemplateMachine(binary_data: str, verbose=False, pattern_size=9, block_size=1032):
    """
    Overlapping Template Matching Test to detect the number of occurrences of pre-specified target strings.
    :param binary_data: a binary string
    :param verbose: True to display debug messages, False to turn off debug messages
    :param pattern_size: the length of the pattern to match
    :param block_size: the size of the block to test
    :return: (p_value, bool) A tuple containing the p_value and a boolean indicating if the sequence is random.
    """
    length_of_binary_data = len(binary_data)
    pattern = '1' * pattern_size

    number_of_block = floor(length_of_binary_data / block_size)

    # λ = (M-m+1)/pow(2, m)
    lambda_val = float(block_size - pattern_size + 1) / pow(2, pattern_size)
    # η = λ/2
    eta = lambda_val / 2.0

    pi = [get_prob(i, eta) for i in range(5)]
    diff = float(array(pi).sum())
    pi.append(1.0 - diff)

    pattern_counts = zeros(6)
    for i in range(number_of_block):
        block_start = i * block_size
        block_end = block_start + block_size
        block_data = binary_data[block_start:block_end]
        
        pattern_count = 0
        j = 0
        while j < block_size:
            sub_block = block_data[j:j + pattern_size]
            if sub_block == pattern:
                pattern_count += 1
            j += 1
        if pattern_count <= 4:
            pattern_counts[pattern_count] += 1
        else:
            pattern_counts[5] += 1

    xObs = 0.0
    for i in range(len(pattern_counts)):
        xObs += pow(pattern_counts[i] - number_of_block * pi[i], 2.0) / (number_of_block * pi[i])

    p_value = gammaincc(5.0 / 2.0, xObs / 2.0)

    if verbose:
        print('Overlapping Template Test DEBUG BEGIN:')
        print("\tLength of input:\t\t", length_of_binary_data)
        print('\tValue of Vs:\t\t\t', pattern_counts)
        print('\tValue of xObs:\t\t\t', xObs)
        print('\tP-Value:\t\t\t\t', p_value)
        print('DEBUG END.')

    return (p_value, (p_value >= 0.01))

def get_prob(u, x):
    out = 1.0 * exp(-x)
    if u != 0:
        out = 1.0 * x * exp(2 * -x) * (2 ** -u) * hyp1f1(u + 1, 2, x)
    return out

# Ejemplo de datos binarios
binary_data = '110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001110010101010111100101010110011101001010111000111001010101001'  # un ejemplo de cadena binaria

# Llamada a la función overlapping_patterns
p_value, is_random = overlappingTemplateMachine(binary_data, verbose=True, pattern_size=9, block_size=1032)

# Imprimir los resultados
print(f"P-Value: {p_value}")
print(f"Is the sequence random? {is_random}")
