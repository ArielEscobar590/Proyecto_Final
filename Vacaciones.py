import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class Vacaciones:
    def __init__(self, inicio, final, mes, supervisor):
        self.inicio = inicio
        self.final = final
        self.mes = mes
        self.supervisor = supervisor



def Conectar():
    conexion = sqlite3.connect('Vacaciones.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vacaciones (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_inicio TEXT,
            fecha_final TEXT,
            mes TEXT,
            supervisor TEXT
        )
    ''')
    conexion.commit()
    return conexion, cursor


# --- Funciones principales ---
def guardar():
    inicio = entry_fecha_inicio.get()
    final = entry_fecha_final.get()
    mes = entry_mes.get()
    supervisor = entry_supervisor.get()

    if not inicio or not final or not mes or not supervisor:
        messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
        return

    try:
        registro = Vacaciones(inicio, final, mes, supervisor)
        conexion, cursor = Conectar()
        cursor.execute('''
            INSERT INTO Vacaciones (fecha_inicio, fecha_final, mes, supervisor)
            VALUES (?, ?, ?, ?)
        ''', (registro.inicio, registro.final, registro.mes, registro.supervisor))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Registro guardado correctamente.")
        limpiar_campos()
        mostrar_datos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el registro: {e}")


def mostrar_datos():
    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion, cursor = Conectar()
    cursor.execute("SELECT * FROM Vacaciones")
    registros = cursor.fetchall()
    for row in registros:
        tabla.insert("", "end", values=row)
    conexion.close()


def eliminar_dato():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Seleccione un registro para eliminar.")
        return

    item = tabla.item(seleccion)
    id_registro = item['values'][0]

    conexion, cursor = Conectar()
    cursor.execute("DELETE FROM Vacaciones WHERE Id=?", (id_registro,))
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
    mostrar_datos()


def limpiar_campos():
    entry_fecha_inicio.delete(0, tk.END)
    entry_fecha_final.delete(0, tk.END)
    entry_mes.delete(0, tk.END)
    entry_supervisor.delete(0, tk.END)


# --- Interfaz Tkinter ---
root = tk.Tk()
root.title("Gestión de Vacaciones")
root.geometry("800x500")

tk.Label(root, text="Fecha inicio:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_fecha_inicio = tk.Entry(root)
entry_fecha_inicio.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Fecha final:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_fecha_final = tk.Entry(root)
entry_fecha_final.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Mes:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_mes = tk.Entry(root)
entry_mes.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Supervisor:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_supervisor = tk.Entry(root)
entry_supervisor.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Guardar", command=guardar, bg="#4CAF50", fg="white").grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Eliminar", command=eliminar_dato, bg="#F44336", fg="white").grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Limpiar", command=limpiar_campos).grid(row=4, column=2, padx=10, pady=10)

# --- Tabla de registros ---
columnas = ("Id", "Fecha Inicio", "Fecha Final", "Mes", "Supervisor")
tabla = ttk.Treeview(root, columns=columnas, show="headings", height=10)
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=130)

tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
mostrar_datos()

root.mainloop()