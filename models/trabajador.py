class Trabajador:
    def __init__(self, nombre_completo, jefe_inmediato=None, estado="Activo"):
        self.__nombre_completo = nombre_completo
        self.__jefe_inmediato = jefe_inmediato
        self.__estado = estado  # Activo, TC, D, R

    # Getters y Setters obligatorios por la tarea
    def get_nombre(self): return self.__nombre_completo
    def set_nombre(self, valor): self.__nombre_completo = valor

    def get_jefe_inmediato(self):
        return self.__jefe_inmediato if self.__jefe_inmediato else "No tiene jefe (Gerencia)"

    def get_estado(self):
        mapa = {"TC": "Término de contrato (TC)", "D": "Despido (D)", "R": "Renuncia (R)"}
        return mapa.get(self.__estado, "Activo")
    
    def set_estado(self, valor): self.__estado = valor

    def get_resumen(self):
        return f"Empleado: {self.__nombre_completo} | Jefe: {self.get_jefe_inmediato()}"

# Herencia para los puestos
class Gerente(Trabajador):
    def get_resumen(self):
        return f"Puesto: Gerente | Rango: Alta Dirección | {self.get_nombre()}"

class JefeArea(Trabajador):
    def __init__(self, nombre, area, jefe):
        super().__init__(nombre, jefe)
        self.__area = area
    def get_resumen(self):
        return f"Puesto: Jefe de Área ({self.__area}) | {self.get_nombre()}"

class Tecnico(Trabajador):
    def __init__(self, nombre, jefe, exp_anios):
        super().__init__(nombre, jefe)
        self.__exp = exp_anios
    def get_resumen(self):
        return f"Puesto: Personal Técnico | Rango: Operativo | Exp: {self.__exp} años | {self.get_nombre()}"

class Asistente(Trabajador):
    def get_resumen(self):
        return f"Puesto: Asistente | Rango: Soporte | {self.get_nombre()}"