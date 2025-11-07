import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class Personal:
    def __init__(self, nombre, apellido, direccion, edad, telefono, correo, rol, contrasena):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.edad = edad
        self.telefono = telefono
        self.correo = correo
        self.rol = rol
        self.contrasena = contrasena



def conectar():
    conexion = sqlite3.connect('personal.db')
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personal (
        id_Personal INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        direccion TEXT NOT NULL,
        edad INTEGER NOT NULL,
        telefono TEXT NOT NULL,
        correo TEXT NOT NULL,
        rol TEXT NOT NULL,
        contrasena TEXT NOT NULL
    )
    """)
    conexion.commit()
    return conexion, cursor



def guardar_personal():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    direccion = entry_direccion.get()
    edad = entry_edad.get()
    telefono = entry_telefono.get()
    if len(telefono) != 8 or not telefono.isdigit():
        messagebox.showerror("Error", "El teléfono debe contener exactamente 8 dígitos numéricos.")
        return
    correo = entry_correo.get()
    rol = entry_rol.get()
    contrasena = entry_contrasena.get()

    if not (nombre and apellido and direccion and edad and telefono and correo and rol and contrasena):
        messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
        return

    try:
        edad = int(edad)
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número entero.")
        return

    conexion, cursor = conectar()
    cursor.execute("""
        INSERT INTO personal(nombre, apellido, direccion, edad, telefono, correo, rol, contrasena)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre, apellido, direccion, edad, telefono, correo, rol, contrasena))
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Éxito", "Registro guardado correctamente.")
    limpiar_campos()
    mostrar_datos()


def mostrar_datos():
    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion, cursor = conectar()
    cursor.execute("SELECT * FROM personal")
    registros = cursor.fetchall()
    conexion.close()

    for reg in registros:
        tabla.insert("", tk.END, values=reg)


def seleccionar_registro(event):
    try:
        item = tabla.selection()[0]
        valores = tabla.item(item, "values")

        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        entry_rol.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)

        entry_id.insert(0, valores[0])
        entry_nombre.insert(0, valores[1])
        entry_apellido.insert(0, valores[2])
        entry_direccion.insert(0, valores[3])
        entry_edad.insert(0, valores[4])
        entry_telefono.insert(0, valores[5])
        entry_correo.insert(0, valores[6])
        entry_rol.insert(0, valores[7])
        entry_contrasena.insert(0, valores[8])
    except IndexError:
        pass


def modificar_personal():

    ventana_buscar = tk.Toplevel(ventana)
    ventana_buscar.title("Modificar Personal")
    ventana_buscar.geometry("300x200")
    ventana_buscar.resizable(False, False)

    tk.Label(ventana_buscar, text="Ingrese ID del personal:").pack(pady=5)
    entry_id = tk.Entry(ventana_buscar)
    entry_id.pack(pady=5)

    tk.Label(ventana_buscar, text="Ingrese Nombre del personal:").pack(pady=5)
    entry_nombre = tk.Entry(ventana_buscar)
    entry_nombre.pack(pady=5)

    def buscar_registro():
        id_personal = entry_id.get()
        nombre_personal = entry_nombre.get().strip()

        if not id_personal or not nombre_personal:
            messagebox.showwarning("Campos vacíos", "Debe ingresar el ID y el nombre.")
            return

        conexion, cursor = conectar()
        cursor.execute("SELECT * FROM personal WHERE id_Personal=? AND nombre=?", (id_personal, nombre_personal))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("No encontrado", f"No existe un registro con ID {id_personal} y nombre '{nombre_personal}'.")
            conexion.close()
            return

        # Si existe el registro, abrir ventana de edición
        ventana_editar = tk.Toplevel(ventana)
        ventana_editar.title("Editar Personal")
        ventana_editar.geometry("400x400")
        ventana_editar.resizable(False, False)


        labels = ["Nombre", "Apellido", "Dirección", "Edad", "Teléfono", "Correo", "Rol", "Contraseña"]
        entries = []

        for i, campo in enumerate(labels):
            tk.Label(ventana_editar, text=campo + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            e = tk.Entry(ventana_editar, width=30)
            e.grid(row=i, column=1, padx=10, pady=5)
            e.insert(0, registro[i+1])  # los campos inician en índice 1
            entries.append(e)

        def guardar_cambios():
            nuevos_valores = [e.get() for e in entries]

            if not all(nuevos_valores):
                messagebox.showwarning("Campos vacíos", "Debe completar todos los campos antes de guardar.")
                return

            cursor.execute("""
                UPDATE personal SET nombre=?, apellido=?, direccion=?, edad=?, telefono=?, correo=?, rol=?, contrasena=?
                WHERE id_Personal=? AND nombre=?
            """, (*nuevos_valores, id_personal, nombre_personal))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", f"Datos de '{nombre_personal}' actualizados correctamente.")
            ventana_editar.destroy()
            ventana_buscar.destroy()
            mostrar_datos()
            limpiar_campos()

        tk.Button(ventana_editar, text="Guardar Cambios", bg="#93c47d", command=guardar_cambios).grid(row=8, column=0, columnspan=2, pady=15)

    tk.Button(ventana_buscar, text="Buscar", bg="#6fa8dc", command=buscar_registro).pack(pady=10)
    tk.Button(ventana_buscar, text="Cancelar", command=ventana_buscar.destroy).pack()

def eliminar_personal():
    # Ventana emergente para ingresar ID y nombre
    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.title("Eliminar registro")
    ventana_eliminar.geometry("300x200")
    ventana_eliminar.resizable(False, False)

    tk.Label(ventana_eliminar, text="Ingrese ID del personal:").pack(pady=5)
    entry_id_eliminar = tk.Entry(ventana_eliminar)
    entry_id_eliminar.pack(pady=5)

    tk.Label(ventana_eliminar, text="Ingrese Nombre del personal:").pack(pady=5)
    entry_nombre_eliminar = tk.Entry(ventana_eliminar)
    entry_nombre_eliminar.pack(pady=5)

    def confirmar_eliminacion():
        id_personal = entry_id_eliminar.get()
        nombre_personal = entry_nombre_eliminar.get().strip()

        if not id_personal or not nombre_personal:
            messagebox.showwarning("Campos vacíos", "Debe ingresar el ID y el nombre.")
            return

        conexion, cursor = conectar()
        cursor.execute("SELECT * FROM personal WHERE id_Personal=? AND nombre=?", (id_personal, nombre_personal))
        registro = cursor.fetchone()

        if registro:
            # Confirmar con el usuario
            confirmacion = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar a '{nombre_personal}' (ID: {id_personal})?")
            if confirmacion:
                cursor.execute("DELETE FROM personal WHERE id_Personal=? AND nombre=?", (id_personal, nombre_personal))
                conexion.commit()
                messagebox.showinfo("Éxito", f"Registro de '{nombre_personal}' eliminado correctamente.")
                ventana_eliminar.destroy()
                mostrar_datos()
                limpiar_campos()
        else:
            messagebox.showerror("No encontrado", f"No existe un registro con ID {id_personal} y nombre '{nombre_personal}'.")

        conexion.close()


    tk.Button(ventana_eliminar, text="Eliminar", bg="#e06666", command=confirmar_eliminacion).pack(pady=10)
    tk.Button(ventana_eliminar, text="Cancelar", command=ventana_eliminar.destroy).pack()

def validar_telefono(texto):
    # Permitir solo números y máximo 8 dígitos
    if texto.isdigit() and len(texto) <= 8:
        return True
    elif texto == "":  # Permitir borrar todo
        return True
    else:
        return False
def limpiar_campos():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_rol.delete(0, tk.END)
    entry_contrasena.delete(0, tk.END)


ventana = tk.Tk()
ventana.title("Gestión de Personal")
ventana.geometry("800x600")

# CAMPOS DE ENTRADA
tk.Label(ventana, text="ID (no editable):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_id = tk.Entry(ventana)
entry_id.grid(row=0, column=1, padx=5, pady=5)
entry_id.config(state="readonly")

tk.Label(ventana, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=1, column=1, padx=5, pady=5)

tk.Label(ventana, text="Apellido:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_apellido = tk.Entry(ventana)
entry_apellido.grid(row=2, column=1, padx=5, pady=5)

tk.Label(ventana, text="Dirección:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_direccion = tk.Entry(ventana)
entry_direccion.grid(row=3, column=1, padx=5, pady=5)

tk.Label(ventana, text="Edad:").grid(row=4, column=0, padx=5, pady=5, sticky="w")


edades = [str(i) for i in range(18, 61)]
entry_edad = ttk.Combobox(ventana, values=edades, state="readonly", width=17)
entry_edad.grid(row=4, column=1, padx=5, pady=5)
entry_edad.set("18")

tk.Label(ventana, text="Teléfono:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
validacion_tel = ventana.register(validar_telefono)
entry_telefono = tk.Entry(ventana, validate="key", validatecommand=(validacion_tel, "%P"))
entry_telefono.grid(row=5, column=1, padx=5, pady=5)

tk.Label(ventana, text="Correo:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
entry_correo = tk.Entry(ventana)
entry_correo.grid(row=6, column=1, padx=5, pady=5)

tk.Label(ventana, text="Rol:").grid(row=7, column=0, padx=5, pady=5, sticky="w")

roles = ["Coordinador", "Supervisor", "Técnico"]
entry_rol = ttk.Combobox(ventana, values=roles, state="readonly", width=17)
entry_rol.grid(row=7, column=1, padx=5, pady=5)
entry_rol.set("Técnico")

tk.Label(ventana, text="Contraseña:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
entry_contrasena = tk.Entry(ventana, show="*")
entry_contrasena.grid(row=8, column=1, padx=5, pady=5)


tk.Button(ventana, text="Guardar", command=guardar_personal, width=12, bg="#E0FFFF").grid(row=9, column=0, pady=10)
tk.Button(ventana, text="Modificar", command=modificar_personal, width=12, bg="#E0FFFF").grid(row=9, column=1)
tk.Button(ventana, text="Eliminar", command=eliminar_personal, width=12, bg="#E0FFFF").grid(row=10, column=0)
tk.Button(ventana, text="Limpiar", command=limpiar_campos, width=12, bg="#E0FFFF").grid(row=10, column=1)


tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Apellido", "Dirección", "Edad", "Teléfono", "Correo", "Rol", "Contraseña"), show="headings", height=10)
tabla.grid(row=11, column=0, columnspan=4, padx=10, pady=10)


encabezados = ["ID", "Nombre", "Apellido", "Dirección", "Edad", "Teléfono", "Correo", "Rol", "Contraseña"]
for i, texto in enumerate(encabezados):
   tabla.heading(texto, text=texto)
   tabla.column(texto, width=100)

tabla.bind("<<TreeviewSelect>>", seleccionar_registro)


mostrar_datos()

ventana.mainloop()