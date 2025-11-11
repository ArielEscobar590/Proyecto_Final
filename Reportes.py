
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import Horas_Extra as he
import Vacaciones as v
import Gestion_Personal as gp
from datetime import datetime, timedelta


fallas = ["Fusible quemado", "Cable dañado", "Conector con zarro", "Movimiento de poste",
          "Nodo inhibido", "Problema de energía comercial"]
DB_NAME_REPORTES = "reporte.db"


class Reporte_falla:
    def __init__(self, fecha, orden, hora_inicio, hora_fin, solucion, tecnico_creador, tecnico_companero):
        self.fecha = fecha
        self.orden = orden
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solucion = solucion
        self.tecnico_creador = tecnico_creador
        self.tecnico_companero = tecnico_companero

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME_REPORTES)
        conn.row_factory = sqlite3.Row
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS Reporte_Falla
                     (
                         num_falla
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         fecha
                         TEXT
                         NOT
                         NULL,
                         orden
                         TEXT
                         NOT
                         NULL,
                         inicio
                         TEXT
                         NOT
                         NULL,
                         fin
                         TEXT
                         NOT
                         NULL,
                         solucion
                         TEXT
                         NOT
                         NULL,
                         tecnico_creador
                         TEXT
                         NOT
                         NULL,
                         tecnico_companero
                         TEXT
                         NOT
                         NULL
                     );
                     """)
        conn.commit()
        return conn

    def guardar(self):
        try:
            with self._conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Reporte_Falla (fecha, orden, inicio, fin, solucion, tecnico_creador, tecnico_companero) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (self.fecha, self.orden, self.hora_inicio, self.hora_fin, self.solucion, self.tecnico_creador,
                     self.tecnico_companero)
                )
                conn.commit()
                num_falla = cursor.lastrowid
                messagebox.showinfo("Éxito",
                                    f"Reporte '{self.orden}' guardado con éxito.\nNúmero de falla: {num_falla}")
                return num_falla
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el reporte: {e}")
            return None

    @staticmethod
    def listar():
        try:
            with Reporte_falla._conn() as conn:
                cur = conn.execute("SELECT * FROM Reporte_Falla ORDER BY num_falla DESC")
                return cur.fetchall()
        except Exception as e:
            print(f"Error al listar reportes: {e}")
            return []

    @staticmethod
    def actualizar(num_falla, fecha, orden, hora_inicio, hora_fin, solucion, tecnico_creador, tecnico_companero):
        try:
            with Reporte_falla._conn() as conn:
                conn.execute(
                    "UPDATE Reporte_Falla SET fecha=?, orden=?, inicio=?, fin=?, solucion=?, tecnico_creador=?, tecnico_companero=? WHERE num_falla=?",
                    (fecha, orden, hora_inicio, hora_fin, solucion, tecnico_creador, tecnico_companero, num_falla)
                )
                conn.commit()
            messagebox.showinfo("Éxito", f"Reporte '{orden}' actualizado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el reporte: {e}")

    @staticmethod
    def eliminar(num_falla):
        try:
            with Reporte_falla._conn() as conn:
                conn.execute("DELETE FROM Reporte_Falla WHERE num_falla=?", (num_falla,))
                conn.commit()
            messagebox.showinfo("Eliminado", "Reporte eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el reporte: {e}")

    @staticmethod
    def obtener_por_id(num_falla):
        try:
            with Reporte_falla._conn() as conn:
                cur = conn.execute("SELECT * FROM Reporte_Falla WHERE num_falla=?", (num_falla,))
                return cur.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener el reporte: {e}")
            return None


class Reportes:
    def __init__(self, frame_padre, volver_menu, usuario_actual):
        self.frame_padre = frame_padre
        self.volver_menu = volver_menu
        self.usuario_actual = usuario_actual
        self.mostrar_interfaz()

    def obtener_tecnicos_desde_bd(self):
        try:
            conn = sqlite3.connect("personal.db")
            cur = conn.cursor()
            cur.execute(
                "SELECT id_Personal, nombre || ' ' || apellido FROM personal WHERE rol = 'Técnico' AND id_Personal != ?",
                (self.usuario_actual['id'],))
            datos = cur.fetchall()
            conn.close()
            return datos
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudieron cargar los Técnicos:\n{e}")
            return []

    def mostrar_interfaz(self):
        for widget in self.frame_padre.winfo_children():
            widget.destroy()

        tk.Label(self.frame_padre, text="Gestión de Reportes de Falla",
                 font=("Arial", 16, "bold"), bg="#E0FFFF").pack(pady=10)

        frame_principal = tk.Frame(self.frame_padre, bg="#E0FFFF")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)


        frame_form = tk.LabelFrame(frame_principal, text="Nuevo Reporte", bg="#E0FFFF", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=10)


        tk.Label(frame_form, text="Fecha:", bg="#E0FFFF").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        fechas = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
        self.fecha_cb = ttk.Combobox(frame_form, values=fechas, state="readonly", width=37)
        self.fecha_cb.set(datetime.now().strftime("%Y-%m-%d"))
        self.fecha_cb.grid(row=0, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Orden:", bg="#E0FFFF").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.orden_entry = tk.Entry(frame_form, width=40)
        self.orden_entry.grid(row=1, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Hora Inicio:", bg="#E0FFFF").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ophora = [f"{i:02}" for i in range(0, 24)]  # CORREGIDO
        opmin = [f"{i:02}" for i in range(0, 60, 5)]

        frame_hora_inicio = tk.Frame(frame_form, bg="#EAF4F4")
        frame_hora_inicio.grid(row=2, column=1, columnspan=2, sticky="w")
        self.hora_inicio_cb = ttk.Combobox(frame_hora_inicio, values=ophora, state="readonly", width=5)
        self.hora_inicio_cb.set("08")
        self.hora_inicio_cb.grid(row=0, column=0, padx=2)
        tk.Label(frame_hora_inicio, text="H", bg="#EAF4F4").grid(row=0, column=1)
        self.min_inicio_cb = ttk.Combobox(frame_hora_inicio, values=opmin, state="readonly", width=5)
        self.min_inicio_cb.set("00")
        self.min_inicio_cb.grid(row=0, column=2, padx=2)
        tk.Label(frame_hora_inicio, text="MIN", bg="#EAF4F4").grid(row=0, column=3)


        tk.Label(frame_form, text="Hora Fin:", bg="#E0FFFF").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        frame_hora_fin = tk.Frame(frame_form, bg="#EAF4F4")
        frame_hora_fin.grid(row=3, column=1, columnspan=2, sticky="w")
        self.hora_fin_cb = ttk.Combobox(frame_hora_fin, values=ophora, state="readonly", width=5)  # CORREGIDO
        self.hora_fin_cb.set("17")
        self.hora_fin_cb.grid(row=0, column=0, padx=2)
        tk.Label(frame_hora_fin, text="H", bg="#EAF4F4").grid(row=0, column=1)
        self.min_fin_cb = ttk.Combobox(frame_hora_fin, values=opmin, state="readonly", width=5)
        self.min_fin_cb.set("00")
        self.min_fin_cb.grid(row=0, column=2, padx=2)
        tk.Label(frame_hora_fin, text="MIN", bg="#EAF4F4").grid(row=0, column=3)


        tk.Label(frame_form, text="Solución:", bg="#E0FFFF").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.solucion_cb = ttk.Combobox(frame_form, values=fallas, state="readonly", width=37)
        self.solucion_cb.grid(row=4, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Técnico Creador:", bg="#E0FFFF").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        tecnico_creador = f"{self.usuario_actual['nombre']} {self.usuario_actual['apellido']} (ID: {self.usuario_actual['id']})"
        lbl_tecnico_creador = tk.Label(frame_form, text=tecnico_creador, bg="#E0FFFF", fg="blue")
        lbl_tecnico_creador.grid(row=5, column=1, padx=5, pady=5, sticky="w")


        tk.Label(frame_form, text="Técnico que Acompaña:", bg="#E0FFFF").grid(row=6, column=0, sticky="e", padx=5,
                                                                              pady=5)
        self.tecnicos_disponibles = self.obtener_tecnicos_desde_bd()
        if not self.tecnicos_disponibles:
            self.tecnicos_disponibles = [("", "No hay técnicos disponibles")]

        self.tecnico_companero_cb = ttk.Combobox(frame_form, values=[t[1] for t in self.tecnicos_disponibles],
                                                 state="readonly", width=37)
        if self.tecnicos_disponibles:
            self.tecnico_companero_cb.set(self.tecnicos_disponibles[0][1])
        self.tecnico_companero_cb.grid(row=6, column=1, padx=5, pady=5)

        # Botones
        frame_botones_form = tk.Frame(frame_form, bg="#E0FFFF")
        frame_botones_form.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(frame_botones_form, text="Guardar Reporte", command=self.guardar_reporte,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones_form, text="Volver al Menú", command=self.volver_menu,
                  bg="#FFB6C1", fg="black", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)


        frame_tabla = tk.Frame(frame_principal, bg="#E0FFFF")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("num_falla", "fecha", "orden", "inicio", "fin", "solucion", "tecnico_creador", "tecnico_companero")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)


        encabezados = ["N° Falla", "Fecha", "Orden", "Inicio", "Fin", "Solución", "Técnico Creador",
                       "Técnico Acompañante"]
        for col, enc in zip(columnas, encabezados):
            self.tabla.heading(col, text=enc)
            self.tabla.column(col, width=120)

        scrollbar = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.actualizar_tabla()

    def guardar_reporte(self):

        fecha = self.fecha_cb.get()
        orden = self.orden_entry.get().strip()
        hora_inicio = f"{self.hora_inicio_cb.get()}:{self.min_inicio_cb.get()}"
        hora_fin = f"{self.hora_fin_cb.get()}:{self.min_fin_cb.get()}"
        solucion = self.solucion_cb.get()
        tecnico_creador = f"{self.usuario_actual['nombre']} {self.usuario_actual['apellido']} (ID: {self.usuario_actual['id']})"


        index = self.tecnico_companero_cb.current()
        if index < 0:
            messagebox.showerror("Error", "Debe seleccionar un técnico que lo acompañe.")
            return

        if self.tecnicos_disponibles and self.tecnicos_disponibles[0][0] == "":
            messagebox.showerror("Error", "No hay técnicos disponibles para seleccionar.")
            return

        tecnico_companero = self.tecnicos_disponibles[index][1]


        if not all([fecha, orden, hora_inicio, hora_fin, solucion]):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return


        reporte = Reporte_falla(fecha, orden, hora_inicio, hora_fin, solucion, tecnico_creador, tecnico_companero)
        if reporte.guardar() is not None:

            self.orden_entry.delete(0, tk.END)
            self.solucion_cb.set('')
            self.actualizar_tabla()

    def actualizar_tabla(self):

        for row in self.tabla.get_children():
            self.tabla.delete(row)


        reportes = Reporte_falla.listar()
        for reporte in reportes:
            self.tabla.insert("", tk.END, values=(
                reporte['num_falla'],
                reporte['fecha'],
                reporte['orden'],
                reporte['inicio'],
                reporte['fin'],
                reporte['solucion'],
                reporte['tecnico_creador'],
                reporte['tecnico_companero']
            ))


class ModificarReportes:
    def __init__(self, frame_padre, volver_menu, usuario_actual):
        self.frame_padre = frame_padre
        self.volver_menu = volver_menu
        self.usuario_actual = usuario_actual
        self.mostrar_interfaz()

    def obtener_tecnicos_desde_bd(self):
        try:
            conn = sqlite3.connect("personal.db")
            cur = conn.cursor()
            cur.execute("SELECT id_Personal, nombre || ' ' || apellido FROM personal WHERE rol = 'Técnico'")
            datos = cur.fetchall()
            conn.close()
            return datos
        except Exception as e:
            messagebox.showerror("Error BD", f"No se pudieron cargar los Técnicos:\n{e}")
            return []

    def mostrar_interfaz(self):
        for widget in self.frame_padre.winfo_children():
            widget.destroy()

        tk.Label(self.frame_padre, text="Modificar Reportes de Falla",
                 font=("Arial", 16, "bold"), bg="#E0FFFF").pack(pady=10)

        frame_principal = tk.Frame(self.frame_padre, bg="#E0FFFF")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)


        frame_form = tk.LabelFrame(frame_principal, text="Editar Reporte", bg="#E0FFFF", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=10)


        tk.Label(frame_form, text="Número de Falla:", bg="#E0FFFF").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_num_falla = tk.Entry(frame_form, state="readonly", width=37)
        self.entry_num_falla.grid(row=0, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Fecha (YYYY-MM-DD):", bg="#E0FFFF").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_fecha = tk.Entry(frame_form, width=40)
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Orden:", bg="#E0FFFF").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_orden = tk.Entry(frame_form, width=40)
        self.entry_orden.grid(row=2, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Hora Inicio (HH:MM):", bg="#E0FFFF").grid(row=3, column=0, sticky="e", padx=5,
                                                                             pady=5)
        self.entry_hora_inicio = tk.Entry(frame_form, width=40)
        self.entry_hora_inicio.grid(row=3, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Hora Fin (HH:MM):", bg="#E0FFFF").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.entry_hora_fin = tk.Entry(frame_form, width=40)
        self.entry_hora_fin.grid(row=4, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Solución:", bg="#E0FFFF").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.cb_solucion = ttk.Combobox(frame_form, values=fallas, state="readonly", width=37)
        self.cb_solucion.grid(row=5, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Técnico Creador:", bg="#E0FFFF").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.entry_tecnico_creador = tk.Entry(frame_form, width=40)
        self.entry_tecnico_creador.grid(row=6, column=1, padx=5, pady=5)


        tk.Label(frame_form, text="Técnico que Acompaña:", bg="#E0FFFF").grid(row=7, column=0, sticky="e", padx=5,
                                                                              pady=5)
        tecnicos = self.obtener_tecnicos_desde_bd()
        self.cb_tecnico_companero = ttk.Combobox(frame_form, values=[t[1] for t in tecnicos], state="readonly",
                                                 width=37)
        self.cb_tecnico_companero.grid(row=7, column=1, padx=5, pady=5)
        self.tecnicos = tecnicos


        frame_botones_form = tk.Frame(frame_form, bg="#E0FFFF")
        frame_botones_form.grid(row=8, column=0, columnspan=2, pady=10)

        tk.Button(frame_botones_form, text="Cargar Reporte", command=self.cargar_reporte,
                  bg="#2196F3", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones_form, text="Guardar Cambios", command=self.guardar_cambios,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones_form, text="Eliminar Reporte", command=self.eliminar_reporte,
                  bg="#f44336", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones_form, text="Volver al Menú", command=self.volver_menu,
                  bg="#FFB6C1", fg="black", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5)


        frame_tabla = tk.Frame(frame_principal, bg="#E0FFFF")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("num_falla", "fecha", "orden", "inicio", "fin", "solucion", "tecnico_creador", "tecnico_companero")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        encabezados = ["N° Falla", "Fecha", "Orden", "Inicio", "Fin", "Solución", "Técnico Creador",
                       "Técnico Acompañante"]
        for col, enc in zip(columnas, encabezados):
            self.tabla.heading(col, text=enc)
            self.tabla.column(col, width=120)

        scrollbar = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_reporte)
        self.actualizar_tabla()

    def cargar_reporte(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un reporte de la tabla.")
            return

        item = self.tabla.item(seleccion[0])
        valores = item['values']

        self.entry_num_falla.config(state="normal")
        self.entry_num_falla.delete(0, tk.END)
        self.entry_num_falla.insert(0, valores[0])
        self.entry_num_falla.config(state="readonly")

        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, valores[1])

        self.entry_orden.delete(0, tk.END)
        self.entry_orden.insert(0, valores[2])

        self.entry_hora_inicio.delete(0, tk.END)
        self.entry_hora_inicio.insert(0, valores[3])

        self.entry_hora_fin.delete(0, tk.END)
        self.entry_hora_fin.insert(0, valores[4])

        self.cb_solucion.set(valores[5])

        self.entry_tecnico_creador.delete(0, tk.END)
        self.entry_tecnico_creador.insert(0, valores[6])

        self.cb_tecnico_companero.set(valores[7])

    def guardar_cambios(self):
        num_falla = self.entry_num_falla.get().strip()
        if not num_falla:
            messagebox.showwarning("Advertencia", "Cargue un reporte para modificar.")
            return

        fecha = self.entry_fecha.get().strip()
        orden = self.entry_orden.get().strip()
        hora_inicio = self.entry_hora_inicio.get().strip()
        hora_fin = self.entry_hora_fin.get().strip()
        solucion = self.cb_solucion.get()
        tecnico_creador = self.entry_tecnico_creador.get().strip()
        tecnico_companero = self.cb_tecnico_companero.get()

        if not all([fecha, orden, hora_inicio, hora_fin, solucion, tecnico_creador, tecnico_companero]):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        Reporte_falla.actualizar(num_falla, fecha, orden, hora_inicio, hora_fin, solucion, tecnico_creador,
                                 tecnico_companero)
        self.actualizar_tabla()
        self.limpiar_campos()

    def eliminar_reporte(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un reporte de la tabla.")
            return

        item = self.tabla.item(seleccion[0])
        num_falla = item['values'][0]
        orden = item['values'][2]

        respuesta = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el reporte {num_falla} - {orden}?")
        if respuesta:
            Reporte_falla.eliminar(num_falla)
            self.actualizar_tabla()
            self.limpiar_campos()

    def seleccionar_reporte(self, event):
        self.cargar_reporte()

    def actualizar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        reportes = Reporte_falla.listar()
        for reporte in reportes:
            self.tabla.insert("", tk.END, values=(
                reporte['num_falla'],
                reporte['fecha'],
                reporte['orden'],
                reporte['inicio'],
                reporte['fin'],
                reporte['solucion'],
                reporte['tecnico_creador'],
                reporte['tecnico_companero']
            ))

    def limpiar_campos(self):
        self.entry_num_falla.config(state="normal")
        self.entry_num_falla.delete(0, tk.END)
        self.entry_num_falla.config(state="readonly")
        self.entry_fecha.delete(0, tk.END)
        self.entry_orden.delete(0, tk.END)
        self.entry_hora_inicio.delete(0, tk.END)
        self.entry_hora_fin.delete(0, tk.END)
        self.cb_solucion.set('')
        self.entry_tecnico_creador.delete(0, tk.END)
        self.cb_tecnico_companero.set('')


def mostrar_reportes(frame_padre, volver_menu, usuario_actual):
    Reportes(frame_padre, volver_menu, usuario_actual)


def mostrar_modificar_reportes(frame_padre, volver_menu, usuario_actual):
    ModificarReportes(frame_padre, volver_menu, usuario_actual)





