import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys, re

st.set_page_config(page_title="Análisis Demográfico · CDE-AC", layout="wide", page_icon="👤")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.design import (inject_css, section_header, kpi_tile, sidebar_nav,
                         CHART_COLORS, SCALE_GOLD, SCALE_TEAL, SCALE_CORAL, apply_layout)

st.markdown(inject_css(), unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        p = os.path.join(os.path.dirname(__file__), "..", "src", "data",
                         "Colombianos_detenidos_en_el_exterior_20260309.csv")
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
    sit_col, genero_col, edad_col, fecha_col = cols[5], cols[6], cols[7], cols[0]

    total = len(df)
    masc = (df[genero_col]=="MASCULINO").sum()
    fem = (df[genero_col]=="FEMENINO").sum()
    adulto = (df[edad_col]=="ADULTO").sum()

    st.markdown("""
    <p class="page-eyebrow">Módulo 4</p>
    <p class="page-title">Análisis <em>Demográfico</em></p>
    <p class="page-desc">Perfiles criminológicos basados en género, edad y características demográficas de los detenidos.</p>
    """, unsafe_allow_html=True)

    # KPIs
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    k1,k2,k3,k4 = st.columns(4)
    with k1: st.markdown(kpi_tile(f"{masc:,}", "Masculino", f"{masc/total*100:.1f} %"), unsafe_allow_html=True)
    with k2: st.markdown(kpi_tile(f"{fem:,}", "Femenino", f"{fem/total*100:.1f} %"), unsafe_allow_html=True)
    with k3: st.markdown(kpi_tile(f"{adulto:,}", "Adultos", f"{adulto/total*100:.1f} %"), unsafe_allow_html=True)
    with k4: st.markdown(kpi_tile(f"{masc/fem:.1f}:1" if fem else "—", "Ratio M:F", "Proporción"), unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # 1. GÉNERO
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("👫", "Análisis por Género"), unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        gc = df[genero_col].value_counts()
        fig = px.pie(values=gc.values, names=gc.index, hole=0.5,
                     color_discrete_sequence=["#58a6ff","#f472b6","#a78bfa","#e8a838","#3fb9a0"])
        apply_layout(fig, height=380, title="Distribución por género")
        fig.update_traces(textinfo="percent+label", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with g2:
        df["_y"] = pd.to_datetime(df[fecha_col], errors="coerce").dt.year
        gy = df[df[genero_col].isin(["MASCULINO","FEMENINO"])].groupby(["_y",genero_col]).size().reset_index(name="n")
        gy.columns = ["Año","Género","Registros"]
        gy = gy.dropna(subset=["Año"]); gy["Año"] = gy["Año"].astype(int)
        fig = px.line(gy, x="Año", y="Registros", color="Género", markers=True,
                      color_discrete_map={"MASCULINO":"#58a6ff","FEMENINO":"#f472b6"})
        apply_layout(fig, height=380, title="Evolución temporal por género")
        st.plotly_chart(fig, use_container_width=True)

    # Género por país
    st.markdown("#### Distribución de género por país (Top 8)")
    t8 = df[~df[pais_col].isin(["DESCONOCIDO","EXTRADICION"])][pais_col].value_counts().head(8).index.tolist()
    gp = df[(df[pais_col].isin(t8))&(df[genero_col].isin(["MASCULINO","FEMENINO"]))]
    gpg = gp.groupby([pais_col,genero_col]).size().reset_index(name="n")
    gpg.columns = ["País","Género","Registros"]
    fig = px.bar(gpg, x="País", y="Registros", color="Género", barmode="group",
                 color_discrete_map={"MASCULINO":"#58a6ff","FEMENINO":"#f472b6"})
    apply_layout(fig, height=380, title="", xaxis_tickangle=-20)
    st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════════════
    # 2. EDAD
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📊", "Análisis por Grupo de Edad", "teal"), unsafe_allow_html=True)

    e1, e2 = st.columns(2)
    with e1:
        order = ["ADOLESCENTE", "ADULTO JOVEN", "ADULTO", "ADULTO MAYOR"]
        ec = df[df[edad_col].isin(order)][edad_col].value_counts().reindex(order).dropna()
        fig = px.bar(x=ec.values, y=ec.index, orientation="h",
                     labels={"x": "Registros", "y": ""},
                     color=ec.values, color_continuous_scale=SCALE_TEAL)
        apply_layout(fig, height=320, title="Distribución por grupo de edad", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with e2:
        ed = df[(df[edad_col].isin(["ADOLESCENTE","ADULTO JOVEN","ADULTO","ADULTO MAYOR"]))
                & (df[delito_col]!="DESCONOCIDO")]
        t5d = ed[delito_col].value_counts().head(5).index.tolist()
        edg = ed[ed[delito_col].isin(t5d)].groupby([edad_col, delito_col]).size().reset_index(name="n")
        edg.columns = ["Edad", "Delito", "Registros"]
        fig = px.bar(edg, x="Registros", y="Edad", color="Delito", barmode="stack",
                     orientation="h", color_discrete_sequence=CHART_COLORS)
        apply_layout(fig, height=340, title="Delitos por grupo de edad")
        fig.update_xaxes(tickangle=0)
        st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════════════
    # 3. PERFILES CRIMINOLÓGICOS
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🔬", "Perfiles Criminológicos", "violet"), unsafe_allow_html=True)

    st.markdown("""
    <div class="card card--bordered-violet">
        <h4>Construcción de perfiles</h4>
        <p>Combinación de género + grupo de edad + tipo de delito para identificar los perfiles 
        más frecuentes en delincuencia transnacional colombiana.</p>
    </div>
    """, unsafe_allow_html=True)

    pf = df[(~df[genero_col].isin(["DESCONOCIDO","OTRO","NO_BINARIO"]))&
            (df[edad_col]!="DESCONOCIDO")&(df[delito_col]!="DESCONOCIDO")]
    profiles = pf.groupby([genero_col,edad_col,delito_col]).size().reset_index(name="Registros")
    profiles.columns = ["Género","Edad","Delito","Registros"]
    profiles = profiles.sort_values("Registros", ascending=False).head(15)
    profiles["% Total"] = (profiles["Registros"]/len(df)*100).round(2)
    profiles = profiles.reset_index(drop=True)
    profiles.index = profiles.index + 1
    st.dataframe(profiles, use_container_width=True)

    # Chart
    top10 = profiles.head(10).copy()
    top10["Perfil"] = top10.apply(lambda r: f"{r['Género'][:3]} · {r['Edad']} · {r['Delito']}", axis=1)
    fig = px.bar(top10, x="Registros", y="Perfil", orientation="h",
                 color="Registros", color_continuous_scale=SCALE_GOLD)
    apply_layout(fig, height=420, title="Top 10 perfiles criminológicos",
                 yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════════════
    # 4. SITUACIÓN JURÍDICA × GÉNERO
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("⚖️", "Situación Jurídica por Género", "coral"), unsafe_allow_html=True)

    def simp(s):
        u=str(s).upper()
        if "CONDENADO" in u: return "Condenado"
        if "INVESTIGACI" in u: return "Investigación"
        if "JUICIO" in u: return "En juicio"
        if "DEPORTACI" in u: return "Deportación"
        if "EXTRADITADO" in u: return "Extraditado"
        return "Otro"

    ds = df[df[genero_col].isin(["MASCULINO","FEMENINO"])].copy()
    ds["Sit"] = ds[sit_col].apply(simp)
    sg = ds.groupby([genero_col,"Sit"]).size().reset_index(name="n")
    sg.columns = ["Género","Situación","Registros"]
    tots = sg.groupby("Género")["Registros"].sum()
    sg["%"] = sg.apply(lambda r: round(r["Registros"]/tots[r["Género"]]*100,1), axis=1)

    fig = px.bar(sg, x="Situación", y="%", color="Género", barmode="group", text="%",
                 color_discrete_map={"MASCULINO":"#58a6ff","FEMENINO":"#f472b6"})
    apply_layout(fig, height=400, title="Distribución jurídica por género (%)", xaxis_tickangle=-35)
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════════════
    # 5. EXPLORADOR POR PAÍS
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🌍", "Perfil Demográfico por País", "blue"), unsafe_allow_html=True)

    options = df[~df[pais_col].isin(["DESCONOCIDO","EXTRADICION"])][pais_col].value_counts().head(20).index.tolist()
    sel = st.selectbox("Selecciona un país:", options)
    pd_ = df[df[pais_col]==sel]

    c1,c2,c3 = st.columns(3)
    with c1:
        vg = pd_[genero_col].value_counts()
        fig = px.pie(values=vg.values, names=vg.index, hole=0.45,
                     color_discrete_sequence=["#58a6ff","#f472b6","#a78bfa","#e8a838"])
        apply_layout(fig, height=330, title=f"Género — {sel}")
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        ve = pd_[edad_col].value_counts()
        fig = px.pie(values=ve.values, names=ve.index, hole=0.45,
                     color_discrete_sequence=CHART_COLORS)
        apply_layout(fig, height=330, title=f"Edad — {sel}")
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        vd = pd_[delito_col].value_counts().head(6)
        fig = px.bar(x=vd.values, y=vd.index, orientation="h",
                     color=vd.values, color_continuous_scale=SCALE_GOLD)
        apply_layout(fig, height=330, title=f"Delitos — {sel}",
                     yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    pm1,pm2,pm3,pm4 = st.columns(4)
    with pm1: st.metric("Registros", f"{len(pd_):,}")
    with pm2: st.metric("% Masculino", f"{(pd_[genero_col]=='MASCULINO').sum()/len(pd_)*100:.1f}%")
    with pm3: st.metric("Delito principal", pd_[delito_col].value_counts().index[0])
    with pm4: st.metric("Edad predominante", pd_[edad_col].value_counts().index[0])

    # ══════════════════════════════════════════════
    # CONCLUSIONES
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📌", "Conclusiones Demográficas", "teal"), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card card--bordered-teal">
        <h4>Hallazgos clave</h4>
        <ul>
            <li><strong class="text-blue">Género:</strong> {masc/total*100:.1f} % masculino (ratio {masc/fem:.1f}:1). 
            Participación femenina es mayor en narcotráfico que en otros delitos.</li>
            <li><strong class="text-coral">Edad:</strong> "Adulto" domina con {adulto/total*100:.1f} %. 
            Los menores son una proporción mínima pero preocupante.</li>
            <li><strong class="text-violet">Perfiles:</strong> El más frecuente es hombre adulto en narcotráfico.</li>
            <li><strong class="text-teal">Jurídica:</strong> Distribución similar entre géneros, mayoría condenados.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ No se pudo cargar el dataset.")

st.sidebar.markdown("### 👤 Análisis Demográfico")
st.sidebar.markdown("Género, edad, perfiles criminológicos y explorador interactivo por país.")
sidebar_nav()
