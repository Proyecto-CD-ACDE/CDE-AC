import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os, sys, re, re

st.set_page_config(page_title="Conclusiones · CDE-AC", layout="wide", page_icon="📌")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.design import (inject_css, section_header, sidebar_nav,
                         CHART_COLORS, SCALE_GOLD, SCALE_TEAL, SCALE_CORAL, apply_layout,
                         DATA_FILE)

st.markdown(inject_css(), unsafe_allow_html=True)

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
    except Exception as e:
        st.error(f"Error: {e}"); return None

df = load_data()

if df is not None:
    cols = list(df.columns)
    pais_col, delito_col = cols[1], cols[3]
    sit_col, genero_col, fecha_col = cols[5], cols[6], cols[0]
    extrad_col = cols[4]

    total = len(df)
    paises_uniq = df[~df[pais_col].isin(["DESCONOCIDO", "EXTRADICION"])][pais_col].nunique()
    delitos_uniq = df[~df[delito_col].isin(["DESCONOCIDO"])][delito_col].nunique()
    top_pais = df[~df[pais_col].isin(["DESCONOCIDO", "EXTRADICION"])][pais_col].value_counts().index[0]
    pct_masc = (df[genero_col] == "MASCULINO").sum() / total * 100
    pct_cond = df[sit_col].str.contains("CONDENADO", case=False, na=False).sum() / total * 100
    extrad_tot = df[df[extrad_col].str.contains("EXTRADICION", case=False, na=False)].shape[0]

    st.markdown("""
    <p class="page-eyebrow">Módulo 8</p>
    <p class="page-title">Conclusiones <em>Finales</em></p>
    <p class="page-desc">Resumen ejecutivo del análisis criminológico estructurado.</p>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📊", "Dashboard Resumen"), unsafe_allow_html=True)

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-val">{total:,}</div>
            <div class="kpi-label">Registros</div>
        </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-val">{paises_uniq}</div>
            <div class="kpi-label">Países</div>
        </div>
        """, unsafe_allow_html=True)
    with d3:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-val">{top_pais}</div>
            <div class="kpi-label">Mayor concentración</div>
        </div>
        """, unsafe_allow_html=True)
    with d4:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-val">{pct_cond:.0f} %</div>
            <div class="kpi-label">Condenados</div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # VISUALIZACIÓN RESUMEN
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📈", "Síntesis Visual", "teal"), unsafe_allow_html=True)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Top 10 Países", "Top 8 Delitos", "Género", "Situación Jurídica"),
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "pie"}, {"type": "pie"}]],
        vertical_spacing=0.15, horizontal_spacing=0.1
    )

    # Paises
    top_p = df[~df[pais_col].isin(["DESCONOCIDO", "EXTRADICION"])][pais_col].value_counts().head(10)
    fig.add_trace(go.Bar(x=top_p.values, y=top_p.index, orientation="h", marker_color="#e8a838"), row=1, col=1)

    # Delitos
    top_d = df[~df[delito_col].isin(["DESCONOCIDO"])][delito_col].value_counts().head(8)
    fig.add_trace(go.Bar(x=top_d.values, y=top_d.index, orientation="h", marker_color="#e06c60"), row=1, col=2)

    # Género
    gen = df[genero_col].value_counts()
    fig.add_trace(go.Pie(values=gen.values, labels=gen.index, hole=0.45,
                         marker_colors=["#58a6ff","#f472b6","#a78bfa","#e8a838"]), row=2, col=1)

    # Juridica
    def simp(s):
        u = str(s).upper()
        if "CONDENADO" in u: return "Condenado"
        if "INVESTIGACI" in u: return "Investigación"
        if "JUICIO" in u: return "En juicio"
        if "DEPORTACI" in u: return "Deportación"
        if "EXTRADITADO" in u: return "Extraditado"
        return "Otro"

    sit = df[sit_col].apply(simp).value_counts()
    fig.add_trace(go.Pie(values=sit.values, labels=sit.index, hole=0.45,
                         marker_colors=CHART_COLORS), row=2, col=2)

    apply_layout(fig, height=650, showlegend=False)
    fig.update_yaxes(autorange="reversed", row=1, col=1)
    fig.update_yaxes(autorange="reversed", row=1, col=2)
    st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════════════
    # CONCLUSIONES
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🎯", "Conclusiones Principales", "violet"), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="conc">
            <h4>🌍 Concentración Geográfica</h4>
            <p>Las detenciones se concentran en países americanos, especialmente en Venezuela 
            ({df[df[pais_col]=='VENEZUELA'].shape[0]:,} casos), EE.UU. e Ecuador. 
            La proximidad y rutas de tráfico son determinantes.</p>
        </div>
        <div class="conc">
            <h4>👤 Perfil Demográfico</h4>
            <p>Perfil predominante: <strong class="text-blue">masculino ({pct_masc:.0f} %)</strong> adulto. 
            Sin embargo, la participación femenina en narcotráfico es proporcionalmente mayor, 
            sugiriendo roles específicos en las redes.</p>
        </div>
        <div class="conc">
            <h4>📅 Patrón Sistemático</h4>
            <p>Los datos muestran un fenómeno <strong class="text-violet">estructural y persistente</strong> 
            (2018-2025), no coyuntural. Los patrones generales se mantienen a lo largo de los años.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="conc">
            <h4>⚖️ Narcotráfico Predominante</h4>
            <p>Confirma el papel de Colombia en redes internacionales de tráfico de drogas, siendo 
            este el delito más frecuente en la mayoría de los países.</p>
        </div>
        <div class="conc">
            <h4>📋 Eficiencia Judicial</h4>
            <p>El <strong class="text-coral">{pct_cond:.0f} %</strong> de los detenidos están condenados y hay 
            {extrad_tot:,} casos de extradición, indicando cooperación judicial activa.</p>
        </div>
        <div class="conc">
            <h4>📊 Calidad de la Información</h4>
            <p>Las variables críticas (país, delito, demografía) tienen una completitud del 100%, 
            permitiendo análisis criminológicos confiables y precisos.</p>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # FUTURO
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🚀", "Limitaciones y Trabajo Futuro", "coral"), unsafe_allow_html=True)

    lf1, lf2 = st.columns(2)
    with lf1:
        st.markdown("""
        <div class="card card--bordered-coral">
            <h4>⚠️ Limitaciones</h4>
            <ul>
                <li>Datos de geolocalización incompletos (68 % faltante en ubicación exacta)</li>
                <li>Posible subregistro dependiendo de acuerdos de información de cada país</li>
                <li>Ausencia de variables socioeconómicas previas a la detención</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with lf2:
        st.markdown("""
        <div class="card card--bordered-blue">
            <h4>🔬 Trabajo Futuro</h4>
            <ul>
                <li>Modelos de machine learning para predecir riesgo por perfil</li>
                <li>Análisis de redes (Network Analysis) en rutas criminales</li>
                <li>Integración con bases de datos del DANE e indicadores económicos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("❌ No se pudo cargar el dataset.")

st.sidebar.markdown("### 📌 Conclusiones")
st.sidebar.markdown("Resumen ejecutivo de los hallazgos descritos a lo largo del EDA.")
sidebar_nav()
