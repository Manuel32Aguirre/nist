from math import floor, log, sqrt
from numpy import zeros
from scipy.special import erfc

def maurers_universal_statistical_test(binary_data):
    """
    Realiza la Prueba Universal Estadística de Maurer para una secuencia binaria.
    
    :param binary_data: list of int, secuencia binaria representada como una lista de bits (0s y 1s)
    :return: (entropia, p_valor, es_aleatorio) -> float, float, bool
    """
    binary_str = ''.join(map(str, binary_data))  # Convertir lista de bits a cadena binaria
    length_of_binary_data = len(binary_str)
    pattern_size = 5

    # Configuración del tamaño de patrón en función de la longitud de la secuencia
    if length_of_binary_data >= 387840:
        pattern_size = 6
    if length_of_binary_data >= 904960:
        pattern_size = 7
    if length_of_binary_data >= 2068480:
        pattern_size = 8
    if length_of_binary_data >= 4654080:
        pattern_size = 9
    if length_of_binary_data >= 10342400:
        pattern_size = 10
    if length_of_binary_data >= 22753280:
        pattern_size = 11
    if length_of_binary_data >= 49643520:
        pattern_size = 12
    if length_of_binary_data >= 107560960:
        pattern_size = 13
    if length_of_binary_data >= 231669760:
        pattern_size = 14
    if length_of_binary_data >= 496435200:
        pattern_size = 15
    if length_of_binary_data >= 1059061760:
        pattern_size = 16

    if 5 < pattern_size < 16:
        num_ints = 2**pattern_size - 1
        vobs = zeros(num_ints + 1)
        num_blocks = floor(length_of_binary_data / pattern_size)
        init_bits = 10 * pow(2, pattern_size)
        test_bits = num_blocks - init_bits

        # Valores esperados y variancia de la prueba
        c = 0.7 - 0.8 / pattern_size + (4 + 32 / pattern_size) * pow(test_bits, -3 / pattern_size) / 15
        variance = [0, 0, 0, 0, 0, 0, 2.954, 3.125, 3.238, 3.311, 3.356, 3.384, 3.401, 3.410, 3.416, 3.419, 3.421]
        expected = [0, 0, 0, 0, 0, 0, 5.2177052, 6.1962507, 7.1836656, 8.1764248, 9.1723243,
                    10.170032, 11.168765, 12.168070, 13.167693, 14.167488, 15.167379]
        sigma = c * sqrt(variance[pattern_size] / test_bits)

        cumsum = 0.0
        for i in range(num_blocks):
            block_start = i * pattern_size
            block_end = block_start + pattern_size
            block_data = binary_str[block_start: block_end]
            int_rep = int(block_data, 2)

            if i < init_bits:
                vobs[int_rep] = i + 1
            else:
                initial = vobs[int_rep]
                vobs[int_rep] = i + 1
                cumsum += log(i - initial + 1, 2)

        phi = cumsum / test_bits
        stat = abs(phi - expected[pattern_size]) / (sqrt(2) * sigma)
        p_value = erfc(stat)
        es_aleatorio = p_value >= 0.01

        return phi, p_value, es_aleatorio
    else:
        return 0.0, -1.0, False
