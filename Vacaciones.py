import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# --- Clase Vacaciones ---
class Vacaciones:
    def __init__(self, id_personal, nombre, dias_go):
        self.id_personal = id_personal
        self.nombre = nombre
        self.dias_go = dias_go



def Conectar():
    conexion = sqlite3.connect('Vacaciones.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vacaciones (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_personal INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            dias_go INTEGER NOT NULL
        )
    ''')
    conexion.commit()
    return conexion, cursor



def cargar_personal():
    try:
        conn = sqlite3.connect('Personal.db')
        cur = conn.cursor()
        cur.execute("SELECT id_Personal, nombre || ' ' || apellido, vacaciones FROM personal")
        datos = cur.fetchall()
        conn.close()
        return datos
    except Exception as e:
        messagebox.showerror("Error BD", f"No se pudo conectar a Personal.db:\n{e}")
        return []


def guardar():
    try:
        id_personal = combo_personal_id.get()
        nombre = combo_personal_nombre.get()
        dias_go = entry_dias_go.get()

        if not id_personal or not nombre or not dias_go:
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        dias_go = int(dias_go)


        conn_p = sqlite3.connect('Personal.db')
        cur_p = conn_p.cursor()
        cur_p.execute("SELECT vacaciones FROM personal WHERE id_Personal=?", (id_personal,))
        resultado = cur_p.fetchone()

        if not resultado:
            messagebox.showerror("Error", "No se encontró el empleado en Personal.db")
            conn_p.close()
            return

        dias_actuales = resultado[0]

        if dias_go > dias_actuales:
            messagebox.showwarning("Advertencia", f"El empleado solo tiene {dias_actuales} días disponibles.")
            conn_p.close()
            return

        nuevos_dias = dias_actuales - dias_go


        conexion, cursor = Conectar()
        cursor.execute('''
            INSERT INTO Vacaciones (id_personal, nombre, dias_go)
            VALUES (?, ?, ?)
        ''', (id_personal, nombre, dias_go))
        conexion.commit()
        conexion.close()

        # 🔹 Actualizar días en Personal.db
        cur_p.execute("UPDATE personal SET vacaciones=? WHERE id_Personal=?", (nuevos_dias, id_personal))
        conn_p.commit()
        conn_p.close()

        messagebox.showinfo("Éxito", f"Registro guardado.\nDías restantes: {nuevos_dias}")
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



def limpiar_campos():
    combo_personal_id.set("")
    combo_personal_nombre.set("")
    entry_dias_go.delete(0, tk.END)



def actualizar_nombre(event):
    id_sel = combo_personal_id.get()
    for p in datos_personal:
        if str(p[0]) == str(id_sel):
            combo_personal_nombre.set(p[1])
            break

def salir():
    if messagebox.askyesno("Salir", "¿Desea salir de la aplicación?"):
        root.destroy()

root = tk.Tk()
root.title("Gestión de Vacaciones")
root.geometry("850x550")
root.configure(bg="#E0FFFF")

tk.Label(root, text="ID Personal:", bg="#E0FFFF").grid(row=0, column=0, padx=10, pady=5, sticky="w")
combo_personal_id = ttk.Combobox(root, width=17, state="readonly")
combo_personal_id.grid(row=0, column=1, padx=10, pady=5)
combo_personal_id.bind("<<ComboboxSelected>>", actualizar_nombre)

tk.Label(root, text="Nombre:", bg="#E0FFFF").grid(row=1, column=0, padx=10, pady=5, sticky="w")
combo_personal_nombre = ttk.Combobox(root, width=17, state="readonly")
combo_personal_nombre.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Días a Gozar:", bg="#E0FFFF").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_dias_go = tk.Entry(root)
entry_dias_go.grid(row=2, column=1, padx=10, pady=5)


# --- Botones ---
tk.Button(root, text="Guardar", command=guardar, bg="#4CAF50", fg="white", width=12).grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Salir", command=salir, bg="red", fg="white", width=12).grid(row=3, column=1, padx=10, pady=10)  # 🔸 Botón Salir
tk.Button(root, text="Limpiar", command=limpiar_campos, width=12).grid(row=3, column=2, padx=10, pady=10)



columnas = ("Id", "ID Personal", "Nombre", "Días a Gozar")
tabla = ttk.Treeview(root, columns=columnas, show="headings", height=10)
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=150)

tabla.grid(row=4, column=0, columnspan=4, padx=10, pady=10)


datos_personal = cargar_personal()
if datos_personal:
    combo_personal_id['values'] = [d[0] for d in datos_personal]
    combo_personal_nombre['values'] = [d[1] for d in datos_personal]

mostrar_datos()
root.mainloop()