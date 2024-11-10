from tkinter import Tk, Label, Button, Entry, StringVar, Checkbutton, IntVar, Frame, filedialog, Canvas, Scrollbar
import random


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

# Crear la ventana principal
root = Tk()
root.title("Pruebas NIST - Pruebas de Aleatoriedad")
root.geometry("1200x900")  # Ajusta el tamaño para hacerlo más largo y un poco más alto
root.configure(bg="#2E2A47")  # Fondo oscuro suave
root.resizable(False, False)  # Desactivar el redimensionamiento

# Crear las variables para los resultados individuales
resultados = {i: StringVar() for i in range(1, 16)}
aleatorio_texto = {i: StringVar() for i in range(1, 16)}

# Crear las variables para los Checkbuttons
check_vars = {i: IntVar() for i in range(1, 16)}

# Crear el frame para las pruebas
frame = Frame(root, bg="#2E2A47", bd=1, relief="solid")
frame.pack(pady=20)

# Configuración del estilo
label_style = {"font": ("Helvetica", 12, "bold"), "fg": "#FFFFFF", "bg": "#3B2C6A", "bd": 1, "relief": "solid"}
result_style = {"font": ("Helvetica", 12), "fg": "#F4C8FF", "bg": "#2E2A47", "bd": 1, "relief": "solid"}

# Crear un Canvas con Scrollbar
canvas = Canvas(frame, bg="#2E2A47", height=500, width=1100)
scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

# Crear un frame dentro del canvas para almacenar las etiquetas
frame_canvas = Frame(canvas, bg="#2E2A47")
canvas.create_window((0, 0), window=frame_canvas, anchor="nw")

# Colocar las cabeceras en el canvas
Label(frame_canvas, text="Prueba", **label_style, width=50).grid(row=0, column=0, padx=5, pady=(0, 10), sticky="w")
Label(frame_canvas, text="Resultado", **label_style, width=40).grid(row=0, column=1, padx=5, pady=(0, 10), sticky="w")
Label(frame_canvas, text="Aleatoriedad", **label_style, width=20).grid(row=0, column=2, padx=5, pady=(0, 10), sticky="w")

# Lista de pruebas con identificadores
pruebas = [
    ("1. Frequency (Monobit) Test", 1),
    ("2. Frequency Test within a Block", 2),
    ("3. Runs Test", 3),
    ("4. Longest Run of Ones in a Block Test", 4),
    ("5. Binary Matrix Rank Test", 5),
    ("6. Discrete Fourier Transform (Spectral) Test", 6),
    ("7. Non-overlapping Template Matching Test", 7),
    ("8. Overlapping Template Matching Test", 8),
    ("9. Maurer's Universal Statistical Test", 9),
    ("10. Linear Complexity Test", 10),
    ("11. Serial Test", 11),
    ("12. Approximate Entropy Test", 12),
    ("13. Cumulative Sums (Cusum) Test", 13),
    ("14. Random Excursions Test", 14),
    ("15. Random Excursions Variant Test", 15),
]

# Agregar las pruebas y sus resultados dentro del Canvas
row = 1
for label_text, test_id in pruebas:
    Checkbutton(frame_canvas, text=label_text, variable=check_vars[test_id], font=("Helvetica", 12), bg="#2E2A47", fg="#F4C8FF", selectcolor="#3B2C6A", bd=1, relief="solid").grid(row=row, column=0, sticky="w", pady=5)
    Label(frame_canvas, textvariable=resultados[test_id], **result_style, width=40, anchor="w").grid(row=row, column=1, pady=5)
    Label(frame_canvas, textvariable=aleatorio_texto[test_id], **result_style, width=20, anchor="w").grid(row=row, column=2, pady=5)
    row += 1

# Actualizar el tamaño del canvas para permitir el desplazamiento
frame_canvas.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Configurar el scrollbar
scrollbar.config(command=canvas.yview)

# Colocar el scrollbar y el canvas en el frame
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Entrada para la secuencia binaria
Label(root, text="Introduce una secuencia binaria:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_binario = Entry(root, width=50, font=("Helvetica", 14), bd=2, relief="solid")
entrada_binario.pack(pady=10)

Label(root, text="Cantidad de bits aleatorios:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_cantidad_bits = Entry(root, width=10, font=("Helvetica", 14), bd=2, relief="solid")
entrada_cantidad_bits.pack(pady=10)

# Función para seleccionar un archivo binario
def seleccionar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            binary_data = file.read().strip()
            entrada_binario.delete(0, "end")
            entrada_binario.insert(0, binary_data)



# Función para generar una secuencia binaria aleatoria
def generarbinario_aleatorio():
    cantidad_bits = entrada_cantidad_bits.get()
    if cantidad_bits.isdigit():
        cantidad_bits = int(cantidad_bits)
        bits_aleatorios = ''.join(random.choice('01') for _ in range(cantidad_bits))
        entrada_binario.delete(0, "end")
        entrada_binario.insert(0, bits_aleatorios)
    else:
        entrada_binario.delete(0, "end")
        entrada_binario.insert(0, "Por favor, ingrese un número válido")

# Botón para seleccionar un archivo binario
boton_seleccionar_archivo = Button(root, text="Seleccionar Archivo Binario", command=seleccionar_archivo, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_seleccionar_archivo.pack(pady=10)

# Botón para generar binario aleatorio
boton_generar_aleatorio = Button(root, text="Generar Binario Aleatorio", command=generarbinario_aleatorio, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_generar_aleatorio.pack(pady=10)

# Función para ejecutar las pruebas seleccionadas
def calcular_pruebas():
    selected_tests = [test_id for test_id, var in check_vars.items() if var.get() == 1]
    esLista = 0
    if selected_tests:
        bits = [int(b) for b in entrada_binario.get().strip()]
        
        # Ejecutar pruebas seleccionadas
        for test_id in selected_tests:
            if test_id == 1:
                p_valor, es_aleatorio = prueba_monobit(bits)
                esLista=0
            elif test_id == 2:  # Block Frequency Test
                binary_data = ''.join(map(str, bits))  # Convertir lista de bits a cadena binaria
                p_valor = block_frequency(binary_data, block_size=128)  # Pasar la cadena binaria correctamente
                es_aleatorio = p_valor >= 0.01  # Si p-valor >= 0.01 es aleatorio
                esLista=0
            elif test_id == 3:
                p_valor, es_aleatorio = count_ones_zeroes(bits)
                esLista=0
            elif test_id == 4:
                p_valor, es_aleatorio = prueba_corrida_mas_larga(bits)
                esLista=0
            elif test_id == 5:
                try:
                    p_valor, es_aleatorio = prueba_rango_matriz_binaria(bits,32)
                    esLista=0
                except ValueError:
                    p_valor, es_aleatorio = 0.01, False
                    esLista=0
            elif test_id == 6:
                p_valor, es_aleatorio = transformada_fourier_discreta_nist(bits)
                esLista=0
            elif test_id == 7:
                p_valor, es_aleatorio = non_overlapping_template_matching_test(bits)
                esLista=0
            elif test_id == 8:
                datos_binarios = ''.join(map(str, bits))
                p_valor, es_aleatorio = overlappingTemplateMachine(datos_binarios, verbose=False, pattern_size=9, block_size=1032)
                esLista=0
            elif test_id == 9:
                p_valor, es_aleatorio = maurers_universal_statistical_test(bits)
                esLista=0
            elif test_id == 10:
                try:
                    p_valor, es_aleatorio = prueba_complejidad_lineal(bits)
                    esLista=0
                except ValueError:
                    p_valor, es_aleatorio = 0.01, False
                    esLista=0
            elif test_id==11:
                p_valor_lista, es_aleatorio = serial_test(bits,None)
                esLista=1
            elif test_id == 12:
                _, p_valor, es_aleatorio = approximate_entropy_test(bits)
                esLista=0
            elif test_id == 13:
                datos_binarios = ''.join(map(str, bits))
                p_valor, es_aleatorio = cumulative_sums_test(datos_binarios, mode=0, verbose=False)
                esLista=0
            elif test_id== 14:
                p_valor_lista, es_aleatorio = random_excursion_test(bits)
                esLista=1
            elif test_id == 15:
                p_valor_lista, es_aleatorio = random_excursion_variant_test(bits)
                esLista = 1
            else:
                p_valor, es_aleatorio = 0.01, False  # Valores de ejemplo
                esLista=0
            
            # Actualizar resultados en la interfaz
            if esLista == 1:
                resultados[test_id].set('\n'.join([f"p-valor: {p:.15f}" for p in p_valor_lista]))
            else:
                resultados[test_id].set(f"p-valor: {p_valor:.15f}")
            aleatorio_texto[test_id].set("Aleatorio" if es_aleatorio else "No Aleatorio")

        # Actualizar la región de desplazamiento del canvas
        frame_canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    else:
        for var in resultados.values():
            var.set("Selecciona al menos una prueba.")

# Botón para ejecutar las pruebas
boton_calcular = Button(root, text="Calcular Pruebas", command=calcular_pruebas, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_calcular.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()