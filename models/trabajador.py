class Trabajador:
    def __init__(self, nombre, jefe=None, estado="Activo"):
        self.__nombre = nombre
        self.__jefe = jefe
        self.__estado = estado

    def get_nombre(self): return self.__nombre
    def get_jefe(self): return self.__jefe if self.__jefe else "Ninguno"
    def get_estado(self): return self.__estado
    def get_resumen(self): return f"Trabajador: {self.__nombre}"

class Gerente(Trabajador):
    def get_resumen(self): return "Puesto: Gerente"

class JefeArea(Trabajador):
    def __init__(self, nombre, jefe):
        super().__init__(nombre, jefe)
    def get_resumen(self): return "Puesto: Jefe de Área"

class Tecnico(Trabajador):
    def __init__(self, nombre, jefe, exp):
        super().__init__(nombre, jefe)
        self.__exp = exp
    def get_resumen(self): return f"Puesto: Técnico (Exp: {self.__exp} años)"

class Asistente(Trabajador):
    def get_resumen(self): return "Puesto: Asistente"