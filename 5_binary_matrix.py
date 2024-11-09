import numpy as np
from scipy.linalg import lu

def binary_matrix_rank_test(binary_data, matrix_size):
    """
    Perform the NIST Binary Matrix Rank Test for a given binary data sequence and matrix size.
    
    Parameters:
    binary_data (str): A string of binary data (e.g., '110010101011').
    matrix_size (int): The size of the matrix (e.g., 3 for a 3x3 matrix).
    
    Returns:
    float: The p-value of the test.
    """
    n = len(binary_data)
    if n < matrix_size * matrix_size:
        raise ValueError("Binary data is too short for the given matrix size.")
    
    num_matrices = n // (matrix_size * matrix_size)
    matrices = []
    
    for i in range(num_matrices):
        matrix = []
        for j in range(matrix_size):
            row = [int(binary_data[i * matrix_size * matrix_size + j * matrix_size + k]) for k in range(matrix_size)]
            matrix.append(row)
        matrices.append(np.array(matrix))
    
    full_rank_count = 0
    for matrix in matrices:
        _, u = lu(matrix, permute_l=True)
        rank = np.sum(np.abs(np.diag(u)) > 1e-10)
        if rank == matrix_size:
            full_rank_count += 1
    
    p_value = full_rank_count / num_matrices
    return p_value

# Example usage
binary_data = '1100101010110010101011001010101100101010110010101011001010101100'
matrix_size = 3
p_value = binary_matrix_rank_test(binary_data, matrix_size)
print(f"P-value: {p_value}")