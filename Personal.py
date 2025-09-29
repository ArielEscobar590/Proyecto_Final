class Personal:
    def __init__(self, usuario, contrasena, rol):
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

class Tecnico(Personal):
    def __init__(self, usuario, contrasena):
        super().__init__(usuario, contrasena, "Tecnico")

class Supervisor(Personal):
    def __init__(self, usuario, contrasena):
        super().__init__(usuario, contrasena, "Supervisor")

class Coordinador(Personal):
    def __init__(self, usuario, contrasena):
        super().__init__(usuario, contrasena, "Coordinador")