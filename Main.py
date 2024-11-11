from tkinter import Tk, Label, Button, Entry, StringVar, Checkbutton, IntVar, Frame, filedialog, Canvas, Scrollbar, Text
import random
from funciones import calcular_pruebas

# Crear la ventana principal
root = Tk()
root.title("Pruebas NIST - Pruebas de Aleatoriedad")
root.geometry("1200x900")
root.configure(bg="#2E2A47")
root.state('zoomed')  # Maximizar la ventana
root.resizable(False, False)  # Desactivar el redimensionamiento

# Crear un Canvas con Scrollbar principal
main_canvas = Canvas(root, bg="#2E2A47")
main_scrollbar = Scrollbar(root, orient="vertical", command=main_canvas.yview)
main_canvas.config(yscrollcommand=main_scrollbar.set)

# Crear un frame dentro del canvas principal
main_frame = Frame(main_canvas, bg="#2E2A47")
main_canvas.create_window((0, 0), window=main_frame, anchor="nw")

# Configurar el scrollbar principal
main_scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

# Crear las variables para los resultados individuales
resultados = {i: StringVar() for i in range(1, 16)}
aleatorio_texto = {i: StringVar() for i in range(1, 16)}

# Crear las variables para los Checkbuttons
check_vars = {i: IntVar() for i in range(1, 16)}

# Crear el frame para las pruebas
frame = Frame(main_frame, bg="#2E2A47", bd=1, relief="solid")
frame.pack(pady=20)

# Configuración del estilo
label_style = {"font": ("Helvetica", 12, "bold"), "fg": "#FFFFFF", "bg": "#3B2C6A", "bd": 1, "relief": "solid"}
result_style = {"font": ("Helvetica", 12), "fg": "#F4C8FF", "bg": "#2E2A47", "bd": 1, "relief": "solid"}

# Crear un Canvas con Scrollbar para las pruebas
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
    if test_id == 14:
        text_widget = Text(frame_canvas, height=5, width=40, font=("Helvetica", 12), fg="#F4C8FF", bg="#2E2A47", bd=1, relief="solid")
        text_widget.grid(row=row, column=1, pady=5)
        resultados[test_id] = text_widget
    else:
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
Label(main_frame, text="Introduce una secuencia binaria:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_binario = Entry(main_frame, width=50, font=("Helvetica", 14), bd=2, relief="solid")
entrada_binario.pack(pady=10)

Label(main_frame, text="Cantidad de bits aleatorios:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_cantidad_bits = Entry(main_frame, width=10, font=("Helvetica", 14), bd=2, relief="solid")
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

# Crear un frame para los botones
botones_frame = Frame(main_frame, bg="#2E2A47")
botones_frame.pack(pady=20)

# Botón para seleccionar un archivo binario
boton_seleccionar_archivo = Button(botones_frame, text="Seleccionar Archivo Binario", command=seleccionar_archivo, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_seleccionar_archivo.grid(row=0, column=0, padx=10)

# Botón para generar binario aleatorio
boton_generar_aleatorio = Button(botones_frame, text="Generar Binario Aleatorio", command=generarbinario_aleatorio, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_generar_aleatorio.grid(row=0, column=1, padx=10)

# Función para ejecutar las pruebas seleccionadas
def realizar_pruebas():
    bits = [int(b) for b in entrada_binario.get().strip()]
    selected_tests = [test_id for test_id in check_vars if check_vars[test_id].get() == 1]
    calcular_pruebas(bits, selected_tests, resultados, aleatorio_texto, frame_canvas)

# Botón para ejecutar las pruebas
boton_calcular = Button(botones_frame, text="Calcular Pruebas", command=realizar_pruebas, font=("Helvetica", 14), bg="#3B2C6A", fg="white", bd=0, relief="flat")
boton_calcular.grid(row=0, column=2, padx=10)

# Actualizar el tamaño del canvas principal para permitir el desplazamiento
main_frame.update_idletasks()
main_canvas.config(scrollregion=main_canvas.bbox("all"))

# Ejecutar la interfaz gráfica
root.mainloop()