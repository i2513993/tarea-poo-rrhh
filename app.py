# Archivo principal de la aplicación
# Aquí se construye toda la pantalla que ve el usuario

import streamlit as st
import pandas as pd
from services.rrhh_service import validar_y_crear
from models.trabajador import Gerente, JefeArea, Tecnico, Asistente

st.title("🏢 Business Corporation - RRHH")

# --- DATOS INICIALES ---
# Si la nómina todavía no existe en la sesión, la creamos con los trabajadores base
# Esto cumple el requisito del docente: 1 gerente, 5 jefes, asistentes y técnicos

if 'nomina' not in st.session_state:

    # Creamos al gerente general (no tiene jefe)
    gerente = Gerente("Carlos Mendoza")

    # Creamos los 5 jefes de área (todos reportan al gerente)
    jefe_marketing   = JefeArea("Ana Torres",    "Carlos Mendoza")
    jefe_sistemas    = JefeArea("Luis Quispe",   "Carlos Mendoza")
    jefe_produccion  = JefeArea("María Huanca",  "Carlos Mendoza")
    jefe_logistica   = JefeArea("Jorge Paredes", "Carlos Mendoza")
    jefe_finanzas    = JefeArea("Rosa Cáceres",  "Carlos Mendoza")

    # Asistentes de Marketing (máximo 2 por área)
    asist_mkt_1 = Asistente("Valeria Ramos",  "Ana Torres")
    asist_mkt_2 = Asistente("Diego Flores",   "Ana Torres")

    # Asistentes de Sistemas
    asist_sis_1 = Asistente("Camila Vargas",  "Luis Quispe")

    # Asistentes de Producción
    asist_pro_1 = Asistente("Sofía Mamani",   "María Huanca")
    asist_pro_2 = Asistente("Pedro Coyla",    "María Huanca")

    # Técnicos de Sistemas (entre 3 y 5 por área)
    tec_sis_1 = Tecnico("Rodrigo Apaza",   "Luis Quispe", 3)
    tec_sis_2 = Tecnico("Fabiola Cruz",    "Luis Quispe", 5)
    tec_sis_3 = Tecnico("Marcos Chávez",   "Luis Quispe", 2)

    # Técnicos de Producción
    tec_pro_1 = Tecnico("Elena Condori",   "María Huanca", 4)
    tec_pro_2 = Tecnico("Iván Lupaca",     "María Huanca", 1)
    tec_pro_3 = Tecnico("Natalia Soto",    "María Huanca", 6)
    tec_pro_4 = Tecnico("Oscar Pilco",     "María Huanca", 2)

    # Técnicos de Logística
    tec_log_1 = Tecnico("Patricia Lira",   "Jorge Paredes", 3)
    tec_log_2 = Tecnico("Sergio Mamani",   "Jorge Paredes", 7)
    tec_log_3 = Tecnico("Carla Bustinza",  "Jorge Paredes", 2)

    # Guardamos todos los trabajadores en la nómina (lista de objetos)
    st.session_state.nomina = [
        gerente,
        jefe_marketing, jefe_sistemas, jefe_produccion, jefe_logistica, jefe_finanzas,
        asist_mkt_1, asist_mkt_2, asist_sis_1, asist_pro_1, asist_pro_2,
        tec_sis_1, tec_sis_2, tec_sis_3,
        tec_pro_1, tec_pro_2, tec_pro_3, tec_pro_4,
        tec_log_1, tec_log_2, tec_log_3,
    ]

# --- FORMULARIO PARA REGISTRAR UN NUEVO TRABAJADOR ---
st.write("### Registrar Nuevo Trabajador")
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre Completo")
    puesto = st.selectbox("Puesto", ["Gerente", "Jefe de Área", "Asistente", "Técnico"])

with col2:
    # Llenamos la lista de posibles jefes con los nombres de quienes ya están en la nómina
    nombres_jefes = [t.get_nombre() for t in st.session_state.nomina]
    jefe = st.selectbox("Jefe Inmediato", ["Ninguno"] + nombres_jefes)
    exp  = st.number_input("Años de Experiencia (solo Técnicos)", min_value=0)

# Cuando el usuario hace clic en el botón, intentamos crear el trabajador
if st.button("Registrar en Nómina"):
    try:
        nuevo = validar_y_crear(nombre, puesto, jefe, exp, st.session_state.nomina)
        st.session_state.nomina.append(nuevo)
        st.success(f"¡{puesto} registrado con éxito!")
    except Exception as e:
        st.error(f"Error: {e}")

# --- TABLA DE LA NÓMINA COMPLETA ---
# Recorremos la lista de objetos y extraemos los datos de cada uno para mostrarlos
st.write("### 📊 Nómina Actual (Array de Objetos)")

tabla_data = []
for trabajador in st.session_state.nomina:
    # Llamamos a los métodos getter de cada objeto para obtener su información
    tabla_data.append({
        "Nombre":          trabajador.get_nombre(),
        "Puesto / Resumen": trabajador.get_resumen(),
        "Jefe Inmediato":  trabajador.get_jefe_inmediato(),   # nombre corregido
        "Estado":          trabajador.get_estado()
    })

# Convertimos la lista de diccionarios a una tabla que Streamlit puede mostrar
df = pd.DataFrame(tabla_data)
st.dataframe(df, use_container_width=True)