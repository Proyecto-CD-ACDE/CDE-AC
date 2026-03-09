import streamlit as st

# Configuración de la página
st.set_page_config(
   page_title="Proyecto CD - Colombianos Detenidos en el Exterior",
   page_icon="🇨🇴",
   layout="wide",
   initial_sidebar_state="expanded"
)

# --- Estilo Personalizado (Opcional) ---
st.markdown("""
   <style>
   .main {
       background-color: #f8f9fa;
   }
   .stAlert {
       border-radius: 10px;
   }
   </style>
   """, unsafe_allow_html=True)

# --- Título Principal ---
st.title("🇨🇴 Proyecto CD: Colombianos Detenidos en el Exterior")
st.subheader("Análisis Criminológico de Delincuencia Transnacional")

st.divider()

# --- 1. Introducción ---
col1, col2 = st.columns([2, 1])

with col1:
   st.header("📖 Introducción")
   st.write("""
   Este proyecto analiza el dataset de **colombianos detenidos en el exterior** con el propósito de comprender los patrones de delincuencia transnacional, identificar países de mayor incidencia y contribuir al diseño de políticas públicas informadas en criminología internacional.

   A través de técnicas avanzadas de **Análisis Exploratorio de Datos (EDA)**, exploraremos cómo la ciencia de datos puede revelar patrones ocultos en la movilidad criminal y apoyar la toma de decisiones estratégicas en materia de seguridad internacional.
   """)

with col2:
   st.info("💡 **Dato Curioso:** Colombia es uno de los países con mayor presencia de ciudadanos detenidos en el exterior, representando un desafío significativo para la política exterior y la cooperación internacional.")

# --- 2. Objetivos ---
st.header("🎯 Objetivos del Proyecto")

obj_gen, obj_esp = st.columns(2)

with obj_gen:
   st.subheader("Objetivo General")
   st.markdown("""
   - Desarrollar un análisis criminológico integral del dataset de colombianos detenidos en el exterior para identificar patrones de delincuencia transnacional y apoyar el diseño de políticas públicas efectivas.
   """)

with obj_esp:
   st.subheader("Objetivos Específicos")
   st.markdown("""
   - Realizar un **Análisis Exploratorio de Datos (EDA)** completo del dataset.
   - Identificar patrones geográficos y temporales de la delincuencia transnacional.
   - Analizar la distribución por tipos de delito y características demográficas.
   - Generar visualizaciones interactivas para facilitar la comprensión de los datos.
   - Contribuir al conocimiento criminológico sobre movilidad criminal internacional.
   """)

st.divider()

# --- 3. Equipo de Trabajo ---
st.header("👥 Equipo de Trabajo")

# Integrantes del proyecto
integrantes = [
   {"nombre": "Juan Esteban Montoya Cadavid", "emoji": "👨‍💻"},
   {"nombre": "Angel Manuel Gaviria", "emoji": "👨‍🔬"},
]

cols = st.columns(len(integrantes))

for i, persona in enumerate(integrantes):
   with cols[i]:
       st.markdown(f"""
       ### {persona['emoji']} {persona['nombre']}
       """)

st.divider()

# --- 4. Tecnologías Utilizadas ---
st.header("🛠️ Tecnologías")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
   st.markdown("### 🐍 Python")
   st.write("Lenguaje base para el procesamiento y análisis de datos.")

with tech_col2:
   st.markdown("### 🐼 Pandas")
   st.write("Librería para manipulación y análisis de estructuras de datos.")

with tech_col3:
   st.markdown("### 🎈 Streamlit")
   st.write("Framework para la creación de aplicaciones web interactivas.")

# --- Pie de página ---
st.sidebar.success("👈 Usa el menú lateral para navegar entre las secciones del proyecto.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Proyecto CD: Análisis de Delincuencia Transnacional")