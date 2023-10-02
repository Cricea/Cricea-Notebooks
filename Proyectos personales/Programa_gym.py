import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('registros.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS entrenamientos
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
           ejercicio TEXT,
           peso REAL,
           repeticiones INTEGER,
           peso_cargado REAL,
           fecha DATE)
          ''')
conn.commit()

def reportar_avance():
    ejercicio = ejercicio_var.get()
    peso = float(peso_entry.get())
    repeticiones = int(repeticiones_entry.get())
    peso_cargado = peso * repeticiones
    fecha = cal.get_date()  # Obtener la fecha del calendario

    c.execute("INSERT INTO entrenamientos (ejercicio, peso, repeticiones, peso_cargado, fecha) VALUES (?, ?, ?, ?, ?)",
              (ejercicio, peso, repeticiones, peso_cargado, fecha))
    conn.commit()

    peso_entry.delete(0, tk.END)
    repeticiones_entry.delete(0, tk.END)

def mostrar_registros():
    resultados.delete(1.0, tk.END)

    c.execute("SELECT * FROM entrenamientos")
    registros = c.fetchall()

    for registro in registros:
        resultados.insert(tk.END, f"Ejercicio: {registro[1]}\n")
        resultados.insert(tk.END, f"Peso (kg): {registro[2]}\n")
        resultados.insert(tk.END, f"Repeticiones: {registro[3]}\n")
        resultados.insert(tk.END, f"Peso Cargado (kg): {registro[4]}\n")
        resultados.insert(tk.END, f"Fecha: {registro[5]}\n")
        resultados.insert(tk.END, "-" * 20 + "\n")

root = tk.Tk()
root.title("Registro de Avances")

ejercicios = ["Press de Banca", "Dominadas", "Sentadillas", "Press de Hombros", "Curl de Bíceps"]

ttk.Label(root, text="Ejercicio:").pack()
ejercicio_var = tk.StringVar()
ejercicio_menu = ttk.Combobox(root, textvariable=ejercicio_var, values=ejercicios, state="readonly")
ejercicio_menu.pack()

ttk.Label(root, text="Peso (kg):").pack()
peso_entry = ttk.Entry(root)
peso_entry.pack()

ttk.Label(root, text="Repeticiones:").pack()
repeticiones_entry = ttk.Entry(root)
repeticiones_entry.pack()

ttk.Label(root, text="Fecha:").pack()
cal = Calendar(root, date_pattern='yyyy-mm-dd')
cal.pack()

reportar_button = ttk.Button(root, text="Reportar Avance", command=reportar_avance)
reportar_button.pack()

mostrar_button = ttk.Button(root, text="Mostrar Registros", command=mostrar_registros)
mostrar_button.pack()

resultados = tk.Text(root, width=40, height=10)
resultados.pack()

root.mainloop()
