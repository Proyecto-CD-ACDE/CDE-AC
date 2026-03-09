# 📊 Análisis Exploratorio de Datos (EDA) - Colombianos Detenidos en el Exterior

## Introducción

Este proyecto es una **aplicación web interactiva** desarrollada en equipo que permite realizar un Análisis Exploratorio de Datos (EDA) sobre un conjunto de datos seleccionado. 

**Objetivo General:** Desarrollar una herramienta que facilite la visualización, exploración y análisis de datos de manera intuitiva, documentar los hallazgos y desplegar el código en GitHub para colaboración y transparencia.

### Tecnologías Utilizadas
- **Python 3.8+** - Lenguaje de programación principal
- **Pandas** - Manipulación y análisis de datos
- **Streamlit** - Framework para crear la aplicación web interactiva
- **Entorno Virtual (venv)** - Aislamiento de dependencias del proyecto

---

## 🚀 Instrucciones para Iniciar el Proyecto

#### 1. Crear carpeta del proyecto

```bash
mkdir proyecto_analitica
cd proyecto_analitica
```

#### 2. Crear entorno virtual

```bash
python -m venv .venv
```

#### 3. Activar entorno virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

#### 4. Instalar dependencias principales

```bash
pip install streamlit pandas
pip freeze > requirements.txt
```

---

### Fase 2: Estructura del Proyecto

El proyecto debe seguir la siguiente estructura de carpetas para habilitar la navegación multipágina de Streamlit:

```
proyecto_analitica/
├── inicio.py                           # Página de inicio (portada)
├── pages/
│   ├── 1_Análisis_Exploratorio_de_Datos_(EDA).py  # Módulo de Análisis
│   └── 2_Resultados_(EDA).py          # Pantalla de entrega
├── data/                              # (Opcional) Carpeta para el dataset CSV
├── .gitignore                         # Archivos que git debe ignorar
└── requirements.txt                   # Lista de librerías necesarias
```

---

### Fase 3: Primeros Pasos para Otros Integrantes

Una vez que el líder haya inicializado el repositorio en GitHub:

#### 1. Clonar el repositorio

```bash
git clone <URL-DEL-REPOSITORIO>
cd proyecto_analitica
```

#### 2. Crear y activar entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# o
source .venv/bin/activate  # macOS/Linux
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Ejecutar la aplicación

```bash
streamlit run inicio.py
```

---

### Fase 4: Ejecución de la Aplicación

Una vez configurado el entorno, para ejecutar la aplicación interactiva:

```bash
streamlit run inicio.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

---

## 📋 Checklist de Inicio

- [ ] Repositorio creado en GitHub
- [ ] Entorno virtual configurado
- [ ] Dependencias instaladas (pandas, streamlit)
- [ ] `requirements.txt` generado
- [ ] Estructura de carpetas creada
- [ ] Archivo `inicio.py` creado
- [ ] Carpeta `pages/` creada con módulos
- [ ] `.gitignore` configurado
- [ ] Primer commit realizado
- [ ] Aplicación ejecutándose correctamente

---

## 💡 Notas Importantes

- Asegúrate de estar en el entorno virtual antes de instalar paquetes
- Usa `requirements.txt` para mantener las dependencias consistentes entre desarrolladores
- Commit regularmente los cambios en Git
- Documenta hallazgos importantes en los comentarios del código

¡A trabajar! 🎯
