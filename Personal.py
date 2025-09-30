import Vacaciones as v
import Reportes as r
import Horas_Extra as h

class Personal:
    def __init__(self, usuario, contrasena, rol):
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    def Mostrar_Personal(self):
        pass

    def Cargar_Personal(self):
        pass

    def Eliminar_Personal(self):
        pass

    def Modificar_Personal(self):
        pass

    def Guardar_Personal(self):
        pass

class Tecnico(Personal):
    def __init__(self, usuario, contrasena):
        super().__init__(usuario, contrasena, "Tecnico")

class Supervisor(Personal):
    def __init__(self, usuario, contrasena):
        super().__init__(usuario, contrasena, "Supervisor")

class Coordinador(Personal):
    def __init__(self, usuario, contrasena):
        super().__init__(usuario, contrasena, "Coordinador")

