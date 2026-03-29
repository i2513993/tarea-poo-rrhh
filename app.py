import streamlit as st
import pandas as pd
import json
import os
from services.rrhh_service import validar_y_crear
from models.trabajador import Gerente, JefeArea, Tecnico, Asistente

st.title("Instituto Continental  - RRHH")

# Ruta donde se guarda la nómina como archivo
ARCHIVO_NOMINA = "data/nomina.json"

# Creamos la carpeta data si no existe todavía
os.makedirs("data", exist_ok=True)


def objeto_a_dict(trabajador):
    # Convierte un objeto trabajador a un diccionario para poder guardarlo en JSON
    datos = {
        "nombre": trabajador.get_nombre(),
        "jefe":   trabajador.get_jefe_inmediato(),
        "estado": trabajador.get_estado(),
        "tipo":   type(trabajador).__name__  # guardamos el tipo: Gerente, Tecnico, etc.
    }
    # Si es técnico también guardamos su experiencia
    if isinstance(trabajador, Tecnico):
        datos["exp"] = trabajador.get_exp()
    return datos


def dict_a_objeto(datos):
    # Reconstruye el objeto trabajador desde un diccionario guardado en JSON
    tipo   = datos["tipo"]
    nombre = datos["nombre"]
    jefe   = datos["jefe"] if datos["jefe"] != "Ninguno" else None
    estado = datos["estado"]

    if tipo == "Gerente":
        obj = Gerente(nombre)
    elif tipo == "JefeArea":
        obj = JefeArea(nombre, jefe)
    elif tipo == "Tecnico":
        obj = Tecnico(nombre, jefe, datos.get("exp", 0))
    elif tipo == "Asistente":
        obj = Asistente(nombre, jefe)
    else:
        return None

    # Restauramos el estado si el trabajador ya no está activo
    if estado != "Activo":
        obj.set_estado(estado)

    return obj


def cargar_nomina():
    # Lee el archivo JSON y reconstruye la lista de objetos
    if not os.path.exists(ARCHIVO_NOMINA):
        return None  # Si no existe el archivo todavía, devolvemos None
    with open(ARCHIVO_NOMINA, "r", encoding="utf-8") as f:
        lista_dicts = json.load(f)
    return [dict_a_objeto(d) for d in lista_dicts]


def guardar_nomina(nomina):
    # Convierte toda la lista de objetos a diccionarios y la guarda en el archivo
    lista_dicts = [objeto_a_dict(t) for t in nomina]
    with open(ARCHIVO_NOMINA, "w", encoding="utf-8") as f:
        json.dump(lista_dicts, f, ensure_ascii=False, indent=2)


# --- CARGA INICIAL ---
# Si la nómina no está en sesión, intentamos cargarla desde el archivo
if 'nomina' not in st.session_state:
    nomina_guardada = cargar_nomina()

    if nomina_guardada:
        # Si ya había datos guardados, los usamos
        st.session_state.nomina = nomina_guardada
    else:
        # Si es la primera vez, creamos los trabajadores base
        gerente = Gerente("Carlos Mendoza")

        jefe_marketing  = JefeArea("Ana Torres",    "Carlos Mendoza")
        jefe_sistemas   = JefeArea("Luis Quispe",   "Carlos Mendoza")
        jefe_produccion = JefeArea("María Huanca",  "Carlos Mendoza")
        jefe_logistica  = JefeArea("Jorge Paredes", "Carlos Mendoza")
        jefe_finanzas   = JefeArea("Rosa Cáceres",  "Carlos Mendoza")

        asist_mkt_1 = Asistente("Valeria Ramos",  "Ana Torres")
        asist_mkt_2 = Asistente("Diego Flores",   "Ana Torres")
        asist_sis_1 = Asistente("Camila Vargas",  "Luis Quispe")
        asist_pro_1 = Asistente("Sofía Mamani",   "María Huanca")
        asist_pro_2 = Asistente("Pedro Coyla",    "María Huanca")

        tec_sis_1 = Tecnico("Rodrigo Apaza",  "Luis Quispe",   3)
        tec_sis_2 = Tecnico("Fabiola Cruz",   "Luis Quispe",   5)
        tec_sis_3 = Tecnico("Marcos Chávez",  "Luis Quispe",   2)
        tec_pro_1 = Tecnico("Elena Condori",  "María Huanca",  4)
        tec_pro_2 = Tecnico("Iván Lupaca",    "María Huanca",  1)
        tec_pro_3 = Tecnico("Natalia Soto",   "María Huanca",  6)
        tec_pro_4 = Tecnico("Oscar Pilco",    "María Huanca",  2)
        tec_log_1 = Tecnico("Patricia Lira",  "Jorge Paredes", 3)
        tec_log_2 = Tecnico("Sergio Mamani",  "Jorge Paredes", 7)
        tec_log_3 = Tecnico("Carla Bustinza", "Jorge Paredes", 2)

        st.session_state.nomina = [
            gerente,
            jefe_marketing, jefe_sistemas, jefe_produccion, jefe_logistica, jefe_finanzas,
            asist_mkt_1, asist_mkt_2, asist_sis_1, asist_pro_1, asist_pro_2,
            tec_sis_1, tec_sis_2, tec_sis_3,
            tec_pro_1, tec_pro_2, tec_pro_3, tec_pro_4,
            tec_log_1, tec_log_2, tec_log_3,
        ]

        # Guardamos los datos iniciales en el archivo por primera vez
        guardar_nomina(st.session_state.nomina)


# --- FORMULARIO ---
st.write("### Registrar Nuevo Trabajador")
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre Completo")
    puesto = st.selectbox("Puesto", ["Gerente", "Jefe de Área", "Asistente", "Técnico"])

with col2:
    nombres_jefes = [t.get_nombre() for t in st.session_state.nomina]

    if puesto == "Gerente":
        jefe = "Ninguno"
        st.selectbox("Jefe Inmediato", ["Ninguno"], disabled=True)
    else:
        jefe = st.selectbox("Jefe Inmediato", nombres_jefes if nombres_jefes else ["Sin trabajadores aún"])

    exp = st.number_input("Años de Experiencia (solo Técnicos)", min_value=0)

if st.button("Registrar en Nómina"):
    try:
        nuevo = validar_y_crear(nombre, puesto, jefe, exp, st.session_state.nomina)
        st.session_state.nomina.append(nuevo)
        # Guardamos cada vez que se agrega alguien nuevo
        guardar_nomina(st.session_state.nomina)
        st.success(f"¡{puesto} registrado con éxito!")
    except Exception as e:
        st.error(f"Error: {e}")


# --- TABLA ---
st.write("### 📊 Nómina Actual (Array de Objetos)")

tabla_data = []
for trabajador in st.session_state.nomina:
    tabla_data.append({
        "Nombre":           trabajador.get_nombre(),
        "Puesto / Resumen": trabajador.get_resumen(),
        "Jefe Inmediato":   trabajador.get_jefe_inmediato(),
        "Estado":           trabajador.get_estado()
    })

df = pd.DataFrame(tabla_data)
st.dataframe(df, use_container_width=True)