import random
from tkinter import filedialog
from T1_Frequency_Test import prueba_monobit
from T2FrecuencyWithinABlock import block_frequency
from T3_runs_test import count_ones_zeroes
from T4_longest_run import prueba_corrida_mas_larga
from T12ApproximateEntropy import approximate_entropy_test
from T5_binary_matrix import prueba_rango_matriz_binaria
from T6_Discrete_Fourier_transform import transformada_fourier_discreta_nist
from T7_non_overlapping_template_matching_test import non_overlapping_template_matching_test
from T8OverlappingTemplateMachine import overlappingTemplateMachine
from T9MaurersUniversalStatistical import maurers_universal_statistical_test
from T10_Linear_Complexity_test import prueba_complejidad_lineal
from T11_serial_test import serial_test
from T12ApproximateEntropy import approximate_entropy_test
from T13CumulativeSum import cumulative_sums_test
from T14_random_excursion_test import random_excursion_test
from T15_random_excursion_variant_test import random_excursion_variant_test


def seleccionar_archivo(entrada_binario):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            binary_data = file.read().strip()
            entrada_binario.delete(0, "end")
            entrada_binario.insert(0, binary_data)

def generarbinario_aleatorio(entrada_cantidad_bits, entrada_binario):
    cantidad_bits = entrada_cantidad_bits.get()
    if cantidad_bits.isdigit():
        cantidad_bits = int(cantidad_bits)
        bits_aleatorios = ''.join(random.choice('01') for _ in range(cantidad_bits))
        entrada_binario.delete(0, "end")
        entrada_binario.insert(0, bits_aleatorios)
    else:
        entrada_binario.delete(0, "end")
        entrada_binario.insert(0, "Por favor, ingrese un número válido")

# Función para realizar las pruebas
from tkinter import Text  # Asegúrate de importar Text

from tkinter import Text  # Asegúrate de importar Text

def calcular_pruebas(bits, selected_tests, resultados, aleatorio_texto, frame_canvas):
    esLista = 0
    if selected_tests:
        for test_id in selected_tests:
            if test_id == 1:
                p_valor, es_aleatorio = prueba_monobit(bits)
                esLista = 0
            elif test_id == 2:
                binary_data = ''.join(map(str, bits))
                p_valor = block_frequency(binary_data, block_size=128)
                es_aleatorio = p_valor >= 0.01
                esLista = 0
            elif test_id == 3:
                p_valor, es_aleatorio = count_ones_zeroes(bits)
                esLista = 0
            elif test_id == 4:
                p_valor, es_aleatorio = prueba_corrida_mas_larga(bits)
                esLista = 0
            elif test_id == 5:
                try:
                    p_valor, es_aleatorio = prueba_rango_matriz_binaria(bits, 32)
                    esLista = 0
                except ValueError:
                    p_valor, es_aleatorio = 0.01, False
                    esLista = 0
            elif test_id == 6:
                p_valor, es_aleatorio = transformada_fourier_discreta_nist(bits)
                esLista = 0
            elif test_id == 7:
                p_valor, es_aleatorio = non_overlapping_template_matching_test(bits)
                esLista = 0
            elif test_id == 8:
                datos_binarios = ''.join(map(str, bits))
                p_valor, es_aleatorio = overlappingTemplateMachine(datos_binarios, verbose=False, pattern_size=9, block_size=1032)
                esLista = 0
            elif test_id == 9:
                p_valor, es_aleatorio = maurers_universal_statistical_test(bits)
                esLista = 0
            elif test_id == 10:
                try:
                    p_valor, es_aleatorio = prueba_complejidad_lineal(bits)
                    esLista = 0
                except ValueError:
                    p_valor, es_aleatorio = 0.01, False
                    esLista = 0
            elif test_id == 11:
                p_valor_lista, es_aleatorio = serial_test(bits, None)
                esLista = 1
            elif test_id == 12:
                _, p_valor, es_aleatorio = approximate_entropy_test(bits)
                esLista = 0
            elif test_id == 13:
                datos_binarios = ''.join(map(str, bits))
                p_valor, es_aleatorio = cumulative_sums_test(datos_binarios, mode=0, verbose=False)
                esLista = 0
            elif test_id == 14:
                p_valor_lista, es_aleatorio = random_excursion_test(bits)
                esLista = 1
            elif test_id == 15:
                p_valor_lista, es_aleatorio = random_excursion_variant_test(bits)
                esLista = 1
            else:
                p_valor, es_aleatorio = 0.01, False
                esLista = 0

            # Actualizar resultados
            if esLista == 1:
                # Limpiar el widget de texto antes de insertar nuevos p-valores
                resultados[test_id].delete(1.0, "end")  # Limpiar el Text widget
                resultados[test_id].insert("1.0", '\n'.join([f"p-valor: {p:.15f}" for p in p_valor_lista]))  # Mostrar los p-valores
            else:
                # Para pruebas con un solo p-valor, simplemente mostramos uno
                resultados[test_id].set(f"p-valor: {p_valor:.15f}")
            
            aleatorio_texto[test_id].set("Aleatorio" if es_aleatorio else "No Aleatorio")
        
        # Actualizar el tamaño del canvas
        frame_canvas.update_idletasks()
        frame_canvas.config(scrollregion=frame_canvas.bbox("all"))
    else:
        for var in resultados.values():
            var.set("Selecciona al menos una prueba.")