from models.trabajador import Gerente, JefeArea, Tecnico, Asistente

def obtener_nomina():
    # 1. Creamos al Gerente
    gerente = Gerente("Ing. Alberto Castro")

    # 2. Creamos 5 Jefes de Área
    jefes = [
        JefeArea("Ana Luna", "Marketing", gerente.get_nombre()),
        JefeArea("Luis Torres", "Sistemas", gerente.get_nombre()),
        JefeArea("Marta Rivas", "Producción", gerente.get_nombre()),
        JefeArea("Pedro Sánchez", "Logística", gerente.get_nombre()),
        JefeArea("Sofía Vega", "RRHH", gerente.get_nombre())
    ]

    # 3. Creamos Asistentes (ejemplo para Sistemas y Marketing)
    asistentes = [
        Asistente("Juan Pérez", "Luis Torres"),
        Asistente("María Jara", "Luis Torres"),
        Asistente("Katy Soto", "Ana Luna")
    ]

    # 4. Creamos Técnicos (ejemplo 5 técnicos)
    tecnicos = [
        Tecnico("Roberto Gómez", "Luis Torres", 5),
        Tecnico("Lucía Fernández", "Marta Rivas", 3),
        Tecnico("Kevin Arrieta", "Pedro Sánchez", 10),
        Tecnico("Julia Quispe", "Luis Torres", 2),
        Tecnico("Marcos Paz", "Marta Rivas", 4)
    ]

    # Retornamos el Array de Objetos completo
    return [gerente] + jefes + asistentes + tecnicos