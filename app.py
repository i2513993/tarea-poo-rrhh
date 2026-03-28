import streamlit as st
import pandas as pd
from services.rrhh_service import obtener_nomina

st.set_page_config(page_title="Business Corporation RRHH", layout="wide")
st.title("🏢 Sistema de Recursos Humanos - Business Corp")

# Cargar el Array de Objetos
if 'nomina' not in st.session_state:
    st.session_state.nomina = obtener_nomina()

# Mostrar Resúmenes
st.subheader("📋 Resumen Jerárquico de Trabajadores")
for t in st.session_state.nomina:
    with st.expander(f"{t.get_nombre()} - {t.get_estado()}"):
        st.write(f"**Resumen:** {t.get_resumen()}")
        st.write(f"**Jefe Inmediato:** {t.get_jefe_inmediato()}")
        st.write(f"**Estado Actual:** {t.get_estado()}")

# Mostrar Tabla de Datos (Pandas)
st.subheader("📊 Vista General de Datos")
datos = []
for t in st.session_state.nomina:
    datos.append({
        "Nombre Completo": t.get_nombre(),
        "Jefe Inmediato": t.get_jefe_inmediato(),
        "Estado": t.get_estado()
    })

df = pd.DataFrame(datos)
st.dataframe(df, use_container_width=True)