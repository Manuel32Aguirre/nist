def prueba_monobit(datos_binarios):
    n = len(datos_binarios)
    if n == 0:
        return -1, False
    
    cuenta_unos = datos_binarios.count(1)
    
    s_obs = abs(cuenta_unos - (n - cuenta_unos)) / (n ** 0.5)
    
    from math import erfc
    valor_p = erfc(s_obs / (2 ** 0.5))
    
    # Determinar si la secuencia pasa la prueba
    pasa_prueba = valor_p >= 0.01
    
    return valor_p, pasa_prueba

# Example usage
if __name__ == '__main__':
    binary_sequence = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
    p_value, passes_test = prueba_monobit(binary_sequence)
    print(f"p-value: {p_value}, Passes test: {passes_test}")