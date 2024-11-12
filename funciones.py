from tkinter import Toplevel, Label, Entry, Button, messagebox, Frame
import os
from T2FrecuencyWithinABlock import block_frequency
import random

def guardar_valor_m(valor_m, archivo):
    with open(archivo, "w") as file:
        file.write(valor_m)

def cargar_valor_m(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r") as file:
            return file.read().strip()
    return ""

def abrir_modal_config(root, archivo, label_text, valor_inicial):
    modal = Toplevel(root)
    modal.title(f"Configuración de {label_text}")
    modal.geometry("300x200")
    modal.configure(bg="#2E2A47")

    frame_entrada = Frame(modal, bg="#2E2A47")
    frame_entrada.pack(pady=10)

    Label(frame_entrada, text=label_text + ":", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(side="left")
    entrada_m = Entry(frame_entrada, width=10, font=("Helvetica", 14), bd=2, relief="solid")
    entrada_m.pack(side="left", padx=5)
    entrada_m.insert(0, cargar_valor_m(archivo))  # Cargar valor desde el archivo correspondiente
    
    def guardar_y_cerrar():
        valor_m = entrada_m.get()
        if valor_m.isdigit():
            guardar_valor_m(valor_m, archivo)  # Guardar valor en el archivo correspondiente
            modal.destroy()
            messagebox.showinfo("Configuración Guardada", f"Valor de {label_text} guardado: {valor_m}")
        else:
            messagebox.showerror("Error", "Valor no válido.")
    
    Button(modal, text="Guardar", font=("Helvetica", 12), bg="#3B2C6A", fg="white", command=guardar_y_cerrar).pack(pady=10)

def abrir_modal_config_prueba_2(root):
    abrir_modal_config(root, "configuracionDePruebas/configT2.txt", "M", "")

def abrir_modal_config_prueba_8(root):
    abrir_modal_config(root, "configuracionDePruebas/configT8.txt", "B (Patron)", "")


def seleccionar_todo(check_vars, boton_seleccionar):
    all_selected = all(check_vars[i].get() for i in range(1, 16))
    for i in range(1, 16):
        check_vars[i].set(0) if all_selected else check_vars[i].set(1)
    boton_seleccionar.config(text="Reiniciar" if not all_selected else "Seleccionar todas las pruebas")
        
def ejecutar_pruebas_seleccionadas(check_vars, entrada_binario, resultados, aleatorio_texto):
    for test_id, var in check_vars.items():
        if var.get() == 1 and test_id == 2:  
            ejecutar_prueba_2(entrada_binario, resultados, aleatorio_texto)
            
def ejecutar_prueba_2(entrada_binario, resultados, aleatorio_texto):
    secuencia_binaria = entrada_binario.get()
    valor_m = cargar_valor_m("configuracionDePruebas/configT2.txt")
    if secuencia_binaria and valor_m:
        try:
            valor_m = int(valor_m)
        except ValueError:
            messagebox.showerror("Error", "El valor de M no es un número válido.")
            return

        p_val, is_random = block_frequency(secuencia_binaria, valor_m)
        resultados[2].set(f"P-valor: {p_val:.17f}")
        aleatorio_texto[2].set("Aleatorio" if is_random else "No Aleatorio")

def generar_secuencia_aleatoria(entrada_cantidad_bits, entrada_binario):
    cantidad_bits = entrada_cantidad_bits.get()
    if cantidad_bits.isdigit():
        cantidad_bits = int(cantidad_bits)
        secuencia_aleatoria = ''.join(str(random.randint(0, 1)) for _ in range(cantidad_bits))
        entrada_binario.delete(0, 'end')
        entrada_binario.insert(0, secuencia_aleatoria)
    else:
        messagebox.showerror("Error", "Por favor, introduce un número válido de bits.")

def obtener_expansion_binaria_e(bits):
    mp.dps = bits + 2
    e = mp.e
    binario_e = bin(int(e * (2 ** bits)))[2:].zfill(bits)
    return binario_e