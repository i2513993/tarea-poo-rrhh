from models.trabajador import Gerente, JefeArea, Tecnico, Asistente

def validar_y_crear(nombre, puesto, jefe, exp, nomina):
    # 1. Validar nombre
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")
    
    # 2. Lógica de negocio: Contar subordinados
    subordinados = [t for t in nomina if t.get_jefe() == jefe]
    
    if puesto == "Asistente":
        asistentes = [s for s in subordinados if isinstance(s, Asistente)]
        if len(asistentes) >= 2:
            raise ValueError(f"El jefe {jefe} ya tiene 2 asistentes.")
        return Asistente(nombre, jefe)

    if puesto == "Técnico":
        tecnicos = [s for s in subordinados if isinstance(s, Tecnico)]
        if len(tecnicos) >= 5:
            raise ValueError(f"El jefe {jefe} ya tiene 5 técnicos.")
        return Tecnico(nombre, jefe, exp)

    if puesto == "Gerente":
        return Gerente(nombre)
        
    if puesto == "Jefe de Área":
        return JefeArea(nombre, jefe)