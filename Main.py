from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Frame, Text, Toplevel, messagebox, PhotoImage, Checkbutton
import os
from funciones import abrir_modal_config, guardar_valor_m, cargar_valor_m, seleccionar_todo
from T2FrecuencyWithinABlock import block_frequency

# Crear la ventana principal
root = Tk()
root.title("Pruebas NIST - Pruebas de Aleatoriedad")
root.geometry("1200x900")
root.configure(bg="#2E2A47")
root.state('zoomed')  # Maximizar la ventana
root.resizable(False, False)  # Desactivar el redimensionamiento

# Cargar imagen para el botón de configuración
config_image = PhotoImage(file="config.png").subsample(25, 25)  # Ajustar tamaño de la imagen

# Crear el frame principal
main_frame = Frame(root, bg="#2E2A47")
main_frame.pack(fill="both", expand=True)

# Crear las variables para los resultados de las pruebas (p-valores)
resultados = {i: StringVar() for i in range(1, 16)}
aleatorio_texto = {i: StringVar() for i in range(1, 16)}

# Crear las variables para los Checkbuttons (selección de pruebas)
check_vars = {i: IntVar() for i in range(1, 16)}

# Crear el frame para las pruebas
frame_pruebas = Frame(main_frame, bg="#2E2A47", bd=1, relief="solid")
frame_pruebas.pack(side="left", padx=30, pady=20, fill="both", expand=True)  # Añadido un margen de 30px

# Configuración del estilo para etiquetas y resultados
label_style = {"font": ("Helvetica", 12, "bold"), "fg": "#FFFFFF", "bg": "#3B2C6A", "bd": 1, "relief": "solid"}
result_style = {"font": ("Helvetica", 12), "fg": "#F4C8FF", "bg": "#2E2A47", "bd": 1, "relief": "solid"}

# Crear el frame donde se mostrarán las pruebas y resultados
frame_canvas_pruebas = Frame(frame_pruebas, bg="#2E2A47")
frame_canvas_pruebas.pack(fill="both", expand=True)

# Colocar las cabeceras
Label(frame_canvas_pruebas, text="Prueba", **label_style, width=45).grid(row=0, column=0, padx=5, pady=(0, 10), sticky="w")
Label(frame_canvas_pruebas, text="Resultado", **label_style, width=40).grid(row=0, column=1, padx=5, pady=(0, 10), sticky="w")
Label(frame_canvas_pruebas, text="Aleatoriedad", **label_style, width=20).grid(row=0, column=2, padx=5, pady=(0, 10), sticky="w")

# Lista de pruebas con sus identificadores
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

# Agregar las pruebas y sus resultados
row = 1
for label_text, test_id in pruebas:
    # Botón de configuración
    if test_id == 2:  # Añadir el modal solo al botón de la prueba 2
        Button(frame_canvas_pruebas, image=config_image, bg="#2E2A47", bd=0, command=lambda: abrir_modal_config(root)).grid(row=row, column=0, sticky="w", padx=(0, 5), pady=5)
    else:
        Button(frame_canvas_pruebas, image=config_image, bg="#2E2A47", bd=0).grid(row=row, column=0, sticky="w", padx=(0, 5), pady=5)

    # Checkbutton para seleccionar pruebas
    Checkbutton(frame_canvas_pruebas, text=label_text, variable=check_vars[test_id], font=("Helvetica", 12), bg="#2E2A47", fg="#F4C8FF", selectcolor="#3B2C6A", bd=1, relief="solid").grid(row=row, column=0, sticky="w", padx=(30, 5), pady=5)

    # Mostrar el resultado
    if test_id == 14 or test_id == 15:
        text_widget = Text(frame_canvas_pruebas, height=5, width=40, font=("Helvetica", 12), fg="#F4C8FF", bg="#2E2A47", bd=1, relief="solid")
        text_widget.grid(row=row, column=1, pady=5)
        resultados[test_id] = text_widget
    else:
        Label(frame_canvas_pruebas, textvariable=resultados[test_id], **result_style, width=40, anchor="w").grid(row=row, column=1, pady=5)

    # Mostrar si el resultado es aleatorio o no
    Label(frame_canvas_pruebas, textvariable=aleatorio_texto[test_id], **result_style, width=20, anchor="w").grid(row=row, column=2, pady=5)
    row += 1

# Función para ejecutar la prueba 2 y actualizar el resultado en la interfaz
def ejecutar_prueba_2():
    secuencia_binaria = entrada_binario.get()  # Obtener la secuencia binaria de la entrada
    valor_m = cargar_valor_m()  # Cargar el valor M desde el archivo
    if secuencia_binaria and valor_m:  # Verificar que la secuencia no esté vacía y que el valor M esté cargado
        try:
            valor_m = int(valor_m)  # Convertir valor_m a entero
        except ValueError:
            messagebox.showerror("Error", "El valor de M no es un número válido.")
            return  # Salir de la función si el valor de M no es válido

        p_val, is_random = block_frequency(secuencia_binaria, valor_m)

        # Actualizar el resultado de la prueba 2 en el Label correspondiente
        resultados[2].set(f"P-valor: {p_val:.30f}")  # Formateamos el p-valor a 5 decimales
        aleatorio_texto[2].set("Aleatorio" if is_random else "No Aleatorio")  # Dependiendo de 'is_random', actualizamos el texto



# Función para ejecutar todas las pruebas seleccionadas
def ejecutar_pruebas_seleccionadas():
    for test_id, var in check_vars.items():
        if var.get() == 1:  # Si la prueba está seleccionada
            if test_id == 2:  # Ejecutar la prueba 2
                ejecutar_prueba_2()
            # Agregar más condiciones para otras pruebas según se necesite

# Frame para los controles de la columna derecha (ingreso de binario y botones)
frame_controls = Frame(main_frame, bg="#2E2A47", bd=1, relief="solid", width=300)
frame_controls.pack(side="right", padx=10, pady=20, fill="y")

# Apilar los controles en el lado derecho
frame_controls.columnconfigure(0, weight=1)
frame_controls.columnconfigure(1, weight=1)

# Crear los widgets en el frame de controles y apilarlos
Label(frame_controls, text="Introduce una secuencia binaria:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_binario = Entry(frame_controls, width=30, font=("Helvetica", 14), bd=2, relief="solid")
entrada_binario.pack(pady=10)

Label(frame_controls, text="Cantidad de bits aleatorios:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_cantidad_bits = Entry(frame_controls, width=10, font=("Helvetica", 14), bd=2, relief="solid")
entrada_cantidad_bits.pack(pady=10)

Button(frame_controls, text="Ejecutar Pruebas Seleccionadas", font=("Helvetica", 14), bg="#3B2C6A", fg="white", width=25, command=ejecutar_pruebas_seleccionadas).pack(pady=10)
Button(frame_controls, text="Generar Secuencia Aleatoria", font=("Helvetica", 14), bg="#3B2C6A", fg="white", width=25).pack(pady=10)

# Iniciar el loop de la interfaz gráfica
root.mainloop()
