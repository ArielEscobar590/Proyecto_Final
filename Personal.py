import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from tkinter import simpledialog

class Personal:
    def __init__(self, nombre, apellido, direccion, edad, telefono, correo, fecha_ingreso,vacaciones ,rol, contrasena):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.edad = edad
        self.telefono = telefono
        self.correo = correo
        self.fecha_ingreso = fecha_ingreso
        self.vacaciones=vacaciones
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
        fecha_ingreso TEXT NOT NULL,
        vacaciones INTEGER,
        rol TEXT NOT NULL,
        contrasena TEXT NOT NULL
    )
    """)
    conexion.commit()
    return conexion, cursor


def calcular_vacaciones(fecha_ingreso):
    try:
        ingreso = datetime.strptime(fecha_ingreso, "%Y-%m-%d")
        hoy = datetime.now()
        diferencia = hoy - ingreso
        meses = diferencia.days / 30

        if meses >= 12:
            return 15
        elif meses >= 6:
            return 8
        elif meses >= 3:
            return 5
        else:
            return 0
    except Exception:
        return 0

def guardar_cambios():

    id_personal = entry_id.get().strip()
    if not id_personal:
        messagebox.showwarning("Atención", "Debe cargar un registro antes de guardar los cambios.")
        return

    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    direccion = entry_direccion.get().strip()
    edad = entry_edad.get().strip()
    telefono = entry_telefono.get().strip()
    correo = entry_correo.get().strip()
    fecha_ingreso = entry_fecha_ingreso.get().strip()
    rol = entry_rol.get().strip()
    contrasena = entry_contrasena.get().strip()

    if not (nombre and apellido and direccion and edad and telefono and correo and fecha_ingreso and rol and contrasena):
        messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos antes de guardar cambios.")
        return

    try:
        edad = int(edad)
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número entero.")
        return

    vacaciones = calcular_vacaciones(fecha_ingreso)

    conexion, cursor = conectar()
    cursor.execute("""
        UPDATE personal
        SET nombre=?, apellido=?, direccion=?, edad=?, telefono=?, correo=?, fecha_ingreso=?, vacaciones=?, rol=?, contrasena=?
        WHERE id_Personal=?
    """, (nombre, apellido, direccion, edad, telefono, correo, fecha_ingreso, vacaciones, rol, contrasena, id_personal))
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Éxito", f"Los datos del personal con ID {id_personal} fueron actualizados correctamente.")
    mostrar_datos()
    limpiar_campos()


def guardar_personal():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    direccion = entry_direccion.get().strip()
    edad = entry_edad.get().strip()
    telefono = entry_telefono.get().strip()
    correo = entry_correo.get().strip()
    fecha_ingreso = entry_fecha_ingreso.get().strip()
    rol = entry_rol.get().strip()
    contrasena = entry_contrasena.get().strip()


    if not (nombre and apellido and direccion and edad and telefono and correo and fecha_ingreso and rol and contrasena):
        messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
        return

    if not telefono.isdigit() or len(telefono) != 8:
        messagebox.showerror("Error", "El teléfono debe tener 8 dígitos numéricos.")
        return

    try:
        edad = int(edad)
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número entero.")
        return

    try:
        vacaciones = calcular_vacaciones(fecha_ingreso)
        conexion, cursor = conectar()
        cursor.execute("""
            INSERT INTO personal (nombre, apellido, direccion, edad, telefono, correo, fecha_ingreso, vacaciones, rol, contrasena)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, direccion, edad, telefono, correo, fecha_ingreso, vacaciones, rol, contrasena))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", f"Registro guardado correctamente.\nVacaciones asignadas: {vacaciones} días.")
        limpiar_campos()
        mostrar_datos()

    except Exception as e:
        messagebox.showerror("Error inesperado", f"No se pudo guardar el registro.\n\nDetalle: {e}")

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
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, valores[0])
        entry_id.config(state="readonly")

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])
        entry_apellido.delete(0, tk.END)
        entry_apellido.insert(0, valores[2])
        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, valores[3])
        entry_edad.set(valores[4])
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, valores[5])
        entry_correo.delete(0, tk.END)
        entry_correo.insert(0, valores[6])
        entry_fecha_ingreso.delete(0, tk.END)
        entry_fecha_ingreso.insert(0, valores[7])
        entry_rol.set(valores[9])
        entry_contrasena.delete(0, tk.END)
        entry_contrasena.insert(0, valores[10])
    except IndexError:
        pass


def modificar_registro():
    id_personal = entry_id.get()
    if not id_personal:
        messagebox.showwarning("Atención", "Seleccione un registro para modificar.")
        return

    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    direccion = entry_direccion.get()
    edad = entry_edad.get()
    telefono = entry_telefono.get()
    correo = entry_correo.get()
    fecha_ingreso = entry_fecha_ingreso.get()
    rol = entry_rol.get()
    contrasena = entry_contrasena.get()
    vacaciones = calcular_vacaciones(fecha_ingreso)

    conexion, cursor = conectar()
    cursor.execute("""
        UPDATE personal
        SET nombre=?, apellido=?, direccion=?, edad=?, telefono=?, correo=?, fecha_ingreso=?, vacaciones=?, rol=?, contrasena=?
        WHERE id_Personal=?
    """, (nombre, apellido, direccion, edad, telefono, correo, fecha_ingreso, vacaciones, rol, contrasena, id_personal))
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Éxito", "Registro modificado correctamente.")
    mostrar_datos()
    limpiar_campos()
def ventana_confirmacion(accion):
    """Ventana que pide ID y nombre antes de actualizar o eliminar"""
    win = tk.Toplevel(ventana)
    win.title(f"Confirmar {accion.capitalize()}")
    win.geometry("320x220")
    win.resizable(False, False)
    win.configure(bg="#E0FFFF")

    tk.Label(win, text="Ingrese ID del personal:", bg="#E0FFFF").pack(pady=5)
    entry_id_conf = tk.Entry(win)
    entry_id_conf.pack(pady=5)

    tk.Label(win, text="Ingrese Nombre del personal:", bg="#E0FFFF").pack(pady=5)
    entry_nombre_conf = tk.Entry(win)
    entry_nombre_conf.pack(pady=5)

    def confirmar():
        id_personal = entry_id_conf.get().strip()
        nombre_personal = entry_nombre_conf.get().strip()

        if not id_personal or not nombre_personal:
            messagebox.showwarning("Campos vacíos", "Debe ingresar el ID y el nombre.")
            return

        conexion, cursor = conectar()
        cursor.execute("SELECT * FROM personal WHERE id_Personal=? AND nombre=?", (id_personal, nombre_personal))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "No se encontró un registro con ese ID y nombre.")
            conexion.close()
            return


        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, registro[0])
        entry_id.config(state="readonly")

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, registro[1])
        entry_apellido.delete(0, tk.END)
        entry_apellido.insert(0, registro[2])
        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, registro[3])
        entry_edad.set(registro[4])
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, registro[5])
        entry_correo.delete(0, tk.END)
        entry_correo.insert(0, registro[6])
        entry_fecha_ingreso.delete(0, tk.END)
        entry_fecha_ingreso.insert(0, registro[7])
        entry_rol.set(registro[9])
        entry_contrasena.delete(0, tk.END)
        entry_contrasena.insert(0, registro[10])

        conexion.close()
        win.destroy()


        if accion == "eliminar":
            confirmar_eliminar(id_personal, nombre_personal)
        else:
            messagebox.showinfo("Modificar", "Ahora puede editar los campos y presionar GUARDAR CAMBIOS.")


    frame_botones = tk.Frame(win, bg="#E0FFFF")
    frame_botones.pack(pady=15)
    tk.Button(frame_botones, text="Confirmar", bg="#6fa8dc", width=10, command=confirmar).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Cancelar", bg="#e06666", width=10, command=win.destroy).grid(row=0, column=1, padx=5)
def modificar_datos(id_personal):
    """Actualiza el registro con los datos ingresados actualmente en los campos"""
    conexion, cursor = conectar()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    direccion = entry_direccion.get()
    edad = entry_edad.get()
    telefono = entry_telefono.get()
    correo = entry_correo.get()
    fecha_ingreso = entry_fecha_ingreso.get()
    rol = entry_rol.get()
    contrasena = entry_contrasena.get()
    vacaciones = calcular_vacaciones(fecha_ingreso)

    cursor.execute("""
        UPDATE personal
        SET nombre=?, apellido=?, direccion=?, edad=?, telefono=?, correo=?, fecha_ingreso=?, vacaciones=?, rol=?, contrasena=?
        WHERE id_Personal=?
    """, (nombre, apellido, direccion, edad, telefono, correo, fecha_ingreso, vacaciones, rol, contrasena, id_personal))
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Éxito", f"Registro ID {id_personal} actualizado correctamente.")
    mostrar_datos()
    limpiar_campos()


def confirmar_eliminar(id_personal, nombre_personal):
    """Elimina el registro después de confirmar"""
    respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el registro de {nombre_personal}?")
    if not respuesta:
        return

    conexion, cursor = conectar()
    cursor.execute("DELETE FROM personal WHERE id_Personal=?", (id_personal,))
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Éxito", f"Registro de {nombre_personal} eliminado correctamente.")
    mostrar_datos()
    limpiar_campos()


def modificar_registro():
    """Abre la ventana para confirmar antes de modificar"""
    ventana_confirmacion("modificar")


def eliminar_registro():
    """Abre la ventana de confirmación antes de eliminar"""
    ventana_confirmacion("eliminar")

def limpiar_campos():
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_edad.set("")
    entry_telefono.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_fecha_ingreso.delete(0, tk.END)
    entry_rol.set("")
    entry_contrasena.delete(0, tk.END)
    entry_id.config(state="readonly")


def validar_telefono(texto):
    return texto.isdigit() and len(texto) <= 8 or texto == ""



ventana = tk.Tk()
ventana.title("Gestión de Personal")
ventana.geometry("1000x700")
ventana.configure(bg="#E0FFFF")

tk.Label(ventana, text="ID:", bg="#E0FFFF").grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(ventana, state="readonly")
entry_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(ventana, text="Nombre:", bg="#E0FFFF").grid(row=1, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=1, column=1, padx=5, pady=5)

tk.Label(ventana, text="Apellido:", bg="#E0FFFF").grid(row=2, column=0, padx=5, pady=5)
entry_apellido = tk.Entry(ventana)
entry_apellido.grid(row=2, column=1, padx=5, pady=5)

tk.Label(ventana, text="Dirección:", bg="#E0FFFF").grid(row=3, column=0, padx=5, pady=5)
entry_direccion = tk.Entry(ventana)
entry_direccion.grid(row=3, column=1, padx=5, pady=5)

tk.Label(ventana, text="Edad:", bg="#E0FFFF").grid(row=4, column=0, padx=5, pady=5)
edades = [str(i) for i in range(18, 61)]
entry_edad = ttk.Combobox(ventana, values=edades, state="readonly")
entry_edad.grid(row=4, column=1, padx=5, pady=5)

tk.Label(ventana, text="Teléfono:", bg="#E0FFFF").grid(row=5, column=0, padx=5, pady=5)
validacion_tel = ventana.register(validar_telefono)
entry_telefono = tk.Entry(ventana, validate="key", validatecommand=(validacion_tel, "%P"))
entry_telefono.grid(row=5, column=1, padx=5, pady=5)

tk.Label(ventana, text="Correo:", bg="#E0FFFF").grid(row=6, column=0, padx=5, pady=5)
entry_correo = tk.Entry(ventana)
entry_correo.grid(row=6, column=1, padx=5, pady=5)

tk.Label(ventana, text="Fecha Ingreso (YYYY-MM-DD):", bg="#E0FFFF").grid(row=7, column=0, padx=5, pady=5)
entry_fecha_ingreso = tk.Entry(ventana)
entry_fecha_ingreso.grid(row=7, column=1, padx=5, pady=5)

tk.Label(ventana, text="Rol:", bg="#E0FFFF").grid(row=8, column=0, padx=5, pady=5)
roles = ["Coordinador", "Supervisor", "Técnico"]
entry_rol = ttk.Combobox(ventana, values=roles, state="readonly")
entry_rol.grid(row=8, column=1, padx=5, pady=5)

tk.Label(ventana, text="Contraseña:", bg="#E0FFFF").grid(row=9, column=0, padx=5, pady=5)
entry_contrasena = tk.Entry(ventana, show="*")
entry_contrasena.grid(row=9, column=1, padx=5, pady=5)

tk.Button(ventana, text="Guardar", command=guardar_personal, bg="#B0E0E6", width=18).grid(row=2, column=3, pady=10)
tk.Button(ventana, text="Cargar para Modificar", command=modificar_registro, bg="#B0E0E6", width=18).grid(row=4, column=3, pady=10)
tk.Button(ventana, text="Guardar Cambios", command=guardar_cambios, bg="#B0E0E6", width=18).grid(row=6, column=3, pady=10)
tk.Button(ventana, text="Eliminar", command=eliminar_registro, bg="#B0E0E6", width=18).grid(row=8, column=3, pady=10)
tk.Button(ventana, text="Limpiar", command=limpiar_campos, bg="#B0E0E6", width=18).grid(row=2, column=4, pady=10)
tk.Button(ventana, text="Actualizar Vacaciones", command=calcular_vacaciones, bg="#B0E0E6", width=18).grid(row=4, column=4, pady=10)
tk.Button(ventana,text="Salir", command=ventana.quit,bg="#B0E0E6", width=18).grid(row=6, column=4, pady=10)


columnas = ("ID", "Nombre", "Apellido", "Dirección", "Edad", "Teléfono", "Correo", "Fecha Ingreso", "Vacaciones", "Rol", "Contraseña")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=90)
tabla.grid(row=11, column=0, columnspan=6, padx=10, pady=10)
tabla.bind("<ButtonRelease-1>", seleccionar_registro)

mostrar_datos()
ventana.mainloop()