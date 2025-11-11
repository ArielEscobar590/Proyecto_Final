import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

DB_NAME = "mi_base_datos.db"
fallas = [
    "Cambio de fusible",
    "Reparación de línea",
    "Ajuste de transformador",
    "Mantenimiento general",
    "Verificación de conexión",
    "Otro"
]


class HorasExtras:
    def __init__(self, orden, idnodo, hora_inicio, hora_fin, solucion, tecnico):
        self.orden = orden
        self.idnodo = idnodo
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solucion = solucion
        self.tecnico = tecnico

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS horas_extras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orden TEXT NOT NULL,
                idnodo TEXT NOT NULL,
                inicio TEXT NOT NULL,
                fin TEXT NOT NULL,
                solucion TEXT NOT NULL,
                tecnico TEXT NOT NULL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO horas_extras (orden, idnodo, inicio, fin, solucion, tecnico) VALUES (?, ?, ?, ?, ?, ?)",
                (self.orden, self.idnodo, self.hora_inicio, self.hora_fin, self.solucion, self.tecnico)
            )
        messagebox.showinfo("Éxito", f"Horas extra '{self.orden}' guardadas con éxito.")

    @staticmethod
    def listar():
        with HorasExtras._conn() as conn:
            cur = conn.execute("SELECT * FROM horas_extras")
            return cur.fetchall()

    @staticmethod
    def eliminar(id_registro):
        with HorasExtras._conn() as conn:
            conn.execute("DELETE FROM horas_extras WHERE id = ?", (id_registro,))
        messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")


def obtener_tecnicos_desde_bd():
    """Obtiene la lista de técnicos desde la base de datos Personal.db"""
    try:
        conn = sqlite3.connect("personal.db")
        cur = conn.cursor()
        cur.execute("SELECT nombre || ' ' || apellido FROM personal WHERE rol = 'Técnico'")
        datos = cur.fetchall()
        conn.close()
        return [d[0] for d in datos] if datos else ["No hay técnicos disponibles"]
    except Exception as e:
        messagebox.showerror("Error BD", f"No se pudieron cargar los Técnicos:\n{e}")
        return ["Error al cargar técnicos"]


def mostrar_horas_extra(frame_padre, volver_menu, usuario_actual):
    """Módulo de gestión de Horas Extra integrado al menú principal"""
    for widget in frame_padre.winfo_children():
        widget.destroy()

    tk.Label(frame_padre, text="Gestión de Horas Extra",
             font=("Arial Rounded MT Bold", 18), bg="#E0FFFF", fg="#003366").pack(pady=10)

    frame_form = tk.LabelFrame(frame_padre, text="Nuevo Registro de Horas Extra", bg="#E0FFFF", padx=10, pady=10)
    frame_form.pack(fill="x", padx=20, pady=10)

    # --- Orden ---
    tk.Label(frame_form, text="N° Orden:", bg="#E0FFFF").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    orden_entry = tk.Entry(frame_form, width=40)
    orden_entry.grid(row=0, column=1, padx=5, pady=5)

    # --- ID Nodo ---
    tk.Label(frame_form, text="ID Nodo:", bg="#E0FFFF").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    idnodo_entry = tk.Entry(frame_form, width=40)
    idnodo_entry.grid(row=1, column=1, padx=5, pady=5)

    # --- Hora inicio ---
    tk.Label(frame_form, text="Hora Inicio:", bg="#E0FFFF").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    ophora = [f"{i:02}" for i in range(0, 24)]
    opmin = [f"{i:02}" for i in range(0, 60, 5)]

    frame_inicio = tk.Frame(frame_form, bg="#EAF4F4")
    frame_inicio.grid(row=2, column=1, sticky="w")
    hora_inicio_cb = ttk.Combobox(frame_inicio, values=ophora, width=5, state="readonly")
    hora_inicio_cb.set("18")
    hora_inicio_cb.grid(row=0, column=0)
    tk.Label(frame_inicio, text="H", bg="#EAF4F4").grid(row=0, column=1)
    min_inicio_cb = ttk.Combobox(frame_inicio, values=opmin, width=5, state="readonly")
    min_inicio_cb.set("00")
    min_inicio_cb.grid(row=0, column=2)
    tk.Label(frame_inicio, text="MIN", bg="#EAF4F4").grid(row=0, column=3)

    # --- Hora fin ---
    tk.Label(frame_form, text="Hora Fin:", bg="#E0FFFF").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    frame_fin = tk.Frame(frame_form, bg="#EAF4F4")
    frame_fin.grid(row=3, column=1, sticky="w")
    hora_fin_cb = ttk.Combobox(frame_fin, values=ophora, width=5, state="readonly")
    hora_fin_cb.set("21")
    hora_fin_cb.grid(row=0, column=0)
    tk.Label(frame_fin, text="H", bg="#EAF4F4").grid(row=0, column=1)
    min_fin_cb = ttk.Combobox(frame_fin, values=opmin, width=5, state="readonly")
    min_fin_cb.set("00")
    min_fin_cb.grid(row=0, column=2)
    tk.Label(frame_fin, text="MIN", bg="#EAF4F4").grid(row=0, column=3)

    # --- Solución ---
    tk.Label(frame_form, text="Solución:", bg="#E0FFFF").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    solucion_cb = ttk.Combobox(frame_form, values=fallas, width=37, state="readonly")
    solucion_cb.set(fallas[0])
    solucion_cb.grid(row=4, column=1, padx=5, pady=5)

    # --- Técnico ---
    tk.Label(frame_form, text="Técnico que Acompaña:", bg="#E0FFFF").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    tecnicos = obtener_tecnicos_desde_bd()
    tecnico_cb = ttk.Combobox(frame_form, values=tecnicos, state="readonly", width=37)
    tecnico_cb.set(tecnicos[0])
    tecnico_cb.grid(row=5, column=1, padx=5, pady=5)

    # --- Tabla ---
    frame_tabla = tk.Frame(frame_padre, bg="#E0FFFF")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
    tabla = ttk.Treeview(frame_tabla, columns=("id", "orden", "idnodo", "inicio", "fin", "solucion", "tecnico"),
                         show="headings")

    encabezados = ["ID", "Orden", "Nodo", "Inicio", "Fin", "Solución", "Técnico"]
    for col, encabezado in zip(tabla["columns"], encabezados):
        tabla.heading(col, text=encabezado)
        tabla.column(col, width=120)
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    # --- Funciones internas ---
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for fila in HorasExtras.listar():
            tabla.insert("", "end", values=(
                fila["id"], fila["orden"], fila["idnodo"],
                fila["inicio"], fila["fin"], fila["solucion"], fila["tecnico"]
            ))

    def guardar_registro():
        data = {
            "orden": orden_entry.get(),
            "idnodo": idnodo_entry.get(),
            "hora_inicio": f"{hora_inicio_cb.get()}:{min_inicio_cb.get()}",
            "hora_fin": f"{hora_fin_cb.get()}:{min_fin_cb.get()}",
            "solucion": solucion_cb.get(),
            "tecnico": tecnico_cb.get()
        }

        if any(not v for v in data.values()):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        registro = HorasExtras(**data)
        registro.guardar()
        orden_entry.delete(0, tk.END)
        idnodo_entry.delete(0, tk.END)
        actualizar_tabla()

    def eliminar_registro():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un registro para eliminar.")
            return
        id_registro = tabla.item(seleccion[0])["values"][0]
        HorasExtras.eliminar(id_registro)
        actualizar_tabla()

    # --- Botones ---
    frame_botones = tk.Frame(frame_padre, bg="#E0FFFF")
    frame_botones.pack(pady=10)
    tk.Button(frame_botones, text="Guardar", command=guardar_registro, bg="#4CAF50",
              fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=0, padx=10)
    tk.Button(frame_botones, text="Eliminar", command=eliminar_registro, bg="#f44336",
              fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=10)
    tk.Button(frame_botones, text="Actualizar Lista", command=actualizar_tabla, bg="#2196F3",
              fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=2, padx=10)
    tk.Button(frame_botones, text="Volver al Menú", command=volver_menu, bg="#FFB6C1",
              fg="black", font=("Arial", 10, "bold"), width=15).grid(row=0, column=3, padx=10)

    actualizar_tabla()
