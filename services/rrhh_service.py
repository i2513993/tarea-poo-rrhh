from models.trabajador import Gerente, JefeArea, Tecnico, Asistente


def validar_y_crear(nombre, puesto, jefe, exp, nomina):

    # Validar que el nombre no esté vacío
    if not nombre.strip():
        raise ValueError("El nombre no puede estar vacío.")

    # Validar que el nombre solo tenga letras y espacios, sin números ni símbolos
    if not all(c.isalpha() or c.isspace() for c in nombre):
        raise ValueError("El nombre solo puede contener letras, sin números ni símbolos.")

    # Validar que solo el Gerente puede no tener jefe
    # Todos los demás puestos DEBEN seleccionar un jefe inmediato
    if puesto != "Gerente" and jefe == "Ninguno":
        raise ValueError(f"El puesto '{puesto}' debe tener un jefe inmediato asignado.")

    # Contamos cuántos subordinados directos ya tiene ese jefe
    subordinados = [t for t in nomina if t.get_jefe_inmediato() == jefe]

    if puesto == "Gerente":
        return Gerente(nombre)

    if puesto == "Jefe de Área":
        return JefeArea(nombre, jefe)

    if puesto == "Asistente":
        asistentes_actuales = [s for s in subordinados if isinstance(s, Asistente)]
        if len(asistentes_actuales) >= 2:
            raise ValueError(f"{jefe} ya tiene 2 asistentes. No se puede agregar más.")
        return Asistente(nombre, jefe)

    if puesto == "Técnico":
        tecnicos_actuales = [s for s in subordinados if isinstance(s, Tecnico)]
        if len(tecnicos_actuales) >= 5:
            raise ValueError(f"{jefe} ya tiene 5 técnicos. No se puede agregar más.")
        return Tecnico(nombre, jefe, exp)