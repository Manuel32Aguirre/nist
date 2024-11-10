import numpy as np
from scipy.linalg import lu
def prueba_rango_matriz_binaria(datos_binarios, tamano_matriz):
    n = len(datos_binarios)
    if n < tamano_matriz * tamano_matriz:
        return -1, False
    
    num_matrices = n // (tamano_matriz * tamano_matriz)
    matrices = []
    
    for i in range(num_matrices):
        matriz = []
        for j in range(tamano_matriz):
            fila = [datos_binarios[i * tamano_matriz * tamano_matriz + j * tamano_matriz + k] for k in range(tamano_matriz)]
            matriz.append(fila)
        matrices.append(np.array(matriz))
    
    cuenta_rango_completo = 0
    for matriz in matrices:
        _, u = lu(matriz, permute_l=True)
        rango = np.sum(np.abs(np.diag(u)) > 1e-10)
        if rango == tamano_matriz:
            cuenta_rango_completo += 1
    
    valor_p = cuenta_rango_completo / num_matrices

    pasa_prueba = valor_p >= 0.01

    return valor_p, pasa_prueba

if __name__ == '__main__':
    datos_binarios = [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1]
    valor_p, pasa_prueba = prueba_rango_matriz_binaria(datos_binarios, tamano_matriz=3)
    print(f"Valor p: {valor_p}, pasa prueba: {pasa_prueba}")