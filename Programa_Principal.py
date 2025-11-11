import tkinter as tk
from tkinter import messagebox
import sqlite3
import Reportes as r
import Horas_Extra as he
import Vacaciones as v
import Gestion_Personal as gp

class SistemaElectrico:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Gestión - Servicios Eléctricos")
        self.ventana.geometry("1000x700")
        self.ventana.configure(bg="#E0FFFF")


        self.crear_admin_si_no_existe()


        self.frame_principal = tk.Frame(self.ventana, bg="#E0FFFF")
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


        self.mostrar_login()

    def crear_admin_si_no_existe(self):


        try:
            conexion = sqlite3.connect('personal.db')
            cursor = conexion.cursor()


            cursor.execute("""
                CREATE TABLE IF NOT EXISTS personal
                (
                    id_Personal TEXT PRIMARY KEY,
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


            cursor.execute("SELECT * FROM personal WHERE id_Personal = ?", ('01',))
            admin_existente = cursor.fetchone()

            if not admin_existente:

                cursor.execute("""
                    INSERT INTO personal (id_Personal, nombre, apellido, direccion, edad, telefono,
                    correo, fecha_ingreso, vacaciones, rol, contrasena)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, ('01', 'Admin', 'Sistema', 'N/A', 30, '00000000',
                      'admin@sistema.com', '2024-01-01', 15, 'Supervisor', '1234'))
                conexion.commit()
                print("Usuario Admin creado exitosamente")

            conexion.close()
        except Exception as e:
            print(f"Error al crear admin: {e}")

    def mostrar_login(self):

        self.limpiar_frame_principal()


        lbl_titulo = tk.Label(
            self.frame_principal, text="Bienvenid@",
            font=("Arial Rounded MT Bold", 30), bg="#3D2B56", fg="white",
            width=18, pady=10
        )
        lbl_titulo.pack(pady=30)


        frame_login = tk.Frame(self.frame_principal, bg="#B2EBF2", bd=2, relief="solid")
        frame_login.pack(pady=20)

        lbl_bienvenida = tk.Label(
            frame_login, text="Iniciar Sesión", font=("Arial Black", 12), bg="#B2EBF2"
        )
        lbl_bienvenida.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        lbl_instr = tk.Label(
            frame_login,
            text="Ingresa tu ID y Contraseña para continuar",
            bg="#B2EBF2", font=("Arial", 8)
        )
        lbl_instr.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        tk.Label(frame_login, text="ID Personal:", bg="#B2EBF2").grid(row=2, column=0, sticky="w", padx=5)
        self.entry_id = tk.Entry(frame_login, width=30)
        self.entry_id.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        tk.Label(frame_login, text="Contraseña:", bg="#B2EBF2").grid(row=4, column=0, sticky="w", padx=5)
        self.entry_contrasena = tk.Entry(frame_login, show="*", width=30)
        self.entry_contrasena.grid(row=5, column=0, columnspan=2, padx=10, pady=5)


        self.var_mostrar = tk.BooleanVar()
        chk_mostrar = tk.Checkbutton(
            frame_login, text="Mostrar", variable=self.var_mostrar,
            bg="#B2EBF2", command=self.mostrar_contrasena
        )
        chk_mostrar.grid(row=5, column=2, padx=5)


        btn_continuar = tk.Button(
            frame_login, text="Continuar", bg="#1E90FF", fg="white",
            font=("Arial", 9), command=self.verificar_login
        )
        btn_continuar.grid(row=6, column=0, columnspan=3, pady=10)


        self.entry_contrasena.bind('<Return>', lambda event: self.verificar_login())

    def mostrar_contrasena(self):
        if self.var_mostrar.get():
            self.entry_contrasena.config(show="")
        else:
            self.entry_contrasena.config(show="*")

    def verificar_login(self):
        """Verifica las credenciales del usuario"""
        id_personal = self.entry_id.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not id_personal or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor ingrese ID y contraseña")
            return

        try:
            conexion = sqlite3.connect('personal.db')
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT nombre, apellido, rol
                FROM personal
                WHERE id_Personal = ?
                AND contrasena = ?
            """, (id_personal, contrasena))

            usuario = cursor.fetchone()
            conexion.close()

            if usuario:
                nombre, apellido, rol = usuario
                self.usuario_actual = {
                    'id': id_personal,
                    'nombre': nombre,
                    'apellido': apellido,
                    'rol': rol
                }
                messagebox.showinfo("Bienvenido", f"Acceso concedido, {nombre} {apellido}")
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Error", "ID o contraseña incorrectos")

        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar credenciales: {e}")

    def mostrar_menu_principal(self):
        """Muestra el menú principal según el rol del usuario"""
        self.limpiar_frame_principal()

        # Header con información del usuario
        frame_header = tk.Frame(self.frame_principal, bg="#E0FFFF")
        frame_header.pack(fill=tk.X, pady=10)

        tk.Label(frame_header,
                text=f"Bienvenido: {self.usuario_actual['nombre']} {self.usuario_actual['apellido']} - {self.usuario_actual['rol']}",
                font=("Arial", 12, "bold"), bg="#E0FFFF").pack()

        tk.Label(frame_header, text="Sistema de Gestión de Servicios Eléctricos",
                font=("Arial", 10), bg="#E0FFFF").pack()

        frame_botones = tk.Frame(self.frame_principal, bg="#E0FFFF")
        frame_botones.pack(pady=30)

        botones_comunes = [
            ("Agregar Reporte", self.abrir_reportes),
            ("Agregar Reporte Horas Extra", self.abrir_horas_extra)
        ]

        if self.usuario_actual['rol'] in ['Supervisor', 'Coordinador']:
            botones_comunes.append(("Vacaciones", self.abrir_vacaciones))

        for i, (texto, comando) in enumerate(botones_comunes):
            tk.Button(frame_botones, text=texto, command=comando,
                     bg="#B0E0E6", width=25, height=2, font=("Arial", 10)).grid(
                     row=i, column=0, padx=15, pady=10)

        if self.usuario_actual['rol'] in ['Supervisor', 'Coordinador']:
            botones_privilegiados = [
                ("Gestión de Personal", self.abrir_gestion_personal),
                ("Modificar Reportes", self.abrir_modificar_reportes)
            ]

            for i, (texto, comando) in enumerate(botones_privilegiados):
                tk.Button(frame_botones, text=texto, command=comando,
                         bg="#98FB98", width=25, height=2, font=("Arial", 10)).grid(
                         row=i, column=1, padx=15, pady=10)


        tk.Button(self.frame_principal, text="Cerrar Sesión",
                 command=self.mostrar_login, bg="#FFB6C1", width=15).pack(pady=20)

    def abrir_reportes(self):
        self.limpiar_frame_principal()
        r.mostrar_reportes(self.frame_principal, self.mostrar_menu_principal, self.usuario_actual)

    def abrir_horas_extra(self):
        self.limpiar_frame_principal()
        he.mostrar_horas_extra(self.frame_principal, self.mostrar_menu_principal, self.usuario_actual)

    def abrir_vacaciones(self):
        self.limpiar_frame_principal()
        v.mostrar_vacaciones(self.frame_principal, self.mostrar_menu_principal, self.usuario_actual)

    def abrir_gestion_personal(self):
        self.limpiar_frame_principal()
        gp.mostrar_gestion_personal(self.frame_principal, self.mostrar_menu_principal, self.usuario_actual)

    def abrir_modificar_reportes(self):
        self.limpiar_frame_principal()
        r.mostrar_modificar_reportes(self.frame_principal, self.mostrar_menu_principal, self.usuario_actual)


    def limpiar_frame_principal(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = SistemaElectrico()
    app.ejecutar()