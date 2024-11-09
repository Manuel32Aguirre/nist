e__ == "__main__":
    # Example sequence (binary)
    sequence = np.random.randint(0, 2, 10000)
    
    # Perform the linear complexity test
    p_value = linear_complexity_test(sequence)
    
    print(f"P-