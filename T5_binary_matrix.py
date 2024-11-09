import numpy as np
from scipy.linalg import lu

def binary_matrix_rank_test(binary_data, matrix_size=32):
    """
    Perform the NIST Binary Matrix Rank Test for a given binary data sequence and matrix size.
    
    Parameters:
    binary_data (list): A list of binary data (e.g., [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1]).
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
            row = [binary_data[i * matrix_size * matrix_size + j * matrix_size + k] for k in range(matrix_size)]
            matrix.append(row)
        matrices.append(np.array(matrix))
    
    full_rank_count = 0
    for matrix in matrices:
        _, u = lu(matrix, permute_l=True)
        rank = np.sum(np.abs(np.diag(u)) > 1e-10)
        if rank == matrix_size:
            full_rank_count += 1
    
    p_value = full_rank_count / num_matrices

    passes_test = p_value >= 0.01

    return p_value, passes_test

# Example usage
binary_data = [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1]
p_value, passes_test = binary_matrix_rank_test(binary_data, matrix_size=3)
print(f"P-value: {p_value}, passes test: {passes_test}")