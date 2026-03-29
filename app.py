import streamlit as st
import pandas as pd
import json
import os
from services.rrhh_service import validar_y_crear
from models.trabajador import Gerente, JefeArea, Tecnico, Asistente

st.set_page_config(page_title="Business Corporation - RRHH", page_icon="🏢", layout="wide")
st.title("Instituto Continental - RRHH")

ARCHIVO_NOMINA = "data/nomina.json"
os.makedirs("data", exist_ok=True)


def objeto_a_dict(trabajador):
    datos = {
        "nombre": trabajador.get_nombre(),
        "jefe":   trabajador.get_jefe_inmediato(),
        "estado": trabajador.get_estado(),
        "tipo":   type(trabajador).__name__
    }
    if isinstance(trabajador, Tecnico):
        datos["exp"] = trabajador.get_exp()
    return datos


def dict_a_objeto(datos):
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

    if estado != "Activo":
        obj.set_estado(estado)
    return obj


def cargar_nomina():
    if not os.path.exists(ARCHIVO_NOMINA):
        return None
    with open(ARCHIVO_NOMINA, "r", encoding="utf-8") as f:
        lista = json.load(f)
    return [dict_a_objeto(d) for d in lista]


def guardar_nomina(nomina):
    lista = [objeto_a_dict(t) for t in nomina]
    with open(ARCHIVO_NOMINA, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


# --- CARGA INICIAL ---
if "nomina" not in st.session_state:
    nomina_guardada = cargar_nomina()
    if nomina_guardada:
        st.session_state.nomina = nomina_guardada
    else:
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
        guardar_nomina(st.session_state.nomina)


# ============================================================
# TABS PRINCIPALES
# ============================================================
tab_registro, tab_nomina, tab_baja, tab_jerarquia = st.tabs([
    "➕ Registrar", "📋 Nómina", "🔴 Dar de Baja", "🌳 Jerarquía"
])


# ============================================================
# TAB 1 — REGISTRAR NUEVO TRABAJADOR
# ============================================================
with tab_registro:
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
            jefe = st.selectbox("Jefe Inmediato", nombres_jefes if nombres_jefes else ["Sin trabajadores"])
        exp = st.number_input("Años de Experiencia (solo Técnicos)", min_value=0)

    if st.button("Registrar en Nómina", type="primary"):
        try:
            nuevo = validar_y_crear(nombre, puesto, jefe, exp, st.session_state.nomina)
            st.session_state.nomina.append(nuevo)
            guardar_nomina(st.session_state.nomina)
            st.success(f"¡{puesto} **{nombre}** registrado con éxito!")
        except Exception as e:
            st.error(f"Error: {e}")


# ============================================================
# TAB 2 — NÓMINA CON COLORES, FILTRO Y TABLA POR ÁREA
# ============================================================
with tab_nomina:
    st.write("### 📋 Nómina Actual")

    # Buscador
    busqueda = st.text_input("🔍 Buscar por nombre o puesto", placeholder="Escribe para filtrar...")

    # Construimos los datos con el estado resuelto a texto legible
    ESTADOS = {"Activo": "Activo", "TC": "Término de contrato", "D": "Despido", "R": "Renuncia"}

    todos = []
    for t in st.session_state.nomina:
        todos.append({
            "Nombre":          t.get_nombre(),
            "Puesto":          t.get_resumen(),
            "Jefe Inmediato":  t.get_jefe_inmediato(),
            "Estado":          t.get_estado(),
            "Estado Texto":    ESTADOS.get(t.get_estado(), t.get_estado()),
            # Guardamos el tipo para poder agrupar por área
            "Área":            t.get_jefe_inmediato() if not isinstance(t, Gerente) else "Dirección General",
        })

    df_total = pd.DataFrame(todos)

    # Aplicar filtro de búsqueda
    if busqueda:
        mask = (
            df_total["Nombre"].str.contains(busqueda, case=False, na=False) |
            df_total["Puesto"].str.contains(busqueda, case=False, na=False)
        )
        df_filtrado = df_total[mask]
    else:
        df_filtrado = df_total

    # Función para colorear filas según estado
    def colorear_estado(val):
        if val == "Activo":
            return "background-color: #d4edda; color: #155724"   # verde suave
        elif val in ("TC", "D", "R"):
            return "background-color: #f8d7da; color: #721c24"   # rojo suave
        return ""

    # Mostrar contadores rápidos
    col_a, col_b, col_c = st.columns(3)
    activos = df_total[df_total["Estado"] == "Activo"].shape[0]
    bajas   = df_total[df_total["Estado"] != "Activo"].shape[0]
    col_a.metric("Total trabajadores", len(df_total))
    col_b.metric("Activos", activos, delta=None)
    col_c.metric("Con baja", bajas, delta=f"-{bajas}" if bajas else None,
                 delta_color="inverse" if bajas else "off")

    st.divider()

    # Opción: ver todos juntos o separados por área
    ver_por_area = st.toggle("Separar tabla por área / jefe")

    columnas_mostrar = ["Nombre", "Puesto", "Jefe Inmediato", "Estado Texto"]

    if ver_por_area:
        # Agrupamos por el jefe inmediato (= área)
        areas = df_filtrado["Área"].unique()
        for area in areas:
            grupo = df_filtrado[df_filtrado["Área"] == area][columnas_mostrar].copy()
            grupo.columns = ["Nombre", "Puesto", "Jefe Inmediato", "Estado"]
            st.write(f"**📁 Área: {area}** — {len(grupo)} persona(s)")
            st.dataframe(
                grupo.style.applymap(colorear_estado, subset=["Estado"]),
                use_container_width=True,
                hide_index=True
            )
            st.write("")
    else:
        df_mostrar = df_filtrado[columnas_mostrar].copy()
        df_mostrar.columns = ["Nombre", "Puesto", "Jefe Inmediato", "Estado"]
        st.dataframe(
            df_mostrar.style.applymap(colorear_estado, subset=["Estado"]),
            use_container_width=True,
            hide_index=True
        )

    if busqueda and df_filtrado.empty:
        st.info("No se encontraron trabajadores con ese criterio.")


# ============================================================
# TAB 3 — DAR DE BAJA
# ============================================================
with tab_baja:
    st.write("### 🔴 Dar de Baja a un Trabajador")

    # Solo mostramos trabajadores que están activos
    activos_lista = [t for t in st.session_state.nomina if t.get_estado() == "Activo"]

    if not activos_lista:
        st.info("No hay trabajadores activos en la nómina.")
    else:
        nombres_activos = [t.get_nombre() for t in activos_lista]
        seleccionado    = st.selectbox("Seleccionar trabajador", nombres_activos)
        motivo          = st.selectbox("Motivo de la baja", [
            "TC — Término de contrato",
            "D — Despido",
            "R — Renuncia"
        ])

        # Extraemos solo el código del motivo (TC, D o R)
        codigo_motivo = motivo.split(" — ")[0]

        if st.button("Confirmar Baja", type="primary"):
            for t in st.session_state.nomina:
                if t.get_nombre() == seleccionado:
                    t.set_estado(codigo_motivo)
                    break
            guardar_nomina(st.session_state.nomina)
            st.success(f"Se registró la baja de **{seleccionado}** por motivo: {motivo}")
            st.rerun()


# ============================================================
# TAB 4 — ÁRBOL DE JERARQUÍA
# ============================================================
with tab_jerarquia:
    st.write("### 🌳 Árbol de Jerarquía")

    ESTADOS_ICONO = {"Activo": "🟢", "TC": "🔴", "D": "🔴", "R": "🔴"}

    # Encontramos al gerente (no tiene jefe)
    gerentes = [t for t in st.session_state.nomina if isinstance(t, Gerente)]

    for gerente in gerentes:
        icono = ESTADOS_ICONO.get(gerente.get_estado(), "⚪")
        st.markdown(f"## {icono} {gerente.get_nombre()} — *Gerente General*")

        # Buscamos los jefes de área que dependen del gerente
        jefes = [t for t in st.session_state.nomina
                 if isinstance(t, JefeArea) and t.get_jefe_inmediato() == gerente.get_nombre()]

        for jefe in jefes:
            icono_j = ESTADOS_ICONO.get(jefe.get_estado(), "⚪")
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;📂 {icono_j} **{jefe.get_nombre()}** — *Jefe de Área*")

            # Buscamos técnicos y asistentes de ese jefe
            subordinados = [t for t in st.session_state.nomina
                            if t.get_jefe_inmediato() == jefe.get_nombre()]

            tecnicos   = [t for t in subordinados if isinstance(t, Tecnico)]
            asistentes = [t for t in subordinados if isinstance(t, Asistente)]

            for tec in tecnicos:
                icono_t = ESTADOS_ICONO.get(tec.get_estado(), "⚪")
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🔧 {icono_t} {tec.get_nombre()} — *{tec.get_resumen()}*")

            for asi in asistentes:
                icono_a = ESTADOS_ICONO.get(asi.get_estado(), "⚪")
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📎 {icono_a} {asi.get_nombre()} — *Asistente*")

        st.write("")

    # Leyenda
    st.divider()
    st.caption("🟢 Activo &nbsp;&nbsp; 🔴 Con baja (TC / D / R) &nbsp;&nbsp; 📂 Área &nbsp;&nbsp; 🔧 Técnico &nbsp;&nbsp; 📎 Asistente")