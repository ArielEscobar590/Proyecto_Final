import tkinter as tk
import Personal as p
import Inicio_Sesion as i


ventana = tk.Tk()
ventana.title("Reportes")
ventana.geometry("600x400")

bienvenida = tk.Label(ventana, text="-Bienvenido-")
bienvenida.pack(pady=5)
etiquetausu = tk.Label(ventana, text="Escribe el usuario:")
etiquetausu.pack(pady=5)
usu = tk.Entry(ventana)
usu.pack(pady=5)
etiquetacontra = tk.Label(ventana, text="Escriba la contraseña:")
etiquetacontra.pack(pady=5)
contra = tk.Entry(ventana)
contra.pack(pady=5)

i.Inicio()
ventana.mainloop()
