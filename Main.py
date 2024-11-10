from tkinter import Tk, Label, Button, Entry, StringVar, Checkbutton, IntVar, Frame, filedialog
import random

from T10_Linear_Complexity_test import prueba_complejidad_lineal
from T12ApproximateEntropy import approximate_entropy_test
from T1_Frequency_Test import prueba_monobit
from T4_longest_run import prueba_corrida_mas_larga
from T5_binary_matrix import prueba_rango_matriz_binaria
from T6_Discrete_Fourier_transform import transformada_fourier_discreta_nist
from T9MaurersUniversalStatistical import maurers_universal_statistical_test
from T8OverlappingTemplateMachine import overlappingTemplateMachine
from T2FrecuencyWithinABlock import block_frequency
from T13CumulativeSum import cumulative_sums_test

# Crear la ventana principal
ventana = Tk()
ventana.title("Pruebas NIST - Pruebas de Aleatoriedad")
ventana.geometry("1200x1200")  # Ajusta el tamaño para hacerlo más largo y un poco más alto
ventana.configure(bg="#2E2A47")  # Fondo oscuro suave
ventana.resizable(True, True)  # Desactivar el redimensionamiento

# Crear las variables para los resultados individuales
resultados = {i: StringVar() for i in range(1, 16)}
aleatorio_texto = {i: StringVar() for i in range(1, 16)}

# Crear las variables para los Checkbuttons
check_vars = {i: IntVar() for i in range(1, 16)}

# Crear el frame para las pruebas y resultados en formato de tabla
marco = Frame(ventana, bg="#2E2A47", bd=1, relief="solid")
marco.pack(pady=20)

# Configuración del estilo
estilo_etiqueta = {"font": ("Helvetica", 12, "bold"), "fg": "#FFFFFF", "bg": "#3B2C6A", "bd": 1, "relief": "solid"}
estilo_resultado = {"font": ("Helvetica", 12), "fg": "#F4C8FF", "bg": "#2E2A47", "bd": 1, "relief": "solid"}

# Cabecera de la tabla, con bordes en las columnas
Label(marco, text="Prueba", **estilo_etiqueta, width=50).grid(row=0, column=0, padx=5, pady=(0, 10), sticky="w")
Label(marco, text="Resultado", **estilo_etiqueta, width=40).grid(row=0, column=1, padx=5, pady=(0, 10), sticky="w")
Label(marco, text="Aleatoriedad", **estilo_etiqueta, width=20).grid(row=0, column=2, padx=5, pady=(0, 10), sticky="w")

# Lista de pruebas con identificadores
pruebas = [
    ("1. Prueba de Frecuencia (Monobit)", 1),
    ("2. Prueba de Frecuencia en un Bloque", 2),
    ("3. Prueba de Corridas", 3),
    ("4. Prueba del Longest Run de Unos", 4),
    ("5. Prueba de Rango de Matriz Binaria", 5),
    ("6. Prueba de Transformada Discreta de Fourier", 6),
    ("7. Prueba de Plantillas no Superpuestas", 7),
    ("8. Prueba de Plantillas Superpuestas", 8),
    ("9. Prueba Estadística Universal de Maurer", 9),
    ("10. Prueba de Complejidad Lineal", 10),
    ("11. Prueba Serial", 11),
    ("12. Prueba de Entropía Aproximada", 12),
    ("13. Prueba de Sumas Cumulativas (Cusum)", 13),
    ("14. Prueba de Excursiones Aleatorias", 14),
    ("15. Prueba Variante de Excursiones Aleatorias", 15),
]

# Agregar pruebas y sus resultados a la interfaz, con bordes en las columnas
fila = 1
for texto_etiqueta, id_prueba in pruebas:
    Checkbutton(marco, text=texto_etiqueta, variable=check_vars[id_prueba], font=("Helvetica", 12), bg="#2E2A47", fg="#F4C8FF", selectcolor="#3B2C6A", bd=1, relief="solid").grid(row=fila, column=0, sticky="w", pady=5)
    Label(marco, textvariable=resultados[id_prueba], **estilo_resultado, width=40, anchor="w").grid(row=fila, column=1, pady=5)
    Label(marco, textvariable=aleatorio_texto[id_prueba], **estilo_resultado, width=20, anchor="w").grid(row=fila, column=2, pady=5)
    fila += 1

# Entrada para la secuencia binaria (común para todas las pruebas)
Label(ventana, text="Introduce una secuencia binaria:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_binario = Entry(ventana, width=50, font=("Helvetica", 14), bd=2, relief="solid")
entrada_binario.pack(pady=10)

# Entrada para la cantidad de bits aleatorios a generar (común para todas las pruebas)
Label(ventana, text="Cantidad de bits aleatorios:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_cantidad_bits = Entry(ventana, width=10, font=("Helvetica", 14), bd=2, relief="solid")
entrada_cantidad_bits.pack(pady=10)

# Función para seleccionar un archivo binario
def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if ruta_archivo:
        with open(ruta_archivo, "r") as archivo:
            datos_binarios = archivo.read().strip()
            entrada_binario.delete(0, "end")
            entrada_binario.insert(0, datos_binarios)

# Función para generar una secuencia binaria aleatoria
def generar_binario_aleatorio():
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
boton_seleccionar_archivo = Button(ventana, text="Seleccionar Archivo Binario", command=seleccionar_archivo, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_seleccionar_archivo.pack(pady=10)

# Botón para generar binario aleatorio
boton_generar_aleatorio = Button(ventana, text="Generar Binario Aleatorio", command=generar_binario_aleatorio, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_generar_aleatorio.pack(pady=10)

# Sección de la prueba Overlapping Template Matching
marco_overlapping = Frame(ventana, bg="#2E2A47", bd=1, relief="solid")
marco_overlapping.pack(pady=20, fill="x")

# Función para ejecutar las pruebas
def calcular_pruebas():
    pruebas_seleccionadas = [id_prueba for id_prueba, var in check_vars.items() if var.get() == 1]
    if pruebas_seleccionadas:
        bits = [int(b) for b in entrada_binario.get().strip()]

        # Procesar los resultados de las pruebas
        for test_id in pruebas_seleccionadas:
            if test_id == 1:
                p_valor, es_aleatorio = prueba_monobit(bits)
            elif test_id == 2:  # Block Frequency Test
                binary_data = ''.join(map(str, bits))  # Convertir lista de bits a cadena binaria
                p_valor = block_frequency(binary_data, block_size=128)  # Pasar la cadena binaria correctamente
                es_aleatorio = p_valor >= 0.01  # Si p-valor >= 0.01 es aleatorio
            elif test_id == 3:
                # p_valor, es_aleatorio = longest_run_ones_test(bits)
                p_valor, es_aleatorio = -1, False
            elif test_id == 4:
                p_valor, es_aleatorio = prueba_corrida_mas_larga(bits)
            elif test_id == 5:
                p_valor, es_aleatorio = prueba_rango_matriz_binaria(bits)
            elif test_id == 6:
                p_valor, es_aleatorio = transformada_fourier_discreta_nist(bits)
            elif test_id == 9:
                p_valor, es_aleatorio = maurers_universal_statistical_test(bits)
            elif test_id == 10:
                try:
                    p_valor, es_aleatorio = prueba_complejidad_lineal(bits)
                except Exception as e:
                    p_valor, es_aleatorio = -1, False
            elif test_id == 12:
                _, p_valor, es_aleatorio = approximate_entropy_test(bits)
            elif test_id == 8:
                datos_binarios = ''.join(map(str, bits))
                p_valor, es_aleatorio = overlappingTemplateMachine(datos_binarios, verbose=False, pattern_size=9, block_size=1032)
            elif test_id == 13:
                datos_binarios = ''.join(map(str, bits))
                p_valor, es_aleatorio = cumulative_sums_test(datos_binarios, mode=0, verbose=False)

            if p_valor is not None:
                try:
                    p_valor = float(p_valor)
                    resultados[test_id].set(f"p-valor: {p_valor:.15f}")
                except ValueError:
                    resultados[test_id].set("Error en el p-valor")
                aleatorio_texto[test_id].set("Aleatorio" if es_aleatorio else "No Aleatorio")
            else:
                resultados[test_id].set("Error en el p-valor")
                aleatorio_texto[test_id].set("No disponible")
    else:
        for var in resultados.values():
            var.set("Selecciona al menos una prueba.")

# Botón para ejecutar las pruebas
boton_calcular = Button(ventana, text="Calcular Pruebas", command=calcular_pruebas, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_calcular.pack(pady=10)

# Ejecutar la interfaz gráfica
ventana.mainloop()
