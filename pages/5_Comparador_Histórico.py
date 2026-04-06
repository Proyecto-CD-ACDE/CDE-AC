import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os, sys, re, re

st.set_page_config(page_title="Comparador · CDE-AC", layout="wide", page_icon="⚖️")

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
    pais_col, delito_col, genero_col, edad_col, sit_col = cols[1], cols[3], cols[6], cols[7], cols[5]

    st.markdown("""
    <p class="page-eyebrow">Módulo 6</p>
    <p class="page-title">Comparador <em>Histórico</em></p>
    <p class="page-desc">Benchmarking interactivo: Análisis cara a cara de las dinámicas criminales entre dos naciones.</p>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # CONTROLES
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    
    paises_validos = df[~df[pais_col].isin(["DESCONOCIDO", "EXTRADICION"])][pais_col].value_counts().head(30).index.tolist()
    
    c_ctrl1, c_ctrl2 = st.columns(2)
    with c_ctrl1:
        pais_a = st.selectbox("🌐 Selecciona el País A", options=paises_validos, index=paises_validos.index("ESTADOS UNIDOS") if "ESTADOS UNIDOS" in paises_validos else 0)
    with c_ctrl2:
        pais_b = st.selectbox("🌐 Selecciona el País B", options=paises_validos, index=paises_validos.index("ESPAÑA") if "ESPAÑA" in paises_validos else 1)

    df_a = df[df[pais_col] == pais_a]
    df_b = df[df[pais_col] == pais_b]

    # ══════════════════════════════════════════════
    # KPIs COMPARATIVOS
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<h3 style='text-align:center; color:#e8a838;'>{pais_a}</h3>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.metric("Registros Totales", f"{len(df_a):,}")
        with k2: st.metric("% Hombres", f"{(df_a[genero_col]=='MASCULINO').sum() / max(len(df_a),1) * 100:.1f}%")
        with k3: st.metric("Delitos Diferentes", df_a[delito_col].nunique())
            
    with col2:
        st.markdown(f"<h3 style='text-align:center; color:#3fb9a0;'>{pais_b}</h3>", unsafe_allow_html=True)
        k4, k5, k6 = st.columns(3)
        with k4: st.metric("Registros Totales", f"{len(df_b):,}")
        with k5: st.metric("% Hombres", f"{(df_b[genero_col]=='MASCULINO').sum() / max(len(df_b),1) * 100:.1f}%")
        with k6: st.metric("Delitos Diferentes", df_b[delito_col].nunique())

    # ══════════════════════════════════════════════
    # RADAR CHART: PERFIL DE DELITOS
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🕸️", "Radar Criminológico: Tipologías Predominantes"), unsafe_allow_html=True)

    # Obtenemos los top 6 delitos combinados de ambos paises para el radar
    top_delitos_ambos = pd.concat([df_a[delito_col], df_b[delito_col]]).value_counts().head(6).index.tolist()
    
    pct_a = []
    pct_b = []
    
    for d in top_delitos_ambos:
        pct_a.append((df_a[delito_col] == d).sum() / max(len(df_a),1) * 100)
        pct_b.append((df_b[delito_col] == d).sum() / max(len(df_b),1) * 100)
        
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=pct_a + [pct_a[0]], theta=top_delitos_ambos + [top_delitos_ambos[0]],
        fill='toself', name=pais_a, fillcolor='rgba(232, 168, 56, 0.4)', line=dict(color='#e8a838')
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=pct_b + [pct_b[0]], theta=top_delitos_ambos + [top_delitos_ambos[0]],
        fill='toself', name=pais_b, fillcolor='rgba(63, 185, 160, 0.4)', line=dict(color='#3fb9a0')
    ))

    apply_layout(fig_radar, height=500, title="Proporción de Detenciones por Tipo de Delito (%)")
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(max(pct_a), max(pct_b)) + 5], gridcolor='rgba(201,209,217,0.1)'),
            angularaxis=dict(gridcolor='rgba(201,209,217,0.1)')
        ),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # ══════════════════════════════════════════════
    # BARRAS PARALELAS: EDAD
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("👥", "Comparación de Grupos de Edad (Pirámide)"), unsafe_allow_html=True)
    
    edades = ["ADOLESCENTE", "ADULTO JOVEN", "ADULTO", "ADULTO MAYOR"]
    edades = [e for e in edades if e in df[edad_col].unique()]
    
    a_edad = [ (df_a[edad_col] == e).sum() / max(len(df_a),1) * 100 for e in edades]
    b_edad = [ (df_b[edad_col] == e).sum() / max(len(df_b),1) * 100 for e in edades]
    
    fig_pyr = go.Figure()
    fig_pyr.add_trace(go.Bar(
        y=edades, x=[-val for val in a_edad], orientation='h', 
        name=pais_a, marker_color='#e8a838', hoverinfo='text',
        text=[f"{val:.1f}%" for val in a_edad], textposition='inside'
    ))
    fig_pyr.add_trace(go.Bar(
        y=edades, x=b_edad, orientation='h', 
        name=pais_b, marker_color='#3fb9a0', hoverinfo='text',
        text=[f"{val:.1f}%" for val in b_edad], textposition='inside'
    ))
    
    apply_layout(fig_pyr, barmode='overlay', height=400, title="Distribución de Edad (%) - País A (Izq) vs País B (Der)")
    fig_pyr.update_xaxes(tickvals=[-80, -60, -40, -20, 0, 20, 40, 60, 80], 
                         ticktext=[80, 60, 40, 20, 0, 20, 40, 60, 80])
    st.plotly_chart(fig_pyr, use_container_width=True)

    # ══════════════════════════════════════════════
    # EFICIENCIA JUDICIAL
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("⚖️", "Estatus Judicial frente al Sistema local", "violet"), unsafe_allow_html=True)

    def simp(s):
        u = str(s).upper()
        if "CONDENADO" in u: return "Condenado"
        if "INVESTIGACI" in u: return "En investigación"
        if "JUICIO" in u: return "En juicio"
        return "Otro"

    df_a_sit = df_a.copy(); df_a_sit['Situación'] = df_a_sit[sit_col].apply(simp)
    df_b_sit = df_b.copy(); df_b_sit['Situación'] = df_b_sit[sit_col].apply(simp)
    
    sit_ambos = pd.DataFrame({
        'Situación': ['Condenado', 'En investigación', 'En juicio', 'Otro'],
        pais_a: [ (df_a_sit['Situación'] == s).sum() / max(len(df_a),1) * 100 for s in ['Condenado', 'En investigación', 'En juicio', 'Otro'] ],
        pais_b: [ (df_b_sit['Situación'] == s).sum() / max(len(df_b),1) * 100 for s in ['Condenado', 'En investigación', 'En juicio', 'Otro'] ]
    })
    
    fig_sit = go.Figure()
    fig_sit.add_trace(go.Bar(x=sit_ambos['Situación'], y=sit_ambos[pais_a], name=pais_a, marker_color='#e8a838'))
    fig_sit.add_trace(go.Bar(x=sit_ambos['Situación'], y=sit_ambos[pais_b], name=pais_b, marker_color='#3fb9a0'))
    
    apply_layout(fig_sit, barmode='group', height=400, title="Comparativa de Estado Legal de los Detenidos (%)")
    st.plotly_chart(fig_sit, use_container_width=True)

else:
    st.error("❌ No se pudo cargar el dataset.")

st.sidebar.markdown("### ⚖️ Comparador Histórico")
st.sidebar.markdown("Benchmarking: Usa esta herramienta para contrastar diferencias demográficas y penales entre dos naciones.")
sidebar_nav()
