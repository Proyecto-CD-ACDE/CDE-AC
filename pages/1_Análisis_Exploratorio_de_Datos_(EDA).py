import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys, re

st.set_page_config(page_title="EDA · CDE-AC", layout="wide", page_icon="🔍")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.design import (inject_css, section_header, kpi_tile, sidebar_nav,
                         CHART_COLORS, SCALE_GOLD, SCALE_TEAL, SCALE_CORAL, apply_layout)

st.markdown(inject_css(), unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        p = os.path.join(os.path.dirname(__file__), "..", "src", "data",
                         "Colombianos_detenidos_en_el_exterior_20260309.csv")
        df = pd.read_csv(p, encoding="latin-1", low_memory=False)
        # Normalize broken encoding variants
        pais_col = df.columns[1]
        delito_col = df.columns[3]
        df[pais_col] = df[pais_col].astype(str).apply(
            lambda x: "ESPAÑA" if re.match(r"ESPA.{1,3}A$", x) else x)
        df[delito_col] = df[delito_col].astype(str).apply(
            lambda x: "NARCOTRÁFICO" if re.match(r"NARCOTR.{1,3}FICO", x) else x)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

df = load_data()

if df is not None:
    cols = list(df.columns)
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    pais_col, consulado_col, delito_col = cols[1], cols[2], cols[3]
    extrad_col, sit_col, genero_col, edad_col = cols[4], cols[5], cols[6], cols[7]
    fecha_col = cols[0]

    # ── Header ────────────────────────────────────────────
    st.markdown("""
    <p class="page-eyebrow">Módulo 1</p>
    <p class="page-title">Análisis <em>Exploratorio</em> de Datos</p>
    <p class="page-desc">Exploración completa del dataset con estadísticas descriptivas y visualizaciones interactivas.</p>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # 1. RESUMEN
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📋", "Resumen del Dataset"), unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.markdown(kpi_tile(f"{df.shape[0]:,}", "Registros"), unsafe_allow_html=True)
    with m2: st.markdown(kpi_tile(str(df.shape[1]), "Variables"), unsafe_allow_html=True)
    with m3: st.markdown(kpi_tile(str(len(cat_cols)), "Categóricas"), unsafe_allow_html=True)
    with m4: st.markdown(kpi_tile(str(len(num_cols)), "Numéricas"), unsafe_allow_html=True)
    with m5: st.markdown(kpi_tile(f"{df.isnull().sum().sum():,}", "Nulos totales"), unsafe_allow_html=True)

    with st.expander("👁️ Vista previa del dataset"):
        st.dataframe(df.head(10), use_container_width=True)

    with st.expander("🏗️ Estructura de variables"):
        info = pd.DataFrame({
            "Variable": cols,
            "Tipo": [str(df[c].dtype) for c in cols],
            "No nulos": [df[c].notna().sum() for c in cols],
            "% Completo": [(df[c].notna().sum()/len(df)*100).round(1) for c in cols],
            "Únicos": [df[c].nunique() for c in cols],
        })
        st.dataframe(info, use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════════
    # 2. CALIDAD
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🧹", "Calidad de los Datos", "teal"), unsafe_allow_html=True)

    miss = df.isnull().sum()
    miss_pct = (miss/len(df)*100).round(2)
    qdf = pd.DataFrame({"Variable": cols, "% Completo": (100-miss_pct).values, "% Faltante": miss_pct.values})
    qdf = qdf.sort_values("% Faltante", ascending=False)

    fig_q = go.Figure()
    fig_q.add_trace(go.Bar(y=qdf["Variable"], x=qdf["% Completo"], orientation="h",
                           name="Completo", marker_color="#3fb9a0",
                           text=qdf["% Completo"].apply(lambda v: f"{v:.1f}%"), textposition="inside"))
    fig_q.add_trace(go.Bar(y=qdf["Variable"], x=qdf["% Faltante"], orientation="h",
                           name="Faltante", marker_color="#e06c60",
                           text=qdf["% Faltante"].apply(lambda v: f"{v:.1f}%" if v>0 else ""), textposition="inside"))
    apply_layout(fig_q, barmode="stack", height=380,
                 title="Completitud de datos por variable",
                 xaxis_title="Porcentaje (%)")
    st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("""
    <div class="card card--bordered-teal">
        <h4>✅ Conclusión sobre calidad</h4>
        <p>Las variables críticas (País, Delito, Género, Edad, Situación Jurídica) están
        <strong class="text-teal">100 % completas</strong>. Los faltantes se concentran en geolocalización,
        lo que no afecta el análisis criminológico principal.</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # 3. PAÍS DE PRISIÓN
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🌍", "Distribución por País de Prisión", "blue"), unsafe_allow_html=True)

    pc = df[df[pais_col]!="DESCONOCIDO"][pais_col].value_counts().head(15)

    fig_p = px.bar(x=pc.values, y=pc.index, orientation="h",
                   labels={"x":"Registros","y":""},
                   color=pc.values, color_continuous_scale=SCALE_GOLD)
    apply_layout(fig_p, height=480, title="Top 15 países con mayor número de detenciones",
                 yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_p, use_container_width=True)

    p1,p2,p3 = st.columns(3)
    with p1: st.metric("🥇 País #1", pc.index[0], f"{pc.values[0]:,}")
    with p2: st.metric("🥈 País #2", pc.index[1], f"{pc.values[1]:,}")
    with p3: st.metric("🥉 País #3", pc.index[2], f"{pc.values[2]:,}")

    # ══════════════════════════════════════════════
    # 4. TIPO DE DELITO
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("⚖️", "Distribución por Tipo de Delito", "coral"), unsafe_allow_html=True)

    dc = df[delito_col].value_counts().head(12)

    c41, c42 = st.columns([3,2])
    with c41:
        fig_d = px.bar(x=dc.index, y=dc.values, labels={"x":"","y":"Registros"},
                       color=dc.values, color_continuous_scale=SCALE_CORAL)
        apply_layout(fig_d, height=430, title="Top 12 tipos de delitos registrados",
                     xaxis_tickangle=-40)
        st.plotly_chart(fig_d, use_container_width=True)
    with c42:
        top6 = df[delito_col].value_counts().head(6)
        otros = df[delito_col].value_counts()[6:].sum()
        pie_d = pd.concat([top6, pd.Series({"Otros": otros})])
        fig_dp = px.pie(values=pie_d.values, names=pie_d.index, hole=0.45,
                        color_discrete_sequence=CHART_COLORS)
        apply_layout(fig_dp, height=430, title="Proporción por delito")
        fig_dp.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(fig_dp, use_container_width=True)

    # ══════════════════════════════════════════════
    # 5. PERFIL DEMOGRÁFICO
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("👤", "Perfil Demográfico General", "violet"), unsafe_allow_html=True)

    cg, ce = st.columns(2)
    with cg:
        gc = df[genero_col].value_counts()
        fig_g = px.pie(values=gc.values, names=gc.index, hole=0.5,
                       color_discrete_sequence=["#58a6ff","#f472b6","#a78bfa","#e8a838","#3fb9a0"])
        apply_layout(fig_g, height=380, title="Distribución por género")
        fig_g.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_g, use_container_width=True)
    with ce:
        ec = df[edad_col].value_counts()
        fig_e = px.bar(x=ec.index, y=ec.values, labels={"x":"","y":"Registros"},
                       color=ec.index, color_discrete_sequence=CHART_COLORS)
        apply_layout(fig_e, height=380, title="Distribución por grupo de edad", showlegend=False,
                     xaxis_tickangle=-25)
        st.plotly_chart(fig_e, use_container_width=True)

    # ══════════════════════════════════════════════
    # 6. SITUACIÓN JURÍDICA
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📜", "Situación Jurídica", "teal"), unsafe_allow_html=True)

    sc = df[sit_col].value_counts()
    fig_s = px.bar(x=sc.values, y=sc.index, orientation="h",
                   labels={"x":"Registros","y":""},
                   color=sc.values, color_continuous_scale=SCALE_TEAL)
    apply_layout(fig_s, height=380, title="Estado jurídico de los detenidos")
    st.plotly_chart(fig_s, use_container_width=True)

    # ══════════════════════════════════════════════
    # 7. EVOLUCIÓN TEMPORAL
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📅", "Evolución Temporal"), unsafe_allow_html=True)

    df["_year"] = pd.to_datetime(df[fecha_col], errors="coerce").dt.year
    yc = df["_year"].value_counts().sort_index().dropna()

    fig_t = go.Figure()
    fig_t.add_trace(go.Scatter(
        x=yc.index.astype(int), y=yc.values,
        mode="lines+markers+text",
        line=dict(color="#e8a838", width=2.5),
        marker=dict(size=8, color="#0b0e14", line=dict(width=2, color="#e8a838")),
        text=[f"{v:,}" for v in yc.values],
        textposition="top center", textfont=dict(color="#8b949e", size=10),
        fill="tozeroy", fillcolor="rgba(232,168,56,0.06)",
    ))
    apply_layout(fig_t, height=380, title="Registros por año de publicación",
                 xaxis_title="Año", yaxis_title="Registros")
    st.plotly_chart(fig_t, use_container_width=True)

    # ══════════════════════════════════════════════
    # 8. HEATMAP PAÍS × DELITO
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🔗", "Análisis Cruzado: País × Delito", "coral"), unsafe_allow_html=True)

    tp = df[~df[pais_col].isin(["DESCONOCIDO","EXTRADICION"])][pais_col].value_counts().head(8).index.tolist()
    td = df[~df[delito_col].isin(["DESCONOCIDO"])][delito_col].value_counts().head(6).index.tolist()
    cdf = df[df[pais_col].isin(tp) & df[delito_col].isin(td)]
    ct = pd.crosstab(cdf[pais_col], cdf[delito_col])

    fig_h = px.imshow(ct.values, x=ct.columns.tolist(), y=ct.index.tolist(),
                      color_continuous_scale=SCALE_GOLD, aspect="auto")
    apply_layout(fig_h, height=430, title="Concentración de delitos por país",
                 xaxis_tickangle=-30)
    fig_h.update_traces(text=ct.values, texttemplate="%{text:,}")
    st.plotly_chart(fig_h, use_container_width=True)

    st.markdown("""
    <div class="card card--bordered-coral">
        <h4>🔍 Interpretación</h4>
        <p>Las concentraciones más intensas revelan las <strong>rutas y patrones predominantes</strong>
        de la delincuencia transnacional colombiana. El narcotráfico domina en países americanos mientras
        que en Europa hay más diversidad de delitos.</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # 9. ESTADÍSTICAS DESCRIPTIVAS
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📈", "Estadísticas Descriptivas", "blue"), unsafe_allow_html=True)

    if "CANTIDAD" in df.columns:
        s1,s2,s3,s4 = st.columns(4)
        q = df["CANTIDAD"]
        with s1: st.metric("Media", f"{q.mean():.2f}")
        with s2: st.metric("Mediana", f"{q.median():.0f}")
        with s3: st.metric("Desv. Estándar", f"{q.std():.2f}")
        with s4: st.metric("Suma Total", f"{q.sum():,}")

    with st.expander("📋 Tabla de estadísticas descriptivas completa"):
        st.dataframe(df.describe(include="all").T, use_container_width=True)

    # ══════════════════════════════════════════════
    # 10. CONCLUSIONES
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🎓", "Conclusiones del EDA", "violet"), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card card--bordered-violet">
        <h4>Hallazgos principales</h4>
        <ul>
            <li><strong class="text-teal">Escala:</strong> {df.shape[0]:,} casos en {df[pais_col].nunique()} países</li>
            <li><strong class="text-teal">Concentración:</strong> Venezuela, EE.UU. y Ecuador lideran las detenciones</li>
            <li><strong class="text-teal">Tipología:</strong> Narcotráfico predominante, seguido de robo/hurto y homicidio</li>
            <li><strong class="text-teal">Demografía:</strong> ~79 % masculino, mayoría adultos</li>
            <li><strong class="text-teal">Jurídica:</strong> Mayoría condenados o en investigación</li>
            <li><strong class="text-teal">Calidad:</strong> Variables críticas al 100 % de completitud</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ No se pudo cargar el dataset.")

# Sidebar
st.sidebar.markdown("### 🔍 Análisis Exploratorio")
st.sidebar.markdown("10 secciones con gráficos interactivos Plotly sobre el dataset completo.")
sidebar_nav()
