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
                   CREATE TABLE IF NOT EXISTS Vacaciones
                   (
                       Id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       id_personal
                       TEXT
                       NOT
                       NULL,
                       nombre
                       TEXT
                       NOT
                       NULL,
                       dias_go
                       INTEGER
                       NOT
                       NULL
                   )
                   ''')
    conexion.commit()
    return conexion, cursor


def cargar_personal():
    try:
        conn = sqlite3.connect('personal.db')
        cur = conn.cursor()
        cur.execute("SELECT id_Personal, nombre || ' ' || apellido, vacaciones FROM personal")
        datos = cur.fetchall()
        conn.close()
        return datos
    except Exception as e:
        messagebox.showerror("Error BD", f"No se pudo conectar a personal.db:\n{e}")
        return []


def mostrar_vacaciones(frame_padre, volver_menu, usuario_actual):
    """Función para mostrar el módulo de vacaciones integrado"""

    # VERIFICACIÓN DE PERMISOS - Solo Supervisores y Coordinadores pueden acceder
    if usuario_actual['rol'] not in ['Supervisor', 'Coordinador']:
        messagebox.showerror("Acceso Denegado",
                             "No tiene permisos para acceder al módulo de Vacaciones.\n"
                             "Solo Supervisores y Coordinadores pueden gestionar vacaciones.")
        volver_menu()
        return

    # Limpiar frame padre
    for widget in frame_padre.winfo_children():
        widget.destroy()

    # Título
    tk.Label(frame_padre, text="Gestión de Vacaciones",
             font=("Arial", 16, "bold"), bg="#E0FFFF").pack(pady=10)

    # Frame principal
    frame_principal = tk.Frame(frame_padre, bg="#E0FFFF")
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Campos de entrada
    campos_frame = tk.Frame(frame_principal, bg="#E0FFFF")
    campos_frame.pack(pady=10)

    # Cargar datos del personal al inicio
    datos_personal = cargar_personal()

    # ID Personal
    tk.Label(campos_frame, text="ID Personal:", bg="#E0FFFF").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    combo_personal_id = ttk.Combobox(campos_frame, width=20, state="readonly")
    combo_personal_id.grid(row=0, column=1, padx=10, pady=5)
    if datos_personal:
        combo_personal_id['values'] = [d[0] for d in datos_personal]

    # Nombre
    tk.Label(campos_frame, text="Nombre:", bg="#E0FFFF").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    combo_personal_nombre = ttk.Combobox(campos_frame, width=20, state="readonly")
    combo_personal_nombre.grid(row=1, column=1, padx=10, pady=5)
    if datos_personal:
        combo_personal_nombre['values'] = [d[1] for d in datos_personal]

    # Días a Gozar
    tk.Label(campos_frame, text="Días a Gozar:", bg="#E0FFFF").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_dias_go = tk.Entry(campos_frame, width=23)
    entry_dias_go.grid(row=2, column=1, padx=10, pady=5)

    # --- Funciones internas ---
    def actualizar_nombre(event):
        id_sel = combo_personal_id.get()
        for p in datos_personal:
            if str(p[0]) == str(id_sel):
                combo_personal_nombre.set(p[1])
                # Mostrar días disponibles
                messagebox.showinfo("Días Disponibles", f"El empleado tiene {p[2]} días de vacaciones disponibles.")
                break

    def guardar():
        try:
            id_personal = combo_personal_id.get()
            nombre = combo_personal_nombre.get()
            dias_go = entry_dias_go.get()

            if not id_personal or not nombre or not dias_go:
                messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
                return

            try:
                dias_go = int(dias_go)
                if dias_go <= 0:
                    messagebox.showwarning("Error", "Los días a gozar deben ser un número positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Los días a gozar deben ser un número válido.")
                return

            # Verificar días disponibles en personal.db
            conn_p = sqlite3.connect('personal.db')
            cur_p = conn_p.cursor()
            cur_p.execute("SELECT vacaciones FROM personal WHERE id_Personal=?", (id_personal,))
            resultado = cur_p.fetchone()

            if not resultado:
                messagebox.showerror("Error", "No se encontró el empleado en personal.db")
                conn_p.close()
                return

            dias_actuales = resultado[0]

            if dias_go > dias_actuales:
                messagebox.showwarning("Advertencia", f"El empleado solo tiene {dias_actuales} días disponibles.")
                conn_p.close()
                return

            nuevos_dias = dias_actuales - dias_go

            # Guardar en Vacaciones.db
            conexion, cursor = Conectar()
            cursor.execute('''
                           INSERT INTO Vacaciones (id_personal, nombre, dias_go)
                           VALUES (?, ?, ?)
                           ''', (id_personal, nombre, dias_go))
            conexion.commit()
            conexion.close()

            # Actualizar días en personal.db
            cur_p.execute("UPDATE personal SET vacaciones=? WHERE id_Personal=?", (nuevos_dias, id_personal))
            conn_p.commit()
            conn_p.close()

            messagebox.showinfo("Éxito", f"Registro guardado correctamente.\nDías restantes: {nuevos_dias}")
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

    def eliminar_registro():
        selection = tabla.selection()
        if not selection:
            messagebox.showwarning("Atención", "Seleccione un registro para eliminar.")
            return

        item = tabla.item(selection[0])
        id_registro = item['values'][0]
        nombre_empleado = item['values'][2]
        dias_gozados = item['values'][3]

        respuesta = messagebox.askyesno("Confirmar eliminación",
                                        f"¿Desea eliminar el registro de {nombre_empleado}?\nDías gozados: {dias_gozados}")
        if not respuesta:
            return

        try:
            # Restaurar días en personal.db
            id_personal = item['values'][1]
            conn_p = sqlite3.connect('personal.db')
            cur_p = conn_p.cursor()
            cur_p.execute("SELECT vacaciones FROM personal WHERE id_Personal=?", (id_personal,))
            dias_actuales = cur_p.fetchone()[0]
            nuevos_dias = dias_actuales + dias_gozados

            cur_p.execute("UPDATE personal SET vacaciones=? WHERE id_Personal=?", (nuevos_dias, id_personal))
            conn_p.commit()
            conn_p.close()

            # Eliminar de Vacaciones.db
            conexion, cursor = Conectar()
            cursor.execute("DELETE FROM Vacaciones WHERE Id=?", (id_registro,))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito",
                                f"Registro eliminado correctamente.\nDías restaurados: {dias_gozados}\nTotal días disponibles: {nuevos_dias}")
            mostrar_datos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")

    def limpiar_campos():
        combo_personal_id.set("")
        combo_personal_nombre.set("")
        entry_dias_go.delete(0, tk.END)

    def actualizar_lista_personal():
        nonlocal datos_personal
        datos_personal = cargar_personal()
        if datos_personal:
            combo_personal_id['values'] = [d[0] for d in datos_personal]
            combo_personal_nombre['values'] = [d[1] for d in datos_personal]
            messagebox.showinfo("Actualizado", "Lista de personal actualizada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No se pudieron cargar los datos del personal.")

    # Vincular evento de selección
    combo_personal_id.bind("<<ComboboxSelected>>", actualizar_nombre)

    # --- Botones ---
    botones_frame = tk.Frame(frame_principal, bg="#E0FFFF")
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Guardar", command=guardar, bg="#4CAF50",
              fg="white", width=15).grid(row=0, column=0, padx=5)
    tk.Button(botones_frame, text="Eliminar", command=eliminar_registro, bg="#f44336",
              fg="white", width=15).grid(row=0, column=1, padx=5)
    tk.Button(botones_frame, text="Limpiar", command=limpiar_campos,
              width=15).grid(row=0, column=2, padx=5)
    tk.Button(botones_frame, text="Actualizar Lista", command=actualizar_lista_personal,
              bg="#2196F3", fg="white", width=15).grid(row=0, column=3, padx=5)
    tk.Button(botones_frame, text="Volver al Menú", command=volver_menu,
              bg="#FFB6C1", width=15).grid(row=0, column=4, padx=5)

    # --- Tabla de registros ---
    tabla_frame = tk.Frame(frame_principal, bg="#E0FFFF")
    tabla_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columnas = ("Id", "ID Personal", "Nombre", "Días a Gozar")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)

    # Scrollbar para la tabla
    scrollbar = tk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Cargar datos iniciales
    mostrar_datos()