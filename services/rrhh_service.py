# Este archivo contiene las reglas de negocio antes de crear un trabajador
# Aquí validamos que todo esté correcto antes de agregarlo a la nómina

from models.trabajador import Gerente, JefeArea, Tecnico, Asistente


def validar_y_crear(nombre, puesto, jefe, exp, nomina):

    # Regla 1: el nombre no puede estar vacío
    if not nombre.strip():
        raise ValueError("El nombre no puede estar vacío.")

    # Contamos cuántos subordinados directos ya tiene ese jefe en la nómina
    subordinados = [t for t in nomina if t.get_jefe_inmediato() == jefe]

    # --- Creación según el puesto elegido ---

    if puesto == "Gerente":
        # El gerente no tiene jefe, se crea directamente
        return Gerente(nombre)

    if puesto == "Jefe de Área":
        # El jefe de área reporta al gerente
        return JefeArea(nombre, jefe)

    if puesto == "Asistente":
        # Contamos cuántos asistentes ya tiene ese jefe
        asistentes_actuales = [s for s in subordinados if isinstance(s, Asistente)]
        # Regla: un jefe no puede tener más de 2 asistentes
        if len(asistentes_actuales) >= 2:
            raise ValueError(f"{jefe} ya tiene 2 asistentes. No se puede agregar más.")
        return Asistente(nombre, jefe)

    if puesto == "Técnico":
        # Contamos cuántos técnicos ya tiene ese jefe
        tecnicos_actuales = [s for s in subordinados if isinstance(s, Tecnico)]
        # Regla: un jefe no puede tener más de 5 técnicos
        if len(tecnicos_actuales) >= 5:
            raise ValueError(f"{jefe} ya tiene 5 técnicos. No se puede agregar más.")
        return Tecnico(nombre, jefe, exp)