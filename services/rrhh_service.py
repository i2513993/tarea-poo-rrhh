from models.trabajador import Gerente, JefeArea, Tecnico, Asistente


def validar_y_crear(nombre, puesto, jefe, exp, nomina):

    if not nombre.strip():
        raise ValueError("El nombre no puede estar vacío.")

    if not all(c.isalpha() or c.isspace() for c in nombre):
        raise ValueError("El nombre solo puede contener letras, sin números ni símbolos.")

    mapa_clases = {
        "Gerente":      Gerente,
        "Jefe de Área": JefeArea,
        "Técnico":      Tecnico,
        "Asistente":    Asistente,
    }
    clase_nueva = mapa_clases[puesto]

    for t in nomina:
        if t.get_nombre().lower() == nombre.strip().lower():
            if isinstance(t, clase_nueva):
                raise ValueError(
                    f'"{nombre}" ya está registrado como {puesto}. '
                    f'No se puede duplicar el mismo cargo.'
                )

    if puesto != "Gerente" and jefe == "Ninguno":
        raise ValueError(f"El puesto '{puesto}' debe tener un jefe inmediato asignado.")

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