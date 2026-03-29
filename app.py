import streamlit as st
import pandas as pd
from services.rrhh_service import validar_y_crear

st.title("🏢 Business Corporation - RRHH")

# Inicializar la nómina (Array de Objetos) en la sesión
if 'nomina' not in st.session_state:
    st.session_state.nomina = []

# --- FORMULARIO DE ENTRADA ---
st.write("### Registro de Nuevo Trabajador")
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre Completo")
    puesto = st.selectbox("Puesto", ["Gerente", "Jefe de Área", "Asistente", "Técnico"])

with col2:
    # Obtener lista de posibles jefes actuales para el selectbox
    nombres_jefes = [t.get_nombre() for t in st.session_state.nomina]
    jefe = st.selectbox("Jefe Inmediato", ["Ninguno"] + nombres_jefes)
    exp = st.number_input("Años de Experiencia (Solo Técnicos)", min_value=0)

# --- BOTÓN DE ACCIÓN ---
if st.button("Registrar en Nómina"):
    try:
        nuevo_t = validar_y_crear(nombre, puesto, jefe, exp, st.session_state.nomina)
        st.session_state.nomina.append(nuevo_t)
        st.success(f"¡{puesto} registrado con éxito!")
    except Exception as e:
        st.error(f"Error: {e}")

# --- TABLA DE RESULTADOS ---
if st.session_state.nomina:
    st.write("### 📊 Array de Objetos (Nómina Actual)")
    
    # Transformamos la lista de objetos a un formato que Pandas entienda (diccionarios)
    tabla_data = []
    for t in st.session_state.nomina:
        tabla_data.append({
            "Nombre": t.get_nombre(),
            "Puesto/Resumen": t.get_resumen(),
            "Jefe Inmediato": t.get_jefe(),
            "Estado": t.get_estado()
        })
    
    df = pd.DataFrame(tabla_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aún no hay trabajadores registrados. Comience creando al Gerente.")