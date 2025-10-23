from tkinter import messagebox
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

fallas = ["fusible quemado", "cable dañado", "conector con zarro", "movimiento de poste", "nodo inhibido", "problema de energía comercial"]
DB_NAME = "reporte.db"


class Reporte_falla:
    def __init__(self, fecha, orden, hora_inicio, hora_fin, solucion, tecnico):
        self.fecha = fecha
        self.orden = orden
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solucion = solucion
        self.tecnico = tecnico

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Reporte_Falla(
                num_falla INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                orden TEXT NOT NULL,
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
                "INSERT INTO Reporte_Falla (fecha, orden, inicio, fin, solucion, tecnico) VALUES (?, ?, ?, ?, ?, ?)",
                (self.fecha, self.orden, self.hora_inicio, self.hora_fin, self.solucion, self.tecnico)
            )
        messagebox.showinfo("Éxito", f"Reporte '{self.orden}' guardado con éxito.")

    @staticmethod
    def listar():
        with Reporte_falla._conn() as conn:
            cur = conn.execute("SELECT * FROM Reporte_Falla")
            return cur.fetchall()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Reportes de Falla")
        self.root.geometry("900x650")

        frame = tk.LabelFrame(root, text="Nuevo Reporte", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)


        tk.Label(frame, text="Fecha:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        fechas = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
        self.fecha_cb = ttk.Combobox(frame, values=fechas, state="readonly", width=37)
        self.fecha_cb.set(fechas[0])
        self.fecha_cb.grid(row=0, column=1, padx=5, pady=5)

        # --- Campo de orden ---
        tk.Label(frame, text="Orden:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.orden_entry = tk.Entry(frame, width=40)
        self.orden_entry.grid(row=1, column=1, padx=5, pady=5)


        tk.Label(frame, text="Hora Inicio:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        horas = [f"{h:02d}:00" for h in range(7, 20)]  # 7:00 a 19:00
        self.hora_inicio_cb = ttk.Combobox(frame, values=horas, state="readonly", width=37)
        self.hora_inicio_cb.set("08:00")
        self.hora_inicio_cb.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Hora Fin:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.hora_fin_cb = ttk.Combobox(frame, values=horas, state="readonly", width=37)
        self.hora_fin_cb.set("17:00")
        self.hora_fin_cb.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Solución:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.solucion_entry = ttk.Combobox(frame, values=fallas, state="readonly", width=37)
        self.solucion_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Técnico:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        tecnicos = ["Carlos Pérez", "Ana Gómez", "Luis Hernández", "Marta López", "Otro"]
        self.tecnico_cb = ttk.Combobox(frame, values=tecnicos, state="readonly", width=37)
        self.tecnico_cb.set(tecnicos[0])
        self.tecnico_cb.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Guardar Reporte",
            command=self.guardar_reporte,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        ).grid(row=6, column=0, columnspan=2, pady=10)


        tk.Button(
            frame,
            text="Mostrar Reportes",
            command=self.mostrar_reportes,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold")
        ).grid(row=7, column=0, columnspan=2, pady=5)


        tk.Button(
            frame,
            text="Salir",
            command=self.root.destroy,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold")
        ).grid(row=8, column=0, columnspan=2, pady=5)


        self.tabla = None

    def guardar_reporte(self):
        data = {
            "fecha": self.fecha_cb.get(),
            "orden": self.orden_entry.get(),
            "hora_inicio": self.hora_inicio_cb.get(),
            "hora_fin": self.hora_fin_cb.get(),
            "solucion": self.solucion_entry.get(),
            "tecnico": self.tecnico_cb.get()
        }

        if any(not v for v in data.values()):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        rep = Reporte_falla(**data)
        rep.guardar()

        self.orden_entry.delete(0, tk.END)
        self.solucion_entry.set('')

    def mostrar_reportes(self):
        """Muestra la tabla solo cuando el usuario hace clic en 'Mostrar Reportes'."""
        if self.tabla:
            # Si ya existe, actualizarla
            self.actualizar_tabla()
            return


        self.tabla = ttk.Treeview(
            self.root,
            columns=("fecha", "orden", "inicio", "fin", "solucion", "tecnico"),
            show="headings"
        )
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.actualizar_tabla()

    def actualizar_tabla(self):

        for row in self.tabla.get_children():
            self.tabla.delete(row)


        for fila in Reporte_falla.listar():
            self.tabla.insert("", tk.END, values=(
                fila["fecha"], fila["orden"], fila["inicio"], fila["fin"], fila["solucion"], fila["tecnico"]
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()