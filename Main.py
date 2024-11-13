from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Frame, Text, messagebox, PhotoImage, Checkbutton
from funciones import *
from T2FrecuencyWithinABlock import block_frequency

root = Tk()
root.title("Pruebas NIST - Pruebas de Aleatoriedad")
root.geometry("1200x900")
root.configure(bg="#2E2A47")
root.state('zoomed')
root.resizable(False, False)

config_image = PhotoImage(file="img/config.png").subsample(25, 25)

main_frame = Frame(root, bg="#2E2A47")
main_frame.pack(fill="both", expand=True)

resultados = {i: StringVar() for i in range(1, 16)}
aleatorio_texto = {i: StringVar() for i in range(1, 16)}
check_vars = {i: IntVar() for i in range(1, 16)}

frame_pruebas = Frame(main_frame, bg="#2E2A47", bd=1, relief="solid")
frame_pruebas.pack(side="left", padx=30, pady=20, fill="both", expand=True)

label_style = {"font": ("Helvetica", 12, "bold"), "fg": "#FFFFFF", "bg": "#3B2C6A", "bd": 1, "relief": "solid"}
result_style = {"font": ("Helvetica", 12), "fg": "#F4C8FF", "bg": "#2E2A47", "bd": 1, "relief": "solid"}

frame_canvas_pruebas = Frame(frame_pruebas, bg="#2E2A47")
frame_canvas_pruebas.pack(fill="both", expand=True)

Label(frame_canvas_pruebas, text="Prueba", **label_style, width=45).grid(row=0, column=0, padx=5, pady=(0, 10), sticky="w")
Label(frame_canvas_pruebas, text="Resultado", **label_style, width=40).grid(row=0, column=1, padx=5, pady=(0, 10), sticky="w")
Label(frame_canvas_pruebas, text="Aleatoriedad", **label_style, width=20).grid(row=0, column=2, padx=5, pady=(0, 10), sticky="w")

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

row = 1
for label_text, test_id in pruebas:
    if test_id == 2:
        button_command = lambda test_id=test_id: abrir_modal_config_prueba_2(root)
    elif test_id == 3:
        button_command = lambda test_id=test_id: abrir_modal_config_prueba_3(root)
    elif test_id == 8:
        button_command = lambda test_id=test_id: abrir_modal_config_prueba_8(root, entrada_binario)
    elif test_id == 9:  # Aquí se agrega la comprobación para la prueba 9
        button_command = lambda test_id=test_id: abrir_modal_config_prueba_9(root)
    else:
        button_command = None

    Button(frame_canvas_pruebas, image=config_image, bg="#2E2A47", bd=0, command=button_command).grid(row=row, column=0, sticky="w", padx=(0, 5), pady=5)
    
    Checkbutton(frame_canvas_pruebas, text=label_text, variable=check_vars[test_id], font=("Helvetica", 12), bg="#2E2A47", fg="#F4C8FF", selectcolor="#3B2C6A", bd=1, relief="solid").grid(row=row, column=0, sticky="w", padx=(30, 5), pady=5)

    if test_id in [14, 15]:
        text_widget = Text(frame_canvas_pruebas, height=5, width=40, font=("Helvetica", 12), fg="#F4C8FF", bg="#2E2A47", bd=1, relief="solid")
        text_widget.grid(row=row, column=1, pady=5)
        resultados[test_id] = text_widget
    else:
        Label(frame_canvas_pruebas, textvariable=resultados[test_id], **result_style, width=40, anchor="w").grid(row=row, column=1, pady=5)

    Label(frame_canvas_pruebas, textvariable=aleatorio_texto[test_id], **result_style, width=20, anchor="w").grid(row=row, column=2, pady=5)

    row += 1


frame_controls = Frame(main_frame, bg="#2E2A47", bd=1, relief="solid", width=300)
frame_controls.pack(side="right", padx=10, pady=20, fill="y")

frame_controls.columnconfigure(0, weight=1)
frame_controls.columnconfigure(1, weight=1)

Label(frame_controls, text="Introduce una secuencia binaria:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_binario = Text(frame_controls, height=6, width=30, font=("Helvetica", 14), bd=2, relief="solid")
entrada_binario.pack(pady=10)
Label(frame_controls, text="Cantidad de bits aleatorios:", font=("Helvetica", 14), fg="#F4C8FF", bg="#2E2A47").pack(pady=10)
entrada_cantidad_bits = Entry(frame_controls, width=10, font=("Helvetica", 14), bd=2, relief="solid")
entrada_cantidad_bits.pack(pady=10)
Button(frame_controls, text="Ejecutar Pruebas Seleccionadas", font=("Helvetica", 14), bg="#3B2C6A", fg="white", width=25, command=lambda: ejecutar_pruebas_seleccionadas(check_vars, entrada_binario, resultados, aleatorio_texto)).pack(pady=10)
Button(frame_controls, text="Generar Secuencia Aleatoria", font=("Helvetica", 14), bg="#3B2C6A", fg="white", width=25, command=lambda: generar_secuencia_aleatoria(entrada_cantidad_bits, entrada_binario)).pack(pady=10)
entrada_binario.bind("<Control-v>", lambda event: on_paste(entrada_binario, event))
root.mainloop()
