import streamlit as st
import pandas as pd
import os, sys, re, re

st.set_page_config(page_title="Resultados EDA · CDE-AC", page_icon="📋", layout="wide")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.design import inject_css, section_header, sidebar_nav, DATA_FILE

st.markdown(inject_css(), unsafe_allow_html=True)

# ── Load ──────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        p = DATA_FILE
        df = pd.read_csv(p, encoding="latin-1", low_memory=False)
        # Normalize encoding-broken variants
        pais_c = df.columns[1]
        delit_c = df.columns[3]
        df[pais_c] = df[pais_c].astype(str).apply(
            lambda x: 'ESPAÑA' if re.match(r'ESPA.{1,3}A$', x) else x)
        df[delit_c] = df[delit_c].astype(str).apply(
            lambda x: 'NARCOTRÁFICO' if re.match(r'NARCOTR.{1,3}FICO', x) else x)
        return df
    except UnicodeDecodeError:
        df = pd.read_csv(p, encoding="latin-1", low_memory=False)
        # Normalize encoding-broken variants
        pais_c = df.columns[1]
        delit_c = df.columns[3]
        df[pais_c] = df[pais_c].astype(str).apply(
            lambda x: 'ESPAÑA' if re.match(r'ESPA.{1,3}A$', x) else x)
        df[delit_c] = df[delit_c].astype(str).apply(
            lambda x: 'NARCOTRÁFICO' if re.match(r'NARCOTR.{1,3}FICO', x) else x)
        return df
    except:
        return None

df = load_data()
cols = list(df.columns) if df is not None else []

# ── Header ────────────────────────────────────────────
st.markdown("""
<p class="page-eyebrow">Módulo 2</p>
<p class="page-title">Resultados del <em>EDA</em></p>
<p class="page-desc">Reporte consolidado de hallazgos — documenta, edita si lo deseas, y genera un reporte descargable.</p>
""", unsafe_allow_html=True)

# ── Reference ─────────────────────────────────────────
if df is not None:
    st.markdown(f"""
    <div class="sep"></div>
    <div class="card card--bordered-teal">
        <h4>📌 Referencia rápida del dataset</h4>
        <p>
            <strong class="text-gold">{df.shape[0]:,}</strong> registros · 
            <strong class="text-gold">{df.shape[1]}</strong> variables · 
            <strong class="text-gold">{df[cols[1]].nunique()}</strong> países · 
            Período <strong class="text-gold">2018 – 2025</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
st.markdown(section_header("🔍", "Identificación y Contexto"), unsafe_allow_html=True)
contexto = st.text_area(
    "¿De qué se trata el dataset?",
    value="El dataset trata sobre el registro histórico de ciudadanos colombianos detenidos en países extranjeros. Su propósito es documentar la magnitud de la delincuencia transnacional, identificar patrones geográficos y tipos de delitos, y fundamentar políticas públicas en cooperación internacional y repatriación. La fuente principal es el Ministerio de Relaciones Exteriores de Colombia, que recopila esta información a través de su red consular.",
    height=140)

st.markdown(section_header("❗", "Calidad de los Datos", "coral"), unsafe_allow_html=True)
calidad = st.text_area(
    "¿Qué encontraste sobre datos faltantes y limpieza?",
    value="Se identificaron datos faltantes en: UBICACIÓN PAÍS (68.6 % faltante), LATITUD y LONGITUD (13.6 %). Las variables críticas — País de Prisión, Delito, Género, Edad y Situación Jurídica — están 100 % completas. Los faltantes en geolocalización se deben a restricciones de privacidad y no afectan el análisis criminológico principal.",
    height=160)

st.markdown(section_header("📈", "Hallazgos Estadísticos", "blue"), unsafe_allow_html=True)
estadisticas = st.text_area(
    "Interpretación de números y categorías principales",
    value="(1) País de Prisión: Venezuela lidera con 26,465 casos, seguido de EE.UU. (24,329) y Ecuador (17,979). (2) Delito: Narcotráfico es el más frecuente (~91,000 registros combinados), seguido de Robo/Hurto (46,910) y Homicidio (30,259). (3) Género: 79 % masculino, 21 % femenino. (4) Situación Jurídica: 42 % condenados, 36 % en investigación, 14 % en juicio. La distribución es altamente concentrada, indicando patrones estructurados.",
    height=160)

st.markdown(section_header("💡", "Conclusiones", "violet"), unsafe_allow_html=True)
conclusion = st.text_area(
    "¿Cuál es el mensaje principal?",
    value="La delincuencia transnacional de colombianos es un fenómeno estructurado: (1) 388,148 casos documentados — problema sistemático; (2) Concentración en países vecinos y centros de narcotráfico; (3) Narcotráfico domina, pero hay diversidad de delitos; (4) Perfil predominante: hombres adultos; participación femenina notable en narcotráfico; (5) Variables críticas al 100 % que permiten análisis confiables.",
    height=140)

# ── Report ────────────────────────────────────────────
st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
st.markdown(section_header("🚀", "Generar Reporte"), unsafe_allow_html=True)

c1, _ = st.columns([1,3])
with c1:
    generar = st.button("📄 Generar Reporte", use_container_width=True, type="primary")

if generar and contexto and calidad and estadisticas and conclusion and df is not None:
    st.success("✅ Reporte generado")

    reporte = f"""# Reporte — Análisis Exploratorio de Datos Criminales
## Colombianos Detenidos en el Exterior

**Fecha:** {pd.Timestamp.now().strftime('%d de %B de %Y')}
**Fuente:** Dataset CDE-AC | **Registros:** {df.shape[0]:,} | **Variables:** {df.shape[1]} | **Período:** 2018–2025

---

## 1. Contexto
{contexto}

## 2. Calidad de los Datos
{calidad}

| Aspecto | Estado |
|---------|--------|
| Análisis de delitos, países, demografía | ✅ Confiable |
| Análisis espacial detallado | ⚠️ Limitado |
| Análisis temporal y legal | ✅ Completo |

## 3. Hallazgos Estadísticos
{estadisticas}

| Indicador | Valor |
|-----------|-------|
| Magnitud | {df.shape[0]:,} casos |
| Países | {df[cols[1]].nunique()} |
| Completitud vars. críticas | 100 % |
| Patrón | Estructurado |

## 4. Conclusiones
{conclusion}

### Recomendaciones
1. Fortalecer cooperación con países de detención predominantes
2. Focalizar prevención en tipologías criminales prevalentes
3. Incorporar perspectiva de género en estrategias
4. Implementar monitoreo predictivo continuo
5. Desarrollar programas de reinserción post-detención

---
*Proyecto CDE-AC · Juan Esteban Montoya Cadavid & Angel Manuel Gaviria · © 2026*
"""
    st.markdown(reporte)
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.download_button("📥 Descargar Reporte (.md)", reporte,
                       "Reporte_EDA_CDE-AC.md", "text/markdown", type="primary")
elif generar:
    st.warning("Completa todas las secciones antes de generar.")

# ── Sidebar ───────────────────────────────────────────
st.sidebar.markdown("### 📋 Resultados del EDA")
st.sidebar.markdown("Documenta hallazgos y genera un reporte descargable en Markdown.")
if df is not None:
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Registros:** {df.shape[0]:,}")
    st.sidebar.markdown(f"**Variables:** {df.shape[1]}")
sidebar_nav()
