class Inicio:
    def __init__(self, ventana):
        self.ventana = ventana

def Cargar_Usuarios():
    pass

def Guardar_Usuarios():
    pass

def Eliminar_Usuarios():
    pass

def Modificar_Usuarios():
    pass

def Inicio():
    import tkinter as tk
    from tkinter import messagebox


    ventana = tk.Tk()
    ventana.title("Inicio de Sesión")
    ventana.geometry("900x630")
    ventana.configure(bg="#E0FFFF")



    def mostrar_contrasena():
        if var_mostrar.get():
            entry_contrasena.config(show="")
        else:
            entry_contrasena.config(show="*")

    def iniciar_sesion():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        if usuario == "admin" and contrasena == "1234":
            messagebox.showinfo("Bienvenido", f"Acceso concedido, {usuario}")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def cambiar_modo():
        global modo_oscuro
        if not modo_oscuro:
            ventana.configure(bg="#1C1C1C")
            frame_login.configure(bg="#333333")
            lbl_titulo.configure(bg="#3D2B56", fg="white")
            lbl_bienvenida.configure(bg="#1C1C1C", fg="white")
            lbl_instr.configure(bg="#333333", fg="#DDDDDD")
            lbl_usuario.configure(bg="#333333", fg="#DDDDDD")
            lbl_contrasena.configure(bg="#333333", fg="#DDDDDD")
            btn_continuar.configure(bg="#0052CC", fg="white")
            btn_modo.configure(text="Cambiar a Modo Claro", bg="white", fg="black")
            modo_oscuro = True
        else:
            ventana.configure(bg="#E0FFFF")
            frame_login.configure(bg="#B2EBF2")
            lbl_titulo.configure(bg="#3D2B56", fg="white")
            lbl_bienvenida.configure(bg="#E0FFFF", fg="black")
            lbl_instr.configure(bg="#B2EBF2", fg="black")
            lbl_usuario.configure(bg="#B2EBF2", fg="black")
            lbl_contrasena.configure(bg="#B2EBF2", fg="black")
            btn_continuar.configure(bg="#1E90FF", fg="white")
            btn_modo.configure(text="Cambiar a Modo Oscuro", bg="black", fg="white")
            modo_oscuro = False


    lbl_titulo = tk.Label(ventana, text="Bienvenid@", font=("Arial Rounded MT Bold", 30),
                          bg="#3D2B56", fg="white", width=18, pady=10)
    lbl_titulo.pack(pady=30)


    frame_login = tk.Frame(ventana, bg="#B2EBF2", bd=2, relief="solid")
    frame_login.pack(pady=20)

    lbl_bienvenida = tk.Label(frame_login, text="Iniciar Sesión", font=("Arial Black", 12), bg="#B2EBF2")
    lbl_bienvenida.grid(row=0, column=0, columnspan=2, pady=(10, 0))

    lbl_instr = tk.Label(frame_login, text="Ingresa tu Usuario y Contraseña para continuar",
                         bg="#B2EBF2", font=("Arial", 8))
    lbl_instr.grid(row=1, column=0, columnspan=2, pady=(0, 10))

    lbl_usuario = tk.Label(frame_login, text="Usuario", bg="#B2EBF2")
    lbl_usuario.grid(row=2, column=0, sticky="w", padx=5)
    entry_usuario = tk.Entry(frame_login, width=30)
    entry_usuario.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    lbl_contrasena = tk.Label(frame_login, text="Contraseña", bg="#B2EBF2")
    lbl_contrasena.grid(row=4, column=0, sticky="w", padx=5)
    entry_contrasena = tk.Entry(frame_login, show="*", width=30)
    entry_contrasena.grid(row=5, column=0, columnspan=2, padx=10, pady=5)


    var_mostrar = tk.BooleanVar()
    chk_mostrar = tk.Checkbutton(frame_login, text="Mostrar", variable=var_mostrar,
                                 bg="#B2EBF2", command=mostrar_contrasena)
    chk_mostrar.grid(row=5, column=2, padx=5)


    btn_continuar = tk.Button(frame_login, text="Continuar", bg="#1E90FF", fg="white",
                              font=("Arial", 9), command=iniciar_sesion)
    btn_continuar.grid(row=6, column=0, columnspan=3, pady=10)


    modo_oscuro = False
    btn_modo = tk.Button(ventana, text="Cambiar a Modo Oscuro", bg="black", fg="white",
                         command=cambiar_modo, width=25)
    btn_modo.pack(side="bottom", pady=20)

    ventana.mainloop()
