import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys, re, re

st.set_page_config(page_title="Visualizaciones · CDE-AC", layout="wide", page_icon="🗺️")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.design import (inject_css, section_header, sidebar_nav,
                         CHART_COLORS, SCALE_GOLD, SCALE_TEAL, SCALE_CORAL, apply_layout)

st.markdown(inject_css(), unsafe_allow_html=True)

COUNTRY_ISO = {
    'VENEZUELA':'VEN','ESTADOS UNIDOS':'USA','ECUADOR':'ECU','ESPAÑA':'ESP',
    'CHILE':'CHL','MEXICO':'MEX','PANAMA':'PAN','PERU':'PER','BRASIL':'BRA',
    'REPUBLICA DOMINICANA':'DOM','COSTA RICA':'CRI','BOLIVIA':'BOL','ARGENTINA':'ARG',
    'CHINA':'CHN','ALEMANIA':'DEU','FRANCIA':'FRA','ITALIA':'ITA','CANADA':'CAN',
    'GUATEMALA':'GTM','HONDURAS':'HND','EL SALVADOR':'SLV','NICARAGUA':'NIC',
    'PARAGUAY':'PRY','URUGUAY':'URY','HOLANDA':'NLD','PORTUGAL':'PRT',
    'REINO UNIDO':'GBR','JAPON':'JPN','AUSTRALIA':'AUS','TRINIDAD Y TOBAGO':'TTO',
    'JAMAICA':'JAM','HAITI':'HTI','CUBA':'CUB','TAILANDIA':'THA','RUSIA':'RUS',
    'TURQUIA':'TUR','INDIA':'IND','INDONESIA':'IDN','MALASIA':'MYS',
    'ISRAEL':'ISR','SUIZA':'CHE','BELGICA':'BEL','SUDAFRICA':'ZAF',
    'ARUBA':'ABW','CURAZAO':'CUW','NIGERIA':'NGA','KENIA':'KEN',
}

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
    pais_col, consulado_col, delito_col = cols[1], cols[2], cols[3]
    extrad_col, sit_col, genero_col, edad_col, fecha_col = cols[4], cols[5], cols[6], cols[7], cols[0]

    st.markdown("""
    <p class="page-eyebrow">Módulo 3</p>
    <p class="page-title">Visualizaciones <em>Avanzadas</em></p>
    <p class="page-desc">Análisis visual de alto nivel — mapas, treemaps, sunbursts y tendencias interactivas.</p>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # 1. MAPA MUNDIAL
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🌎", "Mapa Mundial de Detenciones", "blue"), unsafe_allow_html=True)

    pm = df[df[pais_col]!="DESCONOCIDO"].groupby(pais_col).size().reset_index(name="Registros")
    pm.columns = ["Pais","Registros"]
    pm["ISO"] = pm["Pais"].map(COUNTRY_ISO)
    pm = pm.dropna(subset=["ISO"])

    fig_map = px.choropleth(pm, locations="ISO", color="Registros", hover_name="Pais",
                            color_continuous_scale=SCALE_GOLD, projection="natural earth")
    apply_layout(fig_map, height=520, title="Distribución global de colombianos detenidos",
                 geo=dict(bgcolor="rgba(0,0,0,0)", landcolor="#151a25",
                          oceancolor="#0b0e14", showocean=True, showlakes=False,
                          coastlinecolor="#1e2430", countrycolor="#1e2430"),
                 coloraxis_showscale=True)
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("""
    <div class="card card--bordered-blue">
        <h4>🌍 Interpretación geográfica</h4>
        <p>Se observa <strong class="text-gold">concentración en el continente americano</strong>, 
        especialmente en países vecinos y centros de narcotráfico internacional. 
        La proximidad geográfica y las rutas de tráfico son factores determinantes.</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # 2. TREEMAP
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🌳", "Treemap: País → Delito", "teal"), unsafe_allow_html=True)

    tp = df[~df[pais_col].isin(["DESCONOCIDO","EXTRADICION"])][pais_col].value_counts().head(8).index.tolist()
    td = df[~df[delito_col].isin(["DESCONOCIDO"])][delito_col].value_counts().head(6).index.tolist()
    tdf = df[df[pais_col].isin(tp) & df[delito_col].isin(td)]
    tg = tdf.groupby([pais_col, delito_col]).size().reset_index(name="Registros")
    tg.columns = ["País","Delito","Registros"]

    fig_tree = px.treemap(tg, path=["País","Delito"], values="Registros",
                          color="Registros", color_continuous_scale=SCALE_TEAL)
    apply_layout(fig_tree, height=520, title="Distribución jerárquica País → Delito")
    st.plotly_chart(fig_tree, use_container_width=True)

    # ══════════════════════════════════════════════
    # 3. SUNBURST
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("☀️", "Sunburst: Género → Edad → Situación", "violet"), unsafe_allow_html=True)

    def simplify_sit(s):
        u = str(s).upper()
        if "CONDENADO" in u: return "Condenado"
        if "INVESTIGACI" in u: return "Investigación"
        if "JUICIO" in u: return "En juicio"
        if "DEPORTACI" in u: return "Deportación"
        if "EXTRADITADO" in u: return "Extraditado"
        return "Otro"

    sdf = df[(df[genero_col].isin(["MASCULINO","FEMENINO"])) & (df[edad_col]!="DESCONOCIDO")].copy()
    sdf["Sit"] = sdf[sit_col].apply(simplify_sit)
    sg = sdf.groupby([genero_col, edad_col, "Sit"]).size().reset_index(name="Registros")
    sg.columns = ["Género","Edad","Situación","Registros"]

    fig_sun = px.sunburst(sg, path=["Género","Edad","Situación"], values="Registros",
                          color="Registros", color_continuous_scale=SCALE_GOLD)
    apply_layout(fig_sun, height=560, title="Estructura demográfica y jurídica (clic para explorar)")
    st.plotly_chart(fig_sun, use_container_width=True)

    # ══════════════════════════════════════════════
    # 4. TEMPORAL POR PAÍS
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📅", "Evolución Temporal por País"), unsafe_allow_html=True)

    df["_y"] = pd.to_datetime(df[fecha_col], errors="coerce").dt.year
    t5 = df[~df[pais_col].isin(["DESCONOCIDO","EXTRADICION"])][pais_col].value_counts().head(5).index.tolist()
    tpdf = df[df[pais_col].isin(t5)].groupby(["_y", pais_col]).size().reset_index(name="Registros")
    tpdf.columns = ["Año","País","Registros"]
    tpdf = tpdf.dropna(subset=["Año"])
    tpdf["Año"] = tpdf["Año"].astype(int)

    fig_tl = px.line(tpdf, x="Año", y="Registros", color="País", markers=True,
                     color_discrete_sequence=CHART_COLORS)
    apply_layout(fig_tl, height=420, title="Evolución de detenciones — Top 5 países")
    st.plotly_chart(fig_tl, use_container_width=True)

    # ══════════════════════════════════════════════
    # 5. TEMPORAL POR DELITO
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("📈", "Tendencia Temporal por Delito", "coral"), unsafe_allow_html=True)

    t5d = df[~df[delito_col].isin(["DESCONOCIDO"])][delito_col].value_counts().head(5).index.tolist()
    tddf = df[df[delito_col].isin(t5d)].groupby(["_y", delito_col]).size().reset_index(name="Registros")
    tddf.columns = ["Año","Delito","Registros"]
    tddf = tddf.dropna(subset=["Año"])
    tddf["Año"] = tddf["Año"].astype(int)

    fig_td = px.area(tddf, x="Año", y="Registros", color="Delito",
                     color_discrete_sequence=CHART_COLORS)
    apply_layout(fig_td, height=420, title="Evolución de los principales delitos")
    st.plotly_chart(fig_td, use_container_width=True)

    # ══════════════════════════════════════════════
    # 6. CONSULADOS
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🏛️", "Top Consulados", "teal"), unsafe_allow_html=True)

    cc = df[consulado_col].value_counts().head(15)
    fig_c = px.bar(x=cc.values, y=cc.index, orientation="h",
                   labels={"x":"Registros","y":""},
                   color=cc.values, color_continuous_scale=SCALE_TEAL)
    apply_layout(fig_c, height=480, title="15 consulados con mayor número de casos",
                 yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_c, use_container_width=True)

    # ══════════════════════════════════════════════
    # 7. EXTRADICIÓN
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("✈️", "Extradición y Repatriación", "coral"), unsafe_allow_html=True)

    ce1, ce2 = st.columns(2)
    with ce1:
        ec = df[extrad_col].value_counts()
        fig_ex = px.pie(values=ec.values, names=ec.index, hole=0.45,
                        color_discrete_sequence=CHART_COLORS)
        apply_layout(fig_ex, height=380, title="Estado de extradición / repatriación")
        fig_ex.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_ex, use_container_width=True)
    with ce2:
        edf = df[df[extrad_col].str.contains("EXTRADICION", case=False, na=False)]
        ep = edf[~edf[pais_col].isin(["EXTRADICION"])][pais_col].value_counts().head(10)
        fig_ep = px.bar(x=ep.index, y=ep.values, labels={"x":"","y":"Extradiciones"},
                        color=ep.values, color_continuous_scale=SCALE_CORAL)
        apply_layout(fig_ep, height=380, title="Top 10 países con más extradiciones",
                     xaxis_tickangle=-30)
        st.plotly_chart(fig_ep, use_container_width=True)

    # ══════════════════════════════════════════════
    # 8. GÉNERO × DELITO
    # ══════════════════════════════════════════════
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown(section_header("🔗", "Análisis Cruzado: Género × Delito", "violet"), unsafe_allow_html=True)

    td8 = df[~df[delito_col].isin(["DESCONOCIDO"])][delito_col].value_counts().head(8).index.tolist()
    gd = df[(df[genero_col].isin(["MASCULINO","FEMENINO"])) & (df[delito_col].isin(td8))]
    gdg = gd.groupby([delito_col, genero_col]).size().reset_index(name="Registros")
    gdg.columns = ["Delito","Género","Registros"]

    fig_gd = px.bar(gdg, x="Delito", y="Registros", color="Género", barmode="group",
                    color_discrete_map={"MASCULINO":"#58a6ff","FEMENINO":"#f472b6"})
    apply_layout(fig_gd, height=430, title="Distribución de delitos por género",
                 xaxis_tickangle=-30)
    st.plotly_chart(fig_gd, use_container_width=True)

    st.markdown("""
    <div class="card card--bordered-violet">
        <h4>Observaciones</h4>
        <ul>
            <li>Narcotráfico es predominante en ambos géneros</li>
            <li>La proporción femenina es mayor en narcotráfico vs. otros delitos</li>
            <li>Delitos sexuales y homicidio son predominantemente masculinos</li>
            <li>El patrón sugiere roles diferenciados dentro de organizaciones criminales</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ No se pudo cargar el dataset.")

st.sidebar.markdown("### 🗺️ Visualizaciones Avanzadas")
st.sidebar.markdown("Mapas, treemaps, sunbursts y tendencias temporales interactivas.")
sidebar_nav()
