import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="EDA - Colombianos Detenidos en el Exterior", layout="wide")

st.title("🔍 Análisis Exploratorio de Datos: Colombianos Detenidos en el Exterior")
st.markdown("""
### Objetivo del Proyecto
Este análisis explora el dataset de **colombianos detenidos en el exterior** con el propósito de comprender los patrones de delincuencia transnacional, identificar países de mayor incidencia y contribuir al diseño de políticas públicas informadas en criminología internacional.
""")

# --- Barra Lateral con Contexto Teórico ---
st.markdown("""
   Este dataset contiene información sobre colombianos detenidos en países extranjeros. 
   Es un registro estadístico de delincuencia transnacional y movilidad criminal.
   
   ### Importancia
   - **Criminología**: Entender patrones de delincuencia internacional
   - **Geopolítica**: Identificar regiones con mayor incidencia
   - **Política Pública**: Diseñar estrategias de prevención y repatriación
   
   ### Variables esperadas
   - País de detención
   - Tipo de delito
   - Género y edad
   - Características demográficas
   - Información legal y sentencias
   """)

# --- 1. Carga de Datos ---
@st.cache_data
def load_data():
   try:
       csv_path = os.path.join(os.path.dirname(__file__), "..", "src", "data", "Colombianos_detenidos_en_el_exterior_20260309.csv")
       return pd.read_csv(csv_path, encoding='utf-8')
   except UnicodeDecodeError:
       return pd.read_csv(csv_path, encoding='latin-1')
   except Exception as e:
       st.error(f"Error al cargar el archivo: {e}")
       return None

# Carga automática del dataset
df = load_data()

if df is not None:
   # Clasificación de variables
   num_cols = df.select_dtypes(include=['number']).columns.tolist()
   cat_cols = df.select_dtypes(include=['object']).columns.tolist()
   date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
   
   # --- Paso 1: Primer Impacto ---
   st.header("Step 1: 🔍 Primer Impacto (Dataset Preview)")
   st.markdown("Observa las primeras filas. ¿Qué conceptos o palabras clave se repiten?")
   st.dataframe(df.head(10))
   
   with st.expander("💡 ¿Cómo interpretar este paso?"):
       st.write("""
       - **Nombres de Columnas:** Son las 'etiquetas' de la información. Si ves 'Municipio', sabes que hay datos geográficos. Si ves 'Fecha', hay una línea de tiempo.
       - **Valores Iniciales:** Te dan una idea del formato. ¿Son números decimales, enteros, o texto largo?
       - **Identificadores:** Busca columnas como 'ID' o 'Código', suelen ser llaves únicas para cada registro.
       """)

   # --- Paso 2: La Estructura ---
   st.header("Step 2: 🏗️ La Estructura")
   col1, col2, col3 = st.columns(3)
   with col1:
       st.subheader(f"🔢 Variables Numéricas ({len(num_cols)})")
       if num_cols:
           for col in num_cols[:5]:
               st.write(f"• {col}")
           if len(num_cols) > 5:
               st.write(f"... y {len(num_cols) - 5} más")
       else:
           st.write("Ninguna")
   
   with col2:
       st.subheader(f"📝 Variables Categóricas ({len(cat_cols)})")
       if cat_cols:
           for col in cat_cols[:5]:
               st.write(f"• {col}")
           if len(cat_cols) > 5:
               st.write(f"... y {len(cat_cols) - 5} más")
       else:
           st.write("Ninguna")
   
   with col3:
       st.subheader(f"📅 Variables Temporales ({len(date_cols)})")
       if date_cols:
           for col in date_cols:
               st.write(f"• {col}")
       else:
           st.write("Ninguna")
   
   # === SECCIÓN 3: TEORÍA DE ANÁLISIS DE DATOS CRIMINALES ===
   st.header("🔬 3. Teoría: Análisis de Datos Criminales Internacionales")
   
   st.markdown("""
   ### 3.1 Conceptos Clave en Criminología
   
   **Delito Transnacional:**
   Acciones ilícitas que cruzan fronteras nacionales o que son cometidas en jurisdicciones extranjeras.
   Los datos permiten identificar:
   - Patrones de movilidad de delincuentes
   - Cooperación entre sistemas judiciales
   - Vulnerabilidades en controles fronterizos
   
   **Distribución Geográfica:**
   Los países de detención varían según:
   - Proximidad geográfica a Colombia
   - Rutas tradicionales de tráfico
   - Nivel de aplicación de la ley
   - Acuerdos de cooperación internacional
   
   **Tipología Criminal:**
   Los tipos de delitos registrados reflejan:
   - Delincuencia organizada (narcotráfico, tráfico de personas)
   - Delitos convencionales (robo, asalto)
   - Fraudes y delitos financieros
   - Delitos contra la integridad personal
   """)
   

   # === SECCIÓN 4: DISTRIBUCIONES Y PATRONES ===
   st.header("📊 4. Distribuciones y Patrones Clave")
   
   if len(cat_cols) > 0:
       selected_col = st.selectbox(
           "Selecciona una variable para explorar:",
           cat_cols
       )
       
       value_counts = df[selected_col].value_counts().head(15)
       
       st.markdown(f"#### Distribución de {selected_col}")
       
       # Mostrar en tabla
       distribution_df = pd.DataFrame({
           'Categoría': value_counts.index,
           'Registros': value_counts.values,
           '% del Total': (value_counts.values / value_counts.sum() * 100).round(2)
       }).reset_index(drop=True)
       
       st.dataframe(distribution_df, use_container_width=True)
       
       # Información resumida
       col1, col2, col3 = st.columns(3)
       with col1:
           st.metric("Valor más frecuente", value_counts.index[0])
       with col2:
           st.metric("Casos del top valor", f"{value_counts.values[0]:,}")
       with col3:
           st.metric("Categorías totales", len(value_counts))
   
   # === SECCIÓN 5: CONCLUSIONES TEÓRICAS ===
   st.header("🎓 5. Conclusiones del Análisis Exploratorio")
   
   st.markdown(f"""
   ### Hallazgos Teóricos
   
   **Escala del Fenómeno:**
   Este dataset registra **{df.shape[0]:,} casos** de ciudadanos colombianos detenidos en el exterior.
   Esta cifra es significativa para:
   - Comprender la magnitud real de la delincuencia transnacional
   - Evaluar el impacto de políticas públicas
   - Estimar recursos necesarios para cooperación internacional
   
   **Complejidad de Variables:**
   Con **{df.shape[1]} variables** documentadas, el registro es:
   - **Multidimensional:** Captura múltiples aspectos del caso (legal, demográfico, geográfico)
   - **Holistico:** Permite análisis desde varias perspectivas criminológicas
   - **Robusto:** Suficientemente detallado para investigaciones profundas
   
   **Implicaciones para Investigación:**
   Este dataset permite responder preguntas de criminología como:
   ✓ ¿En qué países se concentra la detención de colombianos?
   ✓ ¿Qué tipos de delitos son más comunes internacionalmente?
   ✓ ¿Hay perfiles demográficos predictivos en delincuencia transnacional?
   ✓ ¿Cómo han evolucionado los patrones con el tiempo?
   """)
   
else:
   st.error("❌ No se pudo cargar el dataset. Verifica la ruta del archivo.")