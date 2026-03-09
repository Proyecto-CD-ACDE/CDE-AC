import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(
   page_title="Resultados EDA - Colombianos Detenidos en el Exterior",
   page_icon="📊",
   layout="wide"
)

st.title("📊 Resultados: Análisis Exploratorio de Datos Criminales")
st.markdown("""
### Reporte de Hallazgos
Este documento consolida los hallazgos del análisis exploratorio sobre **colombianos detenidos en el exterior**. 
Utiliza los datos observados en la página de Análisis Exploratorio para completar cada sección.
""")

st.divider()

# ─────────────────────────────────────────────────────────────────
# CARGAR DATOS PARA REFERENCIA
# ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "..", "src", "data", "Colombianos_detenidos_en_el_exterior_20260309.csv")
        return pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(csv_path, encoding='latin-1')
    except:
        return None

df = load_data()

# ─────────────────────────────────────────────────────────────────
# INFORMACIÓN DE REFERENCIA
# ─────────────────────────────────────────────────────────────────
if df is not None:
    st.info(f"""
    📌 **DATOS DE REFERENCIA:**
    - Total de registros: **{df.shape[0]:,}**
    - Variables documentadas: **{df.shape[1]}**
    - Período: Registros históricos de colombianos detenidos en el exterior
    """)

# --- Formulario de Resultados ---
with st.container():
   st.header("🔍 1. Identificación y Contexto del Dataset")
   contexto = st.text_area(
       "¿De qué se trata el dataset? (Deducción del origen, tema y propósito)",
       placeholder="El dataset trata sobre el registro histórico de ciudadanos colombianos detenidos en países extranjeros. Su propósito es documentar la magnitud de la delincuencia transnacional, identificar patrones geográficos y tipos de delitos, y fundamentar políticas públicas en cooperación internacional y repatriación.",
       value="El dataset trata sobre el registro histórico de ciudadanos colombianos detenidos en países extranjeros. Su propósito es documentar la magnitud de la delincuencia transnacional, identificar patrones geográficos y tipos de delitos, y fundamentar políticas públicas en cooperación internacional y repatriación.",
       height=150
   )

   st.header("❗ 2. Calidad de los Datos y Datos Faltantes")
   calidad = st.text_area(
       "¿Qué encontraste sobre los datos faltantes y la limpieza?",
       placeholder="Se identificaron datos faltantes principalmente en: UBICACIÓN PAÍS (68.6% faltante - 266,321 registros), LATITUD (13.6% faltante) y LONGITUD (13.6% faltante). Sin embargo, las variables críticas como País de Prisión, Delito, Género, Edad y Situación Jurídica están 100% completas. Los datos faltantes en ubicación geográfica sugieren restricciones por privacidad o falta de información en registros históricos, pero no afecta el análisis de patrones criminales.",
       value="Se identificaron datos faltantes principalmente en: UBICACIÓN PAÍS (68.6% faltante - 266,321 registros), LATITUD (13.6% faltante) y LONGITUD (13.6% faltante). Sin embargo, las variables críticas como País de Prisión, Delito, Género, Edad y Situación Jurídica están 100% completas. Los datos faltantes en ubicación geográfica sugieren restricciones por privacidad o falta de información en registros históricos, pero no afecta el análisis de patrones criminales.",
       height=180
   )

   st.header("📈 3. Hallazgos Estadísticos Clave")
   estadisticas = st.text_area(
       "Interpretación de los números y categorías principales (Modas, concentraciones, patrones)",
       placeholder="Del análisis de principales variables categóricas: el País de Prisión muestra concentración en economías avanzadas (probable relación con narcotráfico). El Delito evidencia predominancia de crímenes específicos concentrados en pocas categorías. Por Género se observa una distribución que refleja perfiles delictivos. La Situación Jurídica muestra estados legales diversos. La distribución es altamente concentrada en pocas categorías, indicando que la delincuencia transnacional colombiana sigue patrones específicos y no es aleatoria.",
       value="Del análisis de principales variables categóricas: el País de Prisión muestra concentración en economías avanzadas (probable relación con narcotráfico). El Delito evidencia predominancia de crímenes específicos concentrados en pocas categorías. Por Género se observa una distribución que refleja perfiles delictivos. La Situación Jurídica muestra estados legales diversos. La distribución es altamente concentrada en pocas categorías, indicando que la delincuencia transnacional colombiana sigue patrones específicos y no es aleatoria.",
       height=180
   )

   st.header("💡 4. Conclusiones Finales")
   conclusion = st.text_area(
       "¿Cuál es el mensaje principal que nos dan estos datos?",
       placeholder="El dataset revela que la delincuencia transnacional de colombianos es un fenómeno estructurado y concentrado: (1) Existe una magnitud significativa (388,148 casos) que documenta un problema sistemático; (2) Los patrones no son aleatorios sino concentrados geográfica y tipológicamente; (3) La data quality es robusta en variables críticas lo que permite análisis confiables; (4) La información es multidimensional permitiendo análisis desde perspectivas legal, demográfica y geográfica. Estos datos son fundamentales para diseñar políticas públicas informadas en cooperación internacional, repatriación y prevención de delincuencia transnacional.",
       value="El dataset revela que la delincuencia transnacional de colombianos es un fenómeno estructurado y concentrado: (1) Existe una magnitud significativa (388,148 casos) que documenta un problema sistemático; (2) Los patrones no son aleatorios sino concentrados geográfica y tipológicamente; (3) La data quality es robusta en variables críticas lo que permite análisis confiables; (4) La información es multidimensional permitiendo análisis desde perspectivas legal, demográfica y geográfica. Estos datos son fundamentales para diseñar políticas públicas informadas en cooperación internacional, repatriación y prevención de delincuencia transnacional.",
       height=150
   )

st.divider()

# --- Generación de Reporte ---
st.header("🚀 Generar Reporte Consolidado")

col1, col2 = st.columns([1, 3])
with col1:
   generar = st.button("📄 Generar Reporte", use_container_width=True)

if generar:
   if contexto and calidad and estadisticas and conclusion:
       st.success("✅ Reporte Generado Exitosamente")

       reporte_md = f"""# Reporte de Análisis Exploratorio de Datos Criminales
## Colombianos Detenidos en el Exterior

**Fecha:** {pd.Timestamp.now().strftime('%d de %B de %Y')}  
**Fuente:** Dataset CDE-AC (Colombianos Detenidos en el Exterior - Análisis Criminológico)  

---

## 📋 Resumen Ejecutivo

Este reporte consolida los hallazgos del análisis exploratorio sobre delincuencia transnacional de ciudadanos colombianos, 
basándose en {df.shape[0]:,} registros históricos y {df.shape[1]} variables documentadas.

---

## 1. Identificación y Contexto del Dataset

{contexto}

### Relevancia

- **Criminología:** Proporciona compresión de patrones de delincuencia internacional
- **Política Pública:** Base para estrategias de prevención y repatriación
- **Cooperación Internacional:** Facilita acuerdos y coordinación interinstitucional

---

## 2. Calidad de los Datos

{calidad}

### Implicaciones para el Análisis

- ✅ Análisis de delitos, países y perfiles demográficos: **CONFIABLES**
- ⚠️ Análisis espacial detallado: **LIMITADOS** (datos de ubicación incompletos)
- ✅ Análisis temporal y legal: **COMPLETO**

---

## 3. Hallazgos Estadísticos Clave

{estadisticas}

### Indicadores Principales

| Aspecto | Hallazgo |
|---------|----------|
| **Magnitud** | {df.shape[0]:,} casos documentados |
| **Concentración** | Altamente concentrada en pocas categorías |
| **Completitud** | 96%+ en variables críticas |
| **Patrón** | Estructurado, no aleatorio |

---

## 4. Conclusiones Finales

{conclusion}

### Recomendaciones

1. **Análisis Profundo:** Investigar causas raíz de concentración geográfica
2. **Políticas Informadas:** Diseñar basándose en patrones identificados
3. **Cooperación:** Fortalecer con países de detención predominantes
4. **Prevención:** Enfocarse en tipologías criminales prevalentes

---

## 📊 Metodología

- **Tipo de Análisis:** Exploratorio (EDA)
- **Dataset Principal:** Colombianos_detenidos_en_el_exterior_20260309.csv
- **Período:** Datos históricos consolidados hasta marzo 2026
- **Variables:** Clasificación automática (numéricas, categóricas, temporales)

---

*Generado por: Módulo de Análisis Exploratorio - Proyecto CDE-AC*  
*Responsable: Análisis Criminológico Internacional*
"""

       st.markdown(reporte_md)
       
       st.divider()
       
       st.download_button(
           label="📥 Descargar Reporte Completo (.md)",
           data=reporte_md,
           file_name="Reporte_EDA_Criminales_20260309.md",
           mime="text/markdown"
       )
   else:
       st.warning("⚠️ Por favor, asegúrate de que todas las secciones contengan información antes de generar.")

# --- Barra Lateral ---
   st.header("📋 Instrucciones")
   st.markdown("""
   ### Cómo usar esta página:
   
   1. **Revisa el Análisis:** Consulta la página "Análisis Exploratorio" primero
   2. **Completa Secciones:** Cada campo tiene valores predefinidos que puedes editar
   3. **Valida Datos:** Asegúrate coherencia entre hallazgos y conclusiones
   4. **Genera Reporte:** Crea documento consolidado en Markdown
   5. **Descarga:** Exporta para presentación o documentación
   
   ### Variables Clave
   - **Total Registros:** {df.shape[0]:,}
   - **Total Variables:** {df.shape[1]}
   - **Datos Completos:** Sí, en variables críticas
   - **Período:** Histórico
   """)
   st.divider()
   st.markdown("© 2026 - Proyecto CDE-AC | Criminología Internacional")