from tkinter import Toplevel, Label, Entry, Button, messagebox
import os

def guardar_valor_m(valor_m):
    with open("configuracionDePruebas/configT2.txt", "w") as file:
        file.write(valor_m)

def cargar_valor_m():
    if os.path.exists("configT2.txt"):
        with open("configuracionDePruebas/configT2.txt", "r") as file:
            return file.read().strip()
    return ""

def abrir_modal_config(root):
    modal = Toplevel(root)
    modal.title("Configuración de Prueba 2")
    modal.geometry("300x200")
    modal.configure(bg="#2E2A47")
    
    entrada_m = Entry(modal, width=10, font=("Helvetica", 14), bd=2, relief="solid")
    entrada_m.pack(pady=10)
    entrada_m.insert(0, cargar_valor_m())
    
    def guardar_y_cerrar():
        valor_m = entrada_m.get()
        if valor_m.isdigit():
            guardar_valor_m(valor_m)
            modal.destroy()
            messagebox.showinfo("Configuración Guardada", f"Valor de M guardado: {valor_m}")
        else:
            messagebox.showerror("Error", "Valor no válido.")
    
    Button(modal, text="Guardar", font=("Helvetica", 12), bg="#3B2C6A", fg="white", command=guardar_y_cerrar).pack(pady=10)

def seleccionar_todo(check_vars, boton_seleccionar):
    all_selected = all(check_vars[i].get() for i in range(1, 16))
    if all_selected:
        for i in range(1, 16):
            check_vars[i].set(0)
        boton_seleccionar.config(text="Seleccionar todas las pruebas")
    else:
        for i in range(1, 16):
            check_vars[i].set(1)
        boton_seleccionar.config(text="Reiniciar")
