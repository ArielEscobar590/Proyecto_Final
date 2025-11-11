import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


class GestionPersonal:
    def __init__(self, frame_padre, volver_menu, usuario_actual):
        self.frame_padre = frame_padre
        self.volver_menu = volver_menu
        self.usuario_actual = usuario_actual
        self.mostrar_interfaz()

    def conectar(self):
        conexion = sqlite3.connect('personal.db')
        cursor = conexion.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS personal
                       (
                           id_Personal
                           TEXT
                           PRIMARY
                           KEY,
                           nombre
                           TEXT
                           NOT
                           NULL,
                           apellido
                           TEXT
                           NOT
                           NULL,
                           direccion
                           TEXT
                           NOT
                           NULL,
                           edad
                           INTEGER
                           NOT
                           NULL,
                           telefono
                           TEXT
                           NOT
                           NULL,
                           correo
                           TEXT
                           NOT
                           NULL,
                           fecha_ingreso
                           TEXT
                           NOT
                           NULL,
                           vacaciones
                           INTEGER,
                           rol
                           TEXT
                           NOT
                           NULL,
                           contrasena
                           TEXT
                           NOT
                           NULL
                       )
                       """)
        conexion.commit()
        return conexion, cursor

    def calcular_vacaciones(self, fecha_ingreso):
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

    def mostrar_interfaz(self):

        for widget in self.frame_padre.winfo_children():
            widget.destroy()


        tk.Label(self.frame_padre, text="Gestión de Personal",
                 font=("Arial", 16, "bold"), bg="#E0FFFF").pack(pady=10)


        frame_principal = tk.Frame(self.frame_padre, bg="#E0FFFF")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)


        campos_frame = tk.Frame(frame_principal, bg="#E0FFFF")
        campos_frame.pack(pady=10)


        tk.Label(campos_frame, text="ID Personal:", bg="#E0FFFF").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = tk.Entry(campos_frame, state="readonly")
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Nombre:", bg="#E0FFFF").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = tk.Entry(campos_frame)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Apellido:", bg="#E0FFFF").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_apellido = tk.Entry(campos_frame)
        self.entry_apellido.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Dirección:", bg="#E0FFFF").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_direccion = tk.Entry(campos_frame)
        self.entry_direccion.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Edad:", bg="#E0FFFF").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        edades = [str(i) for i in range(18, 61)]
        self.entry_edad = ttk.Combobox(campos_frame, values=edades, state="readonly")
        self.entry_edad.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Teléfono:", bg="#E0FFFF").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefono = tk.Entry(campos_frame)
        self.entry_telefono.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Correo:", bg="#E0FFFF").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_correo = tk.Entry(campos_frame)
        self.entry_correo.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Fecha Ingreso (YYYY-MM-DD):", bg="#E0FFFF").grid(row=7, column=0, padx=5, pady=5,
                                                                                      sticky="w")
        self.entry_fecha_ingreso = tk.Entry(campos_frame)
        self.entry_fecha_ingreso.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="Rol:", bg="#E0FFFF").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        roles = ["Coordinador", "Supervisor", "Técnico"]
        self.entry_rol = ttk.Combobox(campos_frame, values=roles, state="readonly")
        self.entry_rol.grid(row=8, column=1, padx=5, pady=5)


        tk.Label(campos_frame, text="Contraseña:", bg="#E0FFFF").grid(row=9, column=0, padx=5, pady=5, sticky="w")

        # Frame para contraseña y checkbox
        frame_contrasena = tk.Frame(campos_frame, bg="#E0FFFF")
        frame_contrasena.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        self.entry_contrasena = tk.Entry(frame_contrasena, show="*", width=20)
        self.entry_contrasena.pack(side=tk.LEFT)


        self.var_mostrar_contrasena = tk.BooleanVar()
        chk_mostrar = tk.Checkbutton(
            frame_contrasena, text="Mostrar", variable=self.var_mostrar_contrasena,
            bg="#E0FFFF", command=self.mostrar_contrasena
        )
        chk_mostrar.pack(side=tk.LEFT, padx=(5, 0))


        botones_frame = tk.Frame(frame_principal, bg="#E0FFFF")
        botones_frame.pack(pady=10)

        tk.Button(botones_frame, text="Guardar Nuevo", command=self.guardar_personal,
                  bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(botones_frame, text="Cargar para Modificar", command=self.modificar_registro,
                  bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5)
        tk.Button(botones_frame, text="Guardar Cambios", command=self.guardar_cambios,
                  bg="#FF9800", fg="white", width=15).grid(row=0, column=2, padx=5)
        tk.Button(botones_frame, text="Eliminar", command=self.eliminar_registro,
                  bg="#f44336", fg="white", width=15).grid(row=0, column=3, padx=5)
        tk.Button(botones_frame, text="Limpiar", command=self.limpiar_campos,
                  bg="#607D8B", fg="white", width=15).grid(row=0, column=4, padx=5)
        tk.Button(botones_frame, text="Volver al Menú", command=self.volver_menu,
                  bg="#9C27B0", fg="white", width=15).grid(row=0, column=5, padx=5)

        # Tabla
        tabla_frame = tk.Frame(frame_principal, bg="#E0FFFF")
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("ID", "Nombre", "Apellido", "Dirección", "Edad", "Teléfono", "Correo",
                    "Fecha Ingreso", "Vacaciones", "Rol", "Contraseña")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)

        scrollbar = tk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)
        self.mostrar_datos()

    def mostrar_contrasena(self):

        if self.var_mostrar_contrasena.get():
            self.entry_contrasena.config(show="")
        else:
            self.entry_contrasena.config(show="*")

    def guardar_personal(self):
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        direccion = self.entry_direccion.get().strip()
        edad = self.entry_edad.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()
        fecha_ingreso = self.entry_fecha_ingreso.get().strip()
        rol = self.entry_rol.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not (
                nombre and apellido and direccion and edad and telefono and correo and fecha_ingreso and rol and contrasena):
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

            conexion, cursor = self.conectar()
            cursor.execute("SELECT MAX(CAST(id_Personal AS INTEGER)) FROM personal")
            resultado = cursor.fetchone()
            nuevo_id = str(int(resultado[0] or 0) + 1).zfill(2)

            vacaciones = self.calcular_vacaciones(fecha_ingreso)

            cursor.execute("""
                           INSERT INTO personal (id_Personal, nombre, apellido, direccion, edad, telefono,
                                                 correo, fecha_ingreso, vacaciones, rol, contrasena)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           """, (nuevo_id, nombre, apellido, direccion, edad, telefono, correo,
                                 fecha_ingreso, vacaciones, rol, contrasena))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito",
                                f"Personal guardado correctamente.\nID asignado: {nuevo_id}\nVacaciones: {vacaciones} días.")
            self.limpiar_campos()
            self.mostrar_datos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el registro.\n\nDetalle: {e}")

    def guardar_cambios(self):
        id_personal = self.entry_id.get().strip()
        if not id_personal:
            messagebox.showwarning("Atención", "Debe cargar un registro antes de guardar los cambios.")
            return

        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        direccion = self.entry_direccion.get().strip()
        edad = self.entry_edad.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()
        fecha_ingreso = self.entry_fecha_ingreso.get().strip()
        rol = self.entry_rol.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not (
                nombre and apellido and direccion and edad and telefono and correo and fecha_ingreso and rol and contrasena):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        try:
            edad = int(edad)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return

        vacaciones = self.calcular_vacaciones(fecha_ingreso)

        conexion, cursor = self.conectar()
        cursor.execute("""
                       UPDATE personal
                       SET nombre=?,
                           apellido=?,
                           direccion=?,
                           edad=?,
                           telefono=?,
                           correo=?,
                           fecha_ingreso=?,
                           vacaciones=?,
                           rol=?,
                           contrasena=?
                       WHERE id_Personal = ?
                       """, (nombre, apellido, direccion, edad, telefono, correo,
                             fecha_ingreso, vacaciones, rol, contrasena, id_personal))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", f"Los datos del personal con ID {id_personal} fueron actualizados correctamente.")
        self.mostrar_datos()
        self.limpiar_campos()

    def mostrar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        conexion, cursor = self.conectar()
        cursor.execute("SELECT * FROM personal")
        registros = cursor.fetchall()
        conexion.close()

        for reg in registros:
            self.tabla.insert("", tk.END, values=reg)

    def seleccionar_registro(self, event):
        try:
            item = self.tabla.selection()[0]
            valores = self.tabla.item(item, "values")
            self.entry_id.config(state="normal")
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, valores[0])
            self.entry_id.config(state="readonly")

            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])
            self.entry_apellido.delete(0, tk.END)
            self.entry_apellido.insert(0, valores[2])
            self.entry_direccion.delete(0, tk.END)
            self.entry_direccion.insert(0, valores[3])
            self.entry_edad.set(valores[4])
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, valores[5])
            self.entry_correo.delete(0, tk.END)
            self.entry_correo.insert(0, valores[6])
            self.entry_fecha_ingreso.delete(0, tk.END)
            self.entry_fecha_ingreso.insert(0, valores[7])
            self.entry_rol.set(valores[9])
            self.entry_contrasena.delete(0, tk.END)
            self.entry_contrasena.insert(0, valores[10])


            self.var_mostrar_contrasena.set(False)
            self.entry_contrasena.config(show="*")

        except IndexError:
            pass

    def ventana_confirmacion(self, accion):
        win = tk.Toplevel(self.frame_padre)
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

            conexion, cursor = self.conectar()
            cursor.execute("SELECT * FROM personal WHERE id_Personal=? AND nombre=?", (id_personal, nombre_personal))
            registro = cursor.fetchone()

            if not registro:
                messagebox.showerror("Error", "No se encontró un registro con ese ID y nombre.")
                conexion.close()
                return

            self.entry_id.config(state="normal")
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, registro[0])
            self.entry_id.config(state="readonly")

            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, registro[1])
            self.entry_apellido.delete(0, tk.END)
            self.entry_apellido.insert(0, registro[2])
            self.entry_direccion.delete(0, tk.END)
            self.entry_direccion.insert(0, registro[3])
            self.entry_edad.set(registro[4])
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, registro[5])
            self.entry_correo.delete(0, tk.END)
            self.entry_correo.insert(0, registro[6])
            self.entry_fecha_ingreso.delete(0, tk.END)
            self.entry_fecha_ingreso.insert(0, registro[7])
            self.entry_rol.set(registro[9])
            self.entry_contrasena.delete(0, tk.END)
            self.entry_contrasena.insert(0, registro[10])

            conexion.close()
            win.destroy()

            if accion == "eliminar":
                self.confirmar_eliminar(id_personal, nombre_personal)
            else:
                messagebox.showinfo("Modificar", "Ahora puede editar los campos y presionar GUARDAR CAMBIOS.")

        frame_botones = tk.Frame(win, bg="#E0FFFF")
        frame_botones.pack(pady=15)
        tk.Button(frame_botones, text="Confirmar", bg="#6fa8dc", width=10, command=confirmar).grid(row=0, column=0,
                                                                                                   padx=5)
        tk.Button(frame_botones, text="Cancelar", bg="#e06666", width=10, command=win.destroy).grid(row=0, column=1,
                                                                                                    padx=5)

    def modificar_registro(self):
        self.ventana_confirmacion("modificar")

    def eliminar_registro(self):
        self.ventana_confirmacion("eliminar")

    def confirmar_eliminar(self, id_personal, nombre_personal):
        respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el registro de {nombre_personal}?")
        if not respuesta:
            return

        conexion, cursor = self.conectar()
        cursor.execute("DELETE FROM personal WHERE id_Personal=?", (id_personal,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", f"Registro de {nombre_personal} eliminado correctamente.")
        self.mostrar_datos()
        self.limpiar_campos()

    def limpiar_campos(self):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state="readonly")
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_edad.set("")
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_fecha_ingreso.delete(0, tk.END)
        self.entry_rol.set("")
        self.entry_contrasena.delete(0, tk.END)
        self.var_mostrar_contrasena.set(False)
        self.entry_contrasena.config(show="*")


def mostrar_gestion_personal(frame_padre, volver_menu, usuario_actual):
    GestionPersonal(frame_padre, volver_menu, usuario_actual)