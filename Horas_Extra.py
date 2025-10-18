
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk



class Horas_extras:
    def __init__(self, reporte, idnodo, hora_inicio, hora_fin, solucion, tecnico):
        self.reporte = reporte
        self.idnodo = idnodo
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solucion = solucion
        self.tecnico = tecnico


def conectar():
    conexion = sqlite3.connect("mi_base_datos.db")
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS horas_extras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporte INTEGER NOT NULL,
        idnodo TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT NOT NULL,
        solucion TEXT,
        tecnico TEXT
    )
    """)
    conexion.commit()
    return conexion, cursor



def guardar_datos():
    try:
        reporte = int(entry_reporte.get())
        idnodo = entry_idnodo.get()
        hora_inicio = entry_inicio.get()
        hora_fin = entry_fin.get()
        solucion = entry_solucion.get("1.0", tk.END).strip()
        tecnico = entry_tecnico.get()

        if not (idnodo and hora_inicio and hora_fin and tecnico):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos obligatorios.")
            return

        registro = Horas_extras(reporte, idnodo, hora_inicio, hora_fin, solucion, tecnico)
        conexion, cursor = conectar()
        cursor.execute("""
            INSERT INTO horas_extras (reporte, idnodo, hora_inicio, hora_fin, solucion, tecnico)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (registro.reporte, registro.idnodo, registro.hora_inicio, registro.hora_fin, registro.solucion, registro.tecnico))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Registro guardado correctamente.")
        limpiar_campos()
        mostrar_datos()

    except ValueError:
        messagebox.showerror("Error", "El número de orden debe ser un número entero.")


def mostrar_datos():
    conexion, cursor = conectar()
    cursor.execute("SELECT * FROM horas_extras")
    registros = cursor.fetchall()
    conexion.close()

    for fila in tabla.get_children():
        tabla.delete(fila)

    for fila in registros:
        tabla.insert("", tk.END, values=fila)


def eliminar_dato():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccione un registro para eliminar.")
        return

    id_registro = tabla.item(seleccionado[0])["values"][0]
    conexion, cursor = conectar()
    cursor.execute("DELETE FROM horas_extras WHERE id = ?", (id_registro,))
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
    mostrar_datos()


def modificar_dato():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccione un registro para modificar.")
        return

    id_registro = tabla.item(seleccionado[0])["values"][0]
    nuevo_fin = entry_fin.get()
    nueva_solucion = entry_solucion.get("1.0", tk.END).strip()

    conexion, cursor = conectar()
    cursor.execute("""
        UPDATE horas_extras
        SET hora_fin = ?, solucion = ?
        WHERE id = ?
    """, (nuevo_fin, nueva_solucion, id_registro))
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Éxito", "Registro modificado correctamente.")
    mostrar_datos()


def limpiar_campos():
    entry_reporte.delete(0, tk.END)
    entry_idnodo.delete(0, tk.END)
    entry_inicio.delete(0, tk.END)
    entry_fin.delete(0, tk.END)
    entry_solucion.delete("1.0", tk.END)
    entry_tecnico.delete(0, tk.END)
def salir():
    pass
ventana = tk.Tk()
ventana.title("GESTIÓN DE HORAS EXTRA")
ventana.geometry("950x600")
ventana.configure(bg="#E0FFFF")

titulo = tk.Label(ventana, text="REGISTRO DE HORAS EXTRA", font=("Arial", 18, "bold"), bg="#E0FFFF", fg="#003366")
titulo.pack(pady=10)

frame_form = tk.Frame(ventana, bg="#E0FFFF")
frame_form.pack(pady=10)

tk.Label(frame_form, text="N° Orden:", bg="#E0FFFF").grid(row=0, column=0, padx=5, pady=5)
entry_reporte = tk.Entry(frame_form)
entry_reporte.grid(row=0, column=1)

tk.Label(frame_form, text="ID Nodo:", bg="#E0FFFF").grid(row=1, column=0, padx=5, pady=5)
entry_idnodo = tk.Entry(frame_form)
entry_idnodo.grid(row=1, column=1)

tk.Label(frame_form, text="Hora Inicio:", bg="#E0FFFF").grid(row=0, column=2, padx=5, pady=5)
entry_inicio = tk.Entry(frame_form)
entry_inicio.grid(row=0, column=3)

tk.Label(frame_form, text="Hora Fin:", bg="#E0FFFF").grid(row=1, column=2, padx=5, pady=5)
entry_fin = tk.Entry(frame_form)
entry_fin.grid(row=1, column=3)

tk.Label(frame_form, text="Técnico:", bg="#E0FFFF").grid(row=0, column=4, padx=5, pady=5)
entry_tecnico = tk.Entry(frame_form)
entry_tecnico.grid(row=0, column=5)

tk.Label(frame_form, text="Solución:", bg="#E0FFFF").grid(row=2, column=0, padx=5, pady=5)
entry_solucion = tk.Text(frame_form, width=70, height=3)
entry_solucion.grid(row=2, column=1, columnspan=5, pady=5)

frame_botones = tk.Frame(ventana, bg="#E0FFFF")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Guardar", command=guardar_datos, bg="#D3D3D3", width=12).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Mostrar", command=mostrar_datos, bg="#D3D3D3", width=12).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Modificar", command=modificar_dato, bg="#D3D3D3", width=12).grid(row=0, column=2, padx=10)
tk.Button(frame_botones, text="Eliminar", command=eliminar_dato, bg="#D3D3D3", width=12).grid(row=0, column=3, padx=10)
tk.Button(frame_botones, text="Limpiar", command=limpiar_campos, bg="#D3D3D3", width=12).grid(row=0, column=4, padx=10)
tk.Button(frame_botones, text="salir",bg="#D3D3D3",width=12).grid(row=0, column=5, padx=10)

tabla = ttk.Treeview(ventana, columns=("id", "reporte", "idnodo", "inicio", "fin", "solucion", "tecnico"), show="headings")
tabla.heading("id", text="ID")
tabla.heading("reporte", text="Orden")
tabla.heading("idnodo", text="ID Nodo")
tabla.heading("inicio", text="Inicio")
tabla.heading("fin", text="Fin")
tabla.heading("solucion", text="Solución")
tabla.heading("tecnico", text="Técnico")
tabla.pack(fill="both", expand=True, pady=10)

mostrar_datos()
ventana.mainloop()