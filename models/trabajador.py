# Este archivo define las "plantillas" (clases) para cada tipo de trabajador
# Cada trabajador tiene nombre, jefe y estado (si está activo o ya no trabaja aquí)

# Clase base: todos los trabajadores comparten estas características
class Trabajador:
    def __init__(self, nombre, jefe=None, estado="Activo"):
        # Guardamos los datos con doble guión bajo para que sean privados
        # (privado = nadie puede cambiarlos directamente desde afuera)
        self.__nombre = nombre
        self.__jefe = jefe
        self.__estado = estado  # Por defecto el trabajador está "Activo"

    # --- GETTERS: métodos para leer los datos privados ---

    def get_nombre(self):
        # Devuelve el nombre del trabajador
        return self.__nombre

    def get_jefe_inmediato(self):
        # Devuelve el nombre del jefe, o "Ninguno" si es el jefe máximo
        return self.__jefe if self.__jefe else "Ninguno"

    def get_estado(self):
        # Devuelve el estado actual del trabajador:
        # "Activo" = sigue en la empresa
        # "TC"     = Término de contrato
        # "D"      = Despido
        # "R"      = Renuncia
        return self.__estado

    def get_resumen(self):
        # Cada subclase sobreescribe este método con su propio resumen
        return f"Trabajador: {self.__nombre}"

    # --- SETTERS: métodos para modificar los datos privados ---

    def set_nombre(self, nuevo_nombre):
        # Permite cambiar el nombre del trabajador
        self.__nombre = nuevo_nombre

    def set_jefe_inmediato(self, nuevo_jefe):
        # Permite cambiar quién es el jefe del trabajador
        self.__jefe = nuevo_jefe

    def set_estado(self, nuevo_estado):
        # Permite actualizar el estado cuando el trabajador se va de la empresa
        # Solo acepta valores válidos para evitar errores
        estados_validos = ["Activo", "TC", "D", "R"]
        if nuevo_estado in estados_validos:
            self.__estado = nuevo_estado
        else:
            raise ValueError(f"Estado inválido. Usa uno de estos: {estados_validos}")


# --- Subclases: cada puesto hereda de Trabajador y personaliza su resumen ---

class Gerente(Trabajador):
    # El Gerente no tiene jefe, así que no necesita ese dato
    def __init__(self, nombre):
        super().__init__(nombre)  # Llama al constructor de Trabajador sin jefe

    def get_resumen(self):
        return "Gerente General"


class JefeArea(Trabajador):
    # El Jefe de Área sí tiene jefe (el Gerente)
    def __init__(self, nombre, jefe):
        super().__init__(nombre, jefe)

    def get_resumen(self):
        return "Jefe de Área"


class Tecnico(Trabajador):
    # El Técnico tiene jefe y además guardamos sus años de experiencia
    def __init__(self, nombre, jefe, exp):
        super().__init__(nombre, jefe)
        self.__exp = exp  # Años de experiencia, dato exclusivo del Técnico

    def get_resumen(self):
        # El resumen del técnico incluye sus años de experiencia
        return f"Técnico  |  Experiencia: {self.__exp} años"

    def get_exp(self):
        return self.__exp

    def set_exp(self, nueva_exp):
        # Permite actualizar los años de experiencia
        self.__exp = nueva_exp


class Asistente(Trabajador):
    # El Asistente tiene jefe pero no tiene dato extra como el Técnico
    def __init__(self, nombre, jefe):
        super().__init__(nombre, jefe)

    def get_resumen(self):
        return "Asistente"