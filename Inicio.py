import streamlit as st
import pandas as pd
import os, sys, re, re

st.set_page_config(
    page_title="CDE-AC · Colombianos Detenidos en el Exterior",
    page_icon="🇨🇴",
    layout="wide",
    initial_sidebar_state="expanded",
)

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from src.design import inject_css, kpi_tile, section_header, sidebar_nav

st.markdown(inject_css(), unsafe_allow_html=True)

# ── Data summary ──────────────────────────────────────
@st.cache_data
def dataset_summary():
    try:
        path = os.path.join(os.path.dirname(__file__), "src", "data",
                            "Colombianos_detenidos_en_el_exterior_20260309.csv")
        df = pd.read_csv(path, encoding="latin-1", low_memory=False)
        cols = list(df.columns)
        return dict(
            rows=len(df),
            cols_n=df.shape[1],
            countries=df[cols[1]].nunique(),
            crimes=df[cols[3]].nunique(),
            year_min=str(df[cols[0]].min())[:4],
            year_max=str(df[cols[0]].max())[:4],
        )
    except Exception:
        return None

s = dataset_summary()

# ═══════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════
st.markdown("""
<div style="padding:24px 0 4px 0;">
    <p class="page-eyebrow">Proyecto CDE-AC</p>
    <p class="page-title">Colombianos <em>Detenidos</em><br>en el Exterior</p>
    <p class="page-desc">
        Análisis criminológico de delincuencia transnacional basado en datos abiertos 
        del Ministerio de Relaciones Exteriores — un estudio integral desde la ciencia de datos.
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# KPIs
# ═══════════════════════════════════════════════════════
if s:
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(kpi_tile(f"{s['rows']:,}", "Registros", "Dataset completo"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_tile(str(s['countries']), "Países", "Con detenciones"), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_tile(str(s['crimes']), "Tipos de delito", "Clasificados"), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_tile(str(s['cols_n']), "Variables", "Documentadas"), unsafe_allow_html=True)
    with k5:
        st.markdown(kpi_tile(f"{s['year_min']}–{s['year_max']}", "Período", "Rango temporal"), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# INTRODUCCIÓN
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
st.markdown(section_header("📖", "Introducción"), unsafe_allow_html=True)

col_a, col_b = st.columns([5, 3])
with col_a:
    st.markdown("""
    <div class="card card--bordered-gold">
        <p>Este proyecto analiza el dataset de <strong>colombianos detenidos en el exterior</strong> con el propósito 
        de comprender los patrones de delincuencia transnacional, identificar países de mayor incidencia y contribuir al 
        diseño de políticas públicas informadas en criminología internacional.</p>
        <p style="margin-top:12px;">A través de técnicas de <strong class="text-gold">Análisis Exploratorio de Datos (EDA)</strong>, 
        la ciencia de datos revela patrones ocultos en la movilidad criminal y apoya la toma de decisiones estratégicas 
        en seguridad internacional.</p>
    </div>
    """, unsafe_allow_html=True)
with col_b:
    st.markdown("""
    <div class="card card--highlight">
        <span class="tag tag--gold">Dato clave</span>
        <p style="margin-top:10px;">Colombia es uno de los países con mayor presencia de ciudadanos detenidos en 
        el exterior, representando un desafío para la política exterior y la cooperación internacional.</p>
        <p style="margin-top:8px;">Este dataset reúne <strong class="text-gold">388,148</strong> registros históricos 
        en <strong class="text-gold">93 países</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# OBJETIVOS
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
st.markdown(section_header("🎯", "Objetivos del Proyecto"), unsafe_allow_html=True)

og, oe = st.columns(2)
with og:
    st.markdown("""
    <div class="card card--bordered-teal">
        <h4>Objetivo General</h4>
        <p>Desarrollar un análisis criminológico integral del dataset de colombianos detenidos en el exterior 
        para identificar patrones de delincuencia transnacional y apoyar el diseño de políticas públicas efectivas.</p>
    </div>
    """, unsafe_allow_html=True)
with oe:
    st.markdown("""
    <div class="card card--bordered-blue">
        <h4>Objetivos Específicos</h4>
        <ul>
            <li>Realizar un <strong>Análisis Exploratorio (EDA)</strong> completo</li>
            <li>Identificar patrones geográficos y temporales</li>
            <li>Analizar distribución por delito y demografía</li>
            <li>Generar visualizaciones interactivas</li>
            <li>Proponer recomendaciones de política pública</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# METODOLOGÍA
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
st.markdown(section_header("📐", "Metodología", "teal"), unsafe_allow_html=True)

st.markdown("""
<div style="display:flex;gap:6px;flex-wrap:wrap;">
    <div class="step" style="flex:1;min-width:140px;">
        <div class="step-num">Paso 01</div>
        <div class="step-title">Recolección</div>
        <div class="step-desc">Carga del dataset desde fuentes oficiales abiertas</div>
    </div>
    <div class="step" style="flex:1;min-width:140px;">
        <div class="step-num">Paso 02</div>
        <div class="step-title">Limpieza</div>
        <div class="step-desc">Preprocesamiento y validación de calidad</div>
    </div>
    <div class="step" style="flex:1;min-width:140px;">
        <div class="step-num">Paso 03</div>
        <div class="step-title">Exploración</div>
        <div class="step-desc">Estadísticas descriptivas y distribuciones</div>
    </div>
    <div class="step" style="flex:1;min-width:140px;">
        <div class="step-num">Paso 04</div>
        <div class="step-title">Visualización</div>
        <div class="step-desc">Gráficos interactivos y mapas</div>
    </div>
    <div class="step" style="flex:1;min-width:140px;">
        <div class="step-num">Paso 05</div>
        <div class="step-title">Conclusiones</div>
        <div class="step-desc">Hallazgos y recomendaciones</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# MARCO TEÓRICO (resumen)
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
st.markdown(section_header("📚", "Marco Teórico", "violet"), unsafe_allow_html=True)

mt1, mt2, mt3 = st.columns(3)
with mt1:
    st.markdown("""
    <div class="card card--bordered-violet">
        <span class="tag tag--violet">Criminología</span>
        <h4 style="margin-top:10px;">Delincuencia Transnacional</h4>
        <p>Acciones ilícitas que cruzan fronteras nacionales. El análisis de datos permite
        identificar patrones de movilidad, rutas predominantes y tipologías delictivas en el ámbito internacional.</p>
    </div>
    """, unsafe_allow_html=True)
with mt2:
    st.markdown("""
    <div class="card card--bordered-coral">
        <span class="tag tag--coral">Geopolítica</span>
        <h4 style="margin-top:10px;">Distribución Geográfica</h4>
        <p>Los países de detención varían según proximidad a Colombia, rutas de tráfico, 
        nivel de enforcement legal y acuerdos de cooperación internacional vigentes.</p>
    </div>
    """, unsafe_allow_html=True)
with mt3:
    st.markdown("""
    <div class="card card--bordered-blue">
        <span class="tag tag--blue">Política Pública</span>
        <h4 style="margin-top:10px;">Diseño Basado en Evidencia</h4>
        <p>Los datos habilitan políticas informadas de prevención, cooperación bilateral, 
        reinserción social y protección de derechos de los detenidos en jurisdicciones extranjeras.</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# EQUIPO
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
st.markdown(section_header("👥", "Equipo de Trabajo", "blue"), unsafe_allow_html=True)

integrantes = [
    ("👨‍💻", "Juan Esteban Montoya Cadavid", "Desarrollo & Análisis"),
    ("👨‍🔬", "Angel Manuel Gaviria", "Investigación & Datos"),
]
team_cols = st.columns(len(integrantes))
for i, (emoji, name, role) in enumerate(integrantes):
    with team_cols[i]:
        st.markdown(f"""
        <div class="team-member">
            <div class="team-avatar">{emoji}</div>
            <div class="team-name">{name}</div>
            <div class="team-role">{role}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TECNOLOGÍAS
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
st.markdown(section_header("🛠️", "Stack Tecnológico", "teal"), unsafe_allow_html=True)

techs = [
    ("🐍", "Python 3.13", "Lenguaje principal"),
    ("🐼", "Pandas", "Análisis tabular"),
    ("📊", "Plotly", "Gráficos interactivos"),
    ("🎈", "Streamlit", "App web"),
    ("🔢", "NumPy", "Cálculo numérico"),
]
tc = st.columns(len(techs))
for i, (icon, name, desc) in enumerate(techs):
    with tc[i]:
        st.markdown(f"""
        <div class="tech">
            <div class="tech-icon">{icon}</div>
            <div class="tech-name">{name}</div>
            <div class="tech-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# NAVEGACIÓN
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="card card--highlight" style="text-align:center;">
    <h4 style="margin-bottom:14px;">🧭 Navegación del Proyecto</h4>
    <p>Utiliza el menú lateral <strong>←</strong> para navegar entre secciones</p>
    <div style="display:flex;justify-content:center;gap:18px;flex-wrap:wrap;margin-top:14px;">
        <span class="tag tag--gold">Análisis Exploratorio</span>
        <span class="tag tag--teal">Resultados</span>
        <span class="tag tag--blue">Visualizaciones</span>
        <span class="tag tag--violet">Análisis Demográfico</span>
        <span class="tag tag--coral">Conclusiones</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center;padding:12px 0 4px 0;">
    <div style="font-size:1.6rem;">🇨🇴</div>
    <div style="font-size:0.95rem;font-weight:700;color:#e2e8f0;">Proyecto CDE-AC</div>
    <div style="font-size:0.72rem;color:#545d68;margin-top:2px;">Criminología · Ciencia de Datos</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.success("Usa el menú para navegar entre las secciones.")
st.sidebar.markdown("---")
st.sidebar.markdown("**📅 Período:** 2018 – 2025")
st.sidebar.markdown("**🏛️ Fuente:** Datos Abiertos Colombia")
sidebar_nav()
