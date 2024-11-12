import math
import scipy.special as spc

def block_frequency(bin_data: str, block_size=128):
    num_blocks = math.floor(len(bin_data) / block_size)
    block_start, block_end = 0, block_size
    # Keep track of the proportion of ones per block
    proportion_sum = 0.0
    for i in range(num_blocks):
        # Slice the binary string into a block
        block_data = bin_data[block_start:block_end]
        # Keep track of the number of ones
        ones_count = 0
        for char in block_data:
            if char == '1':
                ones_count += 1
        pi = ones_count / block_size
        proportion_sum += pow(pi - 0.5, 2.0)
        # Update the slice locations
        block_start += block_size
        block_end += block_size
    # Calculate the p-value
    chi_squared = 4.0 * block_size * proportion_sum
    p_val = spc.gammaincc(num_blocks / 2, chi_squared / 2)
    
    # Determine if the sequence is random (True) or not (False)
    is_random = p_val > 0.01
    return p_val, is_random
