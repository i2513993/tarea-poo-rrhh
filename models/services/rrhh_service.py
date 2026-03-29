from models.trabajador import Gerente, JefeArea, Tecnico, Asistente

def validar_y_crear(nombre, puesto, jefe, exp, nomina):
    # Validación básica
    if nombre == "": 
        raise ValueError("El nombre es obligatorio")
    
    # Filtrar subordinados para aplicar reglas de negocio
    subordinados = [t for t in nomina if t.get_jefe() == jefe]
    asistentes = [s for s in subordinados if isinstance(s, Asistente)]
    tecnicos = [s for s in subordinados if isinstance(s, Tecnico)]

    # Reglas de la historia de usuario
    if puesto == "Asistente" and len(asistentes) >= 2:
        raise ValueError(f"El jefe {jefe} ya tiene el máximo de 2 asistentes.")
    
    if puesto == "Técnico" and len(tecnicos) >= 5:
        raise ValueError(f"El jefe {jefe} ya tiene el máximo de 5 técnicos.")

    # Instanciación según el puesto (POO)
    if puesto == "Gerente": 
        return Gerente(nombre)
    elif puesto == "Jefe de Área": 
        return JefeArea(nombre, jefe)
    elif puesto == "Asistente": 
        return Asistente(nombre, jefe)
    elif puesto == "Técnico": 
        return Tecnico(nombre, jefe, exp)