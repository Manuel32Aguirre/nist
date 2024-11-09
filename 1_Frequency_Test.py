def monobit_test(binary_data):
    """
    Perform the Frequency (Monobit) Test on a binary sequence.
    
    Parameters:
    binary_data (str): A string of binary data (e.g., '1100101010110001')
    
    Returns:
    bool: True if the sequence passes the test, False otherwise
    float: The p-value of the test
    """
    n = len(binary_data)
    if n == 0:
        raise ValueError("The binary data should not be empty")
    
    # Count the number of 1s in the binary sequence
    count_ones = binary_data.count('1')
    
    # Calculate the test statistic
    s_obs = abs(count_ones - (n - count_ones)) / (n ** 0.5)
    
    # Calculate the p-value
    from math import erfc
    p_value = erfc(s_obs / (2 ** 0.5))
    
    # Determine if the sequence passes the test
    passes_test = p_value >= 0.01
    
    return p_value

# Example usage
if __name__ == '__main__':
    binary_sequence = '1100101010110001'
    p_value = monobit_test(binary_sequence)
    print(f"p-value: {p_value}")