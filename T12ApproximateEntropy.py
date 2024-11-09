# T12ApproximateEntropy.py

import math
from math import gamma, e
import numpy as np
from tkinter import StringVar
from tkinter import Tk, Label, Button, Entry, StringVar, Checkbutton, IntVar, Frame, Toplevel
from math import log, gamma, e

# Funciones auxiliares de cálculo de gamma
def upper_incomplete_gamma(a, x, d=0, iterations=100):
    if d == iterations:
        if ((d % 2) == 1):
            return 1.0  # fin de las iteraciones
        else:
            m = d / 2
            return x + (m - a)
    if d == 0:
        try:
            result = ((x ** a) * (e ** (-x))) / upper_incomplete_gamma(a, x, d=d + 1)
        except OverflowError:
            result = 0.0
        return result
    elif ((d % 2) == 1):
        m = 1.0 + ((d - 1.0) / 2.0)
        return x + ((m - a) / (upper_incomplete_gamma(a, x, d=d + 1)))
    else:
        m = d / 2
        return 1 + (m / (upper_incomplete_gamma(a, x, d=d + 1)))

def gammaincc(a, x):
    return upper_incomplete_gamma(a, x) / gamma(a)

def bits_to_int(bits):
    theint = 0
    for i in range(len(bits)):
        theint = (theint << 1) + bits[i]
    return theint

def approximate_entropy_test(bits):
    n = len(bits)
    
    m = int(log(n, 2)) - 6
    if m < 2:
        m = 2
    if m > 3:
        m = 3
        
    Cmi = list()
    phi_m = list()
    for iterm in range(m, m + 2):
        padded_bits = bits + bits[0:iterm - 1]
        counts = list()
        for i in range(2 ** iterm):
            count = 0
            for j in range(n):
                if bits_to_int(padded_bits[j:j + iterm]) == i:
                    count += 1
            counts.append(count)

        Ci = list()
        for i in range(2 ** iterm):
            Ci.append(float(counts[i]) / float(n))
        
        Cmi.append(Ci)
    
        sum = 0.0
        for i in range(2 ** iterm):
            if (Ci[i] > 0.0):
                sum += Ci[i] * log((Ci[i] / 10.0))
        phi_m.append(sum)
        
    appen_m = phi_m[0] - phi_m[1]
    chisq = 2 * n * (log(2) - appen_m)
    
    p = gammaincc(2 ** (m - 1), (chisq / 2.0))
    
    success = (p >= 0.01)
    return appen_m, p, success


def mostrar_resultado(binario, tests_seleccionados, resultado_entropia, resultado_pvalor, resultado_final):
    try:
        # Convertir la cadena de entrada en una lista de bits
        bits = [int(b) for b in binario.strip()]
        entropia, p_valor, es_aleatorio = approximate_entropy_test(bits)
        
        # Actualizar los resultados en la interfaz
        resultado = "Aleatorio (P-valor >= 0.01)" if es_aleatorio else "No aleatorio (P-valor < 0.01)"
        
        # Mostrar entropía con 8 decimales y p-valor con 15 decimales
        resultado_entropia.set(f"Entropía Aproximada: {entropia:.8f}")
        resultado_pvalor.set(f"P-valor: {p_valor:.15f}")
        
        # Agregar el criterio de decisión basado en el p-valor
        if p_valor < 0.01:
            criterio_decision = "La secuencia es no aleatoria (P-valor < 0.01)."
        else:
            criterio_decision = "La secuencia es aleatoria (P-valor >= 0.01)."
        
        # Mostrar la conclusión en base a la interpretación
        conclusion = (
            f"Conclusión: {criterio_decision}\n"
            f"Interpretación: Los valores pequeños de ApEn(m) indican regularidad fuerte. "
            f"Valores grandes de ApEn(m) indican fluctuación o irregularidad."
        )
        
        resultado_final.set(conclusion)
    except ValueError:
        resultado_entropia.set("Error: Entrada no válida")
        resultado_pvalor.set("")
        resultado_final.set("")
