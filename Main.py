from tkinter import Tk, Label, Button, Entry, StringVar, Checkbutton, IntVar, Frame, filedialog
import random

from T10_Linear_Complexity_test import linear_complexity_test
from T1_Frequency_Test import monobit_test
from T4_longest_run import longest_run_ones_test
from T12ApproximateEntropy import approximate_entropy_test
from T5_binary_matrix import binary_matrix_rank_test
from T6_Discrete_Fourier_transform import nist_discrete_fourier_transform
from T9MaurersUniversalStatistical import maurers_universal_statistical_test

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

# Crear el frame para las pruebas y resultados en formato de tabla
frame = Frame(root, bg="#2E2A47", bd=1, relief="solid")
frame.pack(pady=20)

# Configuración del estilo
label_style = {"font": ("Helvetica", 12, "bold"), "fg": "#FFFFFF", "bg": "#3B2C6A", "bd": 1, "relief": "solid"}
result_style = {"font": ("Helvetica", 12), "fg": "#F4C8FF", "bg": "#2E2A47", "bd": 1, "relief": "solid"}

# Cabecera de la tabla, con bordes en las columnas
Label(frame, text="Prueba", **label_style, width=50).grid(row=0, column=0, padx=5, pady=(0, 10), sticky="w")
Label(frame, text="Resultado", **label_style, width=40).grid(row=0, column=1, padx=5, pady=(0, 10), sticky="w")
Label(frame, text="Aleatoriedad", **label_style, width=20).grid(row=0, column=2, padx=5, pady=(0, 10), sticky="w")

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

# Agregar pruebas y sus resultados a la interfaz, con bordes en las columnas
row = 1
for label_text, test_id in pruebas:
    Checkbutton(frame, text=label_text, variable=check_vars[test_id], font=("Helvetica", 12), bg="#2E2A47", fg="#F4C8FF", selectcolor="#3B2C6A", bd=1, relief="solid").grid(row=row, column=0, sticky="w", pady=5)
    Label(frame, textvariable=resultados[test_id], **result_style, width=40, anchor="w").grid(row=row, column=1, pady=5)
    Label(frame, textvariable=aleatorio_texto[test_id], **result_style, width=20, anchor="w").grid(row=row, column=2, pady=5)
    row += 1

# Entrada para la secuencia binaria
Label(root, text="Introduce una secuencia binaria:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_binario = Entry(root, width=50, font=("Helvetica", 14), bd=2, relief="solid")
entrada_binario.pack(pady=10)

# Función para seleccionar un archivo binario
def seleccionar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            binary_data = file.read().strip()
            entrada_binario.delete(0, "end")
            entrada_binario.insert(0, binary_data)

# Función para generar una secuencia binaria aleatoria
def generar_binario_aleatorio():
    # Generar una secuencia de 1000 bits aleatorios (suficiente para la prueba de Maurer)
    random_bits = ''.join(random.choice('01') for _ in range(1000))
    entrada_binario.delete(0, "end")
    entrada_binario.insert(0, random_bits)

# Botón para seleccionar un archivo binario
boton_seleccionar_archivo = Button(root, text="Seleccionar Archivo Binario", command=seleccionar_archivo, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_seleccionar_archivo.pack(pady=10)

# Botón para generar binario aleatorio
boton_generar_aleatorio = Button(root, text="Generar Binario Aleatorio", command=generar_binario_aleatorio, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_generar_aleatorio.pack(pady=10)

# Función para ejecutar pruebas seleccionadas
def calcular_pruebas():
    selected_tests = [test_id for test_id, var in check_vars.items() if var.get() == 1]
    if selected_tests:
        bits = [int(b) for b in entrada_binario.get().strip()]
        
        # Ejecutar pruebas seleccionadas
        for test_id in selected_tests:
            if test_id == 1:
                p_valor, es_aleatorio = monobit_test(bits)
            elif test_id == 4:
                p_valor, es_aleatorio = longest_run_ones_test(bits)
            elif test_id == 5:
                try:
                    p_valor, es_aleatorio = binary_matrix_rank_test(bits, matrix_size=32)
                except ValueError:
                    p_valor, es_aleatorio = 0.01, False
            elif test_id == 6:
                p_valor, es_aleatorio = nist_discrete_fourier_transform(bits)
            elif test_id == 9:
                _, p_valor, es_aleatorio = maurers_universal_statistical_test(bits)
            elif test_id == 10:
                try:
                    p_valor, es_aleatorio = linear_complexity_test(bits)
                except ValueError:
                    p_valor, es_aleatorio = 0.01, False
            elif test_id == 12:
                _, p_valor, es_aleatorio = approximate_entropy_test(bits)
            else:
                # Aquí se deben implementar y llamar las funciones para las demás pruebas
                p_valor, es_aleatorio = 0.01, False  # Valores de ejemplo
            
            # Actualizar resultados en la interfaz
            resultados[test_id].set(f"p-valor: {p_valor:.15f}")
            aleatorio_texto[test_id].set("Aleatorio" if es_aleatorio else "No Aleatorio")
    else:
        for var in resultados.values():
            var.set("Selecciona al menos una prueba.")

# Botón para ejecutar las pruebas
boton_calcular = Button(root, text="Calcular Pruebas", command=calcular_pruebas, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_calcular.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
