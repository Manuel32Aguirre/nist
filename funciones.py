from tkinter import Toplevel, Label, Entry, Button, messagebox, Frame
import os
import random
from T2FrecuencyWithinABlock import block_frequency
import mpmath as mp
from T8OverlappingTemplateMatching import obtener_expansion_binaria_e, overlappingTemplateMachine
from T9MaurersUniversalStatistical import universal_test
from T3RunsTest import runs_test

def guardar_valor(valor, archivo):
    with open(archivo, "w") as file:
        file.write(valor)

def cargar_valor(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r") as file:
            return file.read().strip()
    return ""

def abrir_modal_config_prueba_2(root):
    modal = Toplevel(root)
    modal.title("Configuración de Prueba 2")
    modal.geometry("300x250")
    modal.configure(bg="#2E2A47")

    frame_entrada = Frame(modal, bg="#2E2A47")
    frame_entrada.pack(pady=10)
    Label(frame_entrada, text="M:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(side="left")
    entrada_m = Entry(frame_entrada, width=10, font=("Helvetica", 14), bd=2, relief="solid")
    entrada_m.pack(side="left", padx=5)
    entrada_m.insert(0, cargar_valor("configuracionDePruebas/configT2.txt"))

    def guardar_y_cerrar():
        valor = entrada_m.get()
        if valor.isdigit():
            guardar_valor(valor, "configuracionDePruebas/configT2.txt")
            modal.destroy()
            messagebox.showinfo("Configuración Guardada", "Valor de M guardado.")
        else:
            messagebox.showerror("Error", "Por favor, ingrese un valor válido para M.")

    Button(modal, text="Guardar", font=("Helvetica", 12), bg="#3B2C6A", fg="white", command=guardar_y_cerrar).pack(pady=10)

def insertar_texto_con_saltos(text_widget, texto, max_line_length=60):
    lines = [texto[i:i + max_line_length] for i in range(0, len(texto), max_line_length)]
    text_widget.delete('1.0', 'end')
    text_widget.insert('1.0', '\n'.join(lines) + '\n')
    text_widget.yview_moveto(1)

def abrir_modal_config_prueba_8(root, entrada_binario):
    modal = Toplevel(root)
    modal.title("Configuración de Prueba 8")
    modal.geometry("300x350")
    modal.configure(bg="#2E2A47")

    entradas = {}
    frame_entrada = Frame(modal, bg="#2E2A47")
    frame_entrada.pack(pady=10)
    Label(frame_entrada, text="Patrón (B):", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(side="left")
    entrada_patron = Entry(frame_entrada, width=20, font=("Helvetica", 14), bd=2, relief="solid")
    entrada_patron.pack(side="left", padx=5)
    entrada_patron.insert(0, cargar_valor("configuracionDePruebas/configT8_Patron.txt"))
    entradas["Patrón (B)"] = entrada_patron

    def guardar_y_cerrar():
        valor_patron = entrada_patron.get()
        if valor_patron:
            guardar_valor(valor_patron, "configuracionDePruebas/configT8_Patron.txt")
            modal.destroy()
            messagebox.showinfo("Configuración Guardada", "Valores guardados.")
        else:
            messagebox.showerror("Error", "El patrón no puede estar vacío.")

    Button(modal, text="Guardar", font=("Helvetica", 12), bg="#3B2C6A", fg="white", command=guardar_y_cerrar).pack(pady=10)
    Label(modal, text="Generar expansión binaria", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
    Label(modal, text="Número de bits:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=5)
    entrada_numero_bits = Entry(modal, width=10, font=("Helvetica", 14), bd=2, relief="solid")
    entrada_numero_bits.pack(pady=5)
    entrada_numero_bits.insert(0, cargar_valor("configuracionDePruebas/configT8_NumeroBits.txt"))
    entradas["Número de bits"] = entrada_numero_bits

    def generar_expansion_binaria_modal():
        n = entrada_numero_bits.get()
        if n.isdigit():
            bits = int(n)
            expansion = obtener_expansion_binaria_e(bits)
            entrada_binario.delete('1.0', 'end')
            insertar_texto_con_saltos(entrada_binario, expansion)

            archivo_expansion = os.path.join(os.getcwd(), "configuracionDePruebas", "configT8_expansionBinaria.txt")
            with open(archivo_expansion, "w") as file:
                file.write(expansion)

            messagebox.showinfo("Expansión Binaria Generada", f"La expansión binaria se ha cargado en el campo de secuencia binaria y guardado en {archivo_expansion}.")
        else:
            messagebox.showerror("Error", "Por favor, ingrese un número válido para los bits.")

    Button(modal, text="Generar Expansión Binaria", font=("Helvetica", 12), bg="#3B2C6A", fg="white", command=generar_expansion_binaria_modal).pack(pady=10)

def ejecutar_prueba_2(secuencia_binaria, resultados, aleatorio_texto):
    valor_m = cargar_valor("configuracionDePruebas/configT2.txt")
    secuencia_binaria_sin_saltos = secuencia_binaria.replace("\n", "")
    
    if secuencia_binaria_sin_saltos and valor_m.isdigit():
        p_val, is_random = block_frequency(secuencia_binaria_sin_saltos, int(valor_m))
        resultados[2].set(f"P-valor: {p_val:.17f}")
        aleatorio_texto[2].set("Aleatorio" if is_random else "No Aleatorio")
        
def ejecutar_prueba_3(secuencia_binaria, resultados, aleatorio_texto):
    p_val, is_random = runs_test(secuencia_binaria)
    print(f"el p val es {p_val}")
    resultados[3].set(f"P-valor: {p_val:.17f}")
    aleatorio_texto[3].set("Aleatorio" if is_random else "No Aleatorio")

def ejecutar_prueba_8(secuencia_binaria, resultados, aleatorio_texto):
    secuencia_binaria_sin_saltos = secuencia_binaria.replace("\n", "")
    pattern = cargar_valor("configuracionDePruebas/configT8_Patron.txt")
    
    if secuencia_binaria_sin_saltos and pattern:
        p_val, is_random = overlappingTemplateMachine(secuencia_binaria_sin_saltos, pattern)
        resultados[8].set(f"P-valor: {p_val:.17f}")
        aleatorio_texto[8].set("Aleatorio" if is_random else "No Aleatorio")
    else:
        messagebox.showerror("Error", "La secuencia o el patrón no son válidos.")

def ejecutar_prueba_9(secuencia_binaria, resultados, aleatorio_texto):
    # Cargar los valores de L y Q desde el archivo
    try:
        with open("configuracionDePruebas/configT9.txt", "r") as file:
            L = int(file.readline().strip())  # Leer el primer renglón como L
            Q = int(file.readline().strip())  # Leer el segundo renglón como Q
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo de configuración: {e}")
        return

    # Limpiar la secuencia binaria de saltos de línea y espacios innecesarios
    secuencia_binaria_sin_saltos = secuencia_binaria.replace("\n", "").replace(" ", "")
    
    if secuencia_binaria_sin_saltos and L > 0 and Q > 0:
        # Llamar a la función universal_test con epsilon (secuencia binaria), L y Q
        p_val, is_random = universal_test(secuencia_binaria_sin_saltos, L, Q)
        
        # Mostrar el p-valor en los resultados
        resultados[9].set(f"P-valor: {p_val:.17f}")
        
        # Indicar si la secuencia es aleatoria o no
        aleatorio_texto[9].set("Aleatorio" if is_random else "No Aleatorio")
    else:
        messagebox.showerror("Error", "La secuencia binaria o los valores de L y Q no son válidos.")


def ejecutar_pruebas_seleccionadas(check_vars, entrada_binario, resultados, aleatorio_texto):
    secuencia_binaria = entrada_binario.get("1.0", "end-1c")
    if check_vars[2].get():
        ejecutar_prueba_2(secuencia_binaria, resultados, aleatorio_texto)
    if check_vars[3].get():
        ejecutar_prueba_3(secuencia_binaria, resultados, aleatorio_texto)
    if check_vars[8].get():
        ejecutar_prueba_8(secuencia_binaria, resultados, aleatorio_texto)
    if check_vars[9].get():  # Verifica si la prueba 9 está seleccionada
        ejecutar_prueba_9(secuencia_binaria, resultados, aleatorio_texto)  # Llamada a la función de la prueba 9

def generar_secuencia_aleatoria(entrada_cantidad_bits, entrada_binario, max_line_length=60):
    cantidad_bits = entrada_cantidad_bits.get()
    if cantidad_bits.isdigit():
        secuencia_aleatoria = ''.join(str(random.randint(0, 1)) for _ in range(int(cantidad_bits)))
        entrada_binario.delete('1.0', 'end')
        insertar_texto_con_saltos(entrada_binario, secuencia_aleatoria, max_line_length)
    else:
        messagebox.showerror("Error", "Por favor, introduce un número válido de bits.")

def on_paste(entry_widget, event):
    texto = entry_widget.clipboard_get()
    texto_limpio = texto.replace("\n", "").replace(" ", "")
    entry_widget.delete("1.0", "end")
    entry_widget.insert("1.0", texto_limpio)
    return "break"

def abrir_modal_config_prueba_9(root):
    modal = Toplevel(root)
    modal.title("Configuración de Prueba 9")
    modal.geometry("300x250")
    modal.configure(bg="#2E2A47")

    frame_entrada = Frame(modal, bg="#2E2A47")
    frame_entrada.pack(pady=10)

    # Campo para L
    Label(frame_entrada, text="L:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(side="left")
    entrada_l = Entry(frame_entrada, width=10, font=("Helvetica", 14), bd=2, relief="solid")
    entrada_l.pack(side="left", padx=5)

    # Cargar valor de L desde el archivo
    valor_l = cargar_valor("configuracionDePruebas/configT9.txt")
    if valor_l:
        entrada_l.insert(0, valor_l.split('\n')[0])  # Asignar solo la primera línea a L

    # Campo para Q
    Label(frame_entrada, text="Q:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(side="left")
    entrada_q = Entry(frame_entrada, width=10, font=("Helvetica", 14), bd=2, relief="solid")
    entrada_q.pack(side="left", padx=5)

    # Cargar valor de Q desde el archivo
    if valor_l:
        valor_q = valor_l.split('\n')[1] if len(valor_l.split('\n')) > 1 else ""  # Asignar la segunda línea a Q
        entrada_q.insert(0, valor_q)

    def guardar_y_cerrar():
        valor_l = entrada_l.get()
        valor_q = entrada_q.get()
        
        # Validar que L y Q sean números válidos
        if valor_l.isdigit() and valor_q.isdigit():
            # Guardar L y Q en el archivo de configuración
            with open("configuracionDePruebas/configT9.txt", "w") as file:
                file.write(f"{valor_l}\n{valor_q}")  # Guardar L en la primera línea y Q en la segunda línea
            modal.destroy()
            messagebox.showinfo("Configuración Guardada", "Valores de L y Q guardados.")
        else:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos para L y Q.")

    # Botón para guardar la configuración
    Button(modal, text="Guardar", font=("Helvetica", 12), bg="#3B2C6A", fg="white", command=guardar_y_cerrar).pack(pady=10)

def abrir_modal_config_prueba_12(root):
    modal = Toplevel(root)
    modal.title("Configuración de Prueba 12")
    modal.geometry("300x250")
    modal.configure(bg="#2E2A47")

    frame_entrada = Frame(modal, bg="#2E2A47")
    frame_entrada.pack(pady=10)
    
    # Etiqueta y campo de entrada para el valor de entropía
    Label(frame_entrada, text="M:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(side="left")
    entrada_entropia = Entry(frame_entrada, width=10, font=("Helvetica", 14), bd=2, relief="solid")
    entrada_entropia.pack(side="left", padx=5)
    entrada_entropia.insert(0, cargar_valor("configuracionDePruebas/configT12.txt"))

    # Función para guardar el valor de entropía y cerrar el modal
    def guardar_y_cerrar():
        valor_entropia = entrada_entropia.get()
        try:
            # Convertir a float para verificar que sea un valor numérico válido
            valor_m = int(valor_entropia)
            guardar_valor(str(valor_m), "configuracionDePruebas/configT12.txt")
            modal.destroy()
            messagebox.showinfo("Configuración Guardada", "Valor de entropía guardado.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor numérico válido para la entropía.")

    # Botón para guardar la configuración
    Button(modal, text="Guardar", font=("Helvetica", 12), bg="#3B2C6A", fg="white", command=guardar_y_cerrar).pack(pady=10)
