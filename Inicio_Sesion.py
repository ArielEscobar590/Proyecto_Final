import tkinter as tk
from tkinter import messagebox


class Inicio:
    def __init__(self, ventana):
        self.ventana = ventana
        self.modo_oscuro = False  # Estado inicial del modo

        self.configurar_interfaz()

    def configurar_interfaz(self):
        self.ventana.title("Inicio de Sesión")
        self.ventana.geometry("1200x750")
        self.ventana.configure(bg="#E0FFFF")

        # Título
        self.lbl_titulo = tk.Label(
            self.ventana, text="Bienvenid@", font=("Arial Rounded MT Bold", 30),
            bg="#3D2B56", fg="white", width=18, pady=10
        )
        self.lbl_titulo.pack(pady=30)

        # Frame principal
        self.frame_login = tk.Frame(self.ventana, bg="#B2EBF2", bd=2, relief="solid")
        self.frame_login.pack(pady=20)

        self.lbl_bienvenida = tk.Label(
            self.frame_login, text="Iniciar Sesión", font=("Arial Black", 12), bg="#B2EBF2"
        )
        self.lbl_bienvenida.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        self.lbl_instr = tk.Label(
            self.frame_login,
            text="Ingresa tu Usuario y Contraseña para continuar",
            bg="#B2EBF2", font=("Arial", 8)
        )
        self.lbl_instr.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        self.lbl_usuario = tk.Label(self.frame_login, text="Usuario", bg="#B2EBF2")
        self.lbl_usuario.grid(row=2, column=0, sticky="w", padx=5)
        self.entry_usuario = tk.Entry(self.frame_login, width=30)
        self.entry_usuario.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.lbl_contrasena = tk.Label(self.frame_login, text="Contraseña", bg="#B2EBF2")
        self.lbl_contrasena.grid(row=4, column=0, sticky="w", padx=5)
        self.entry_contrasena = tk.Entry(self.frame_login, show="*", width=30)
        self.entry_contrasena.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.var_mostrar = tk.BooleanVar()
        self.chk_mostrar = tk.Checkbutton(
            self.frame_login, text="Mostrar", variable=self.var_mostrar,
            bg="#B2EBF2", command=self.mostrar_contrasena
        )
        self.chk_mostrar.grid(row=5, column=2, padx=5)

        self.btn_continuar = tk.Button(
            self.frame_login, text="Continuar", bg="#1E90FF", fg="white",
            font=("Arial", 9), command=self.iniciar_sesion
        )
        self.btn_continuar.grid(row=6, column=0, columnspan=3, pady=10)

        # Botón modo oscuro
        self.btn_modo = tk.Button(
            self.ventana, text="Cambiar a Modo Oscuro", bg="black", fg="white",
            command=self.cambiar_modo, width=25
        )
        self.btn_modo.pack(side="bottom", pady=20)

    def mostrar_contrasena(self):
        if self.var_mostrar.get():
            self.entry_contrasena.config(show="")
        else:
            self.entry_contrasena.config(show="*")

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if usuario == "admin" and contrasena == "1234":
            messagebox.showinfo("Bienvenido", f"Acceso concedido, {usuario}")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def cambiar_modo(self):
        """Activa o desactiva el modo oscuro."""
        if not self.modo_oscuro:
            # Cambiar a modo oscuro
            self.ventana.configure(bg="#1C1C1C")
            self.frame_login.configure(bg="#333333")
            self.lbl_titulo.configure(bg="#3D2B56", fg="white")
            self.lbl_bienvenida.configure(bg="#333333", fg="white")
            self.lbl_instr.configure(bg="#333333", fg="#DDDDDD")
            self.lbl_usuario.configure(bg="#333333", fg="#DDDDDD")
            self.lbl_contrasena.configure(bg="#333333", fg="#DDDDDD")
            self.chk_mostrar.configure(bg="#333333", fg="#DDDDDD", selectcolor="#333333")
            self.btn_continuar.configure(bg="#0052CC", fg="white")
            self.btn_modo.configure(text="Cambiar a Modo Claro", bg="white", fg="black")

            self.modo_oscuro = True
        else:
            # Cambiar a modo claro
            self.ventana.configure(bg="#E0FFFF")
            self.frame_login.configure(bg="#B2EBF2")
            self.lbl_titulo.configure(bg="#3D2B56", fg="white")
            self.lbl_bienvenida.configure(bg="#B2EBF2", fg="black")
            self.lbl_instr.configure(bg="#B2EBF2", fg="black")
            self.lbl_usuario.configure(bg="#B2EBF2", fg="black")
            self.lbl_contrasena.configure(bg="#B2EBF2", fg="black")
            self.chk_mostrar.configure(bg="#B2EBF2", fg="black", selectcolor="#B2EBF2")
            self.btn_continuar.configure(bg="#1E90FF", fg="white")
            self.btn_modo.configure(text="Cambiar a Modo Oscuro", bg="black", fg="white")

            self.modo_oscuro = False


# Función principal
def InicioApp():
    ventana = tk.Tk()
    app = Inicio(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    InicioApp()
