"""
Design System — CDE-AC
Shared visual language across the application.
"""

import os

DATA_FILE = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "data",
    "Colombianos_detenidos_en_el_exterior_20260309.csv"
))


def inject_css():
    """Returns the global CSS string used by every page."""
    return """
<style>
/* ───── RESET & FOUNDATION ───── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary:    #0b0e14;
    --bg-secondary:  #111620;
    --bg-card:       #151a25;
    --bg-card-hover: #1a2030;
    --border-subtle: rgba(201,209,217,0.06);
    --border-accent: rgba(232,168,56,0.25);
    
    --text-primary:   #e2e8f0;
    --text-secondary: #8b949e;
    --text-muted:     #545d68;
    
    --accent-gold:    #e8a838;
    --accent-amber:   #f0983e;
    --accent-coral:   #e06c60;
    --accent-teal:    #3fb9a0;
    --accent-blue:    #58a6ff;
    --accent-violet:  #a78bfa;
    --accent-rose:    #f472b6;
    
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    
    --shadow-glow: 0 0 24px rgba(232,168,56,0.08);
}

/* Solo aplicamos la fuente a textos comunes, no a íconos globales (*) para evitar romper ligaduras de Streamlit */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText { 
    font-family: 'Plus Jakarta Sans', sans-serif !important; 
}

.main { background: var(--bg-primary) !important; }

/* Streamlit overrides */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li { color: var(--text-secondary); font-size: 0.88rem; }

/* Corrección de métricas nativas de Streamlit para que no se crucen */
div[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 15px;
    box-sizing: border-box;
}
div[data-testid="stMetric"] label { 
    color: var(--text-secondary) !important; 
    font-size: 0.8rem !important; 
    letter-spacing: 0.5px; 
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] { 
    color: var(--accent-gold) !important; 
}
div[data-testid="stMetricValue"] > div {
    font-size: 1.4rem !important;
    white-space: pre-wrap !important;
    text-overflow: clip !important;
}

.stDataFrame { border-radius: var(--radius-md) !important; overflow: hidden; }
.stTextArea textarea { background: var(--bg-card) !important; border-color: var(--border-subtle) !important; border-radius: var(--radius-md) !important; color: var(--text-primary) !important; }
.stSelectbox > div > div { background: var(--bg-card) !important; border-color: var(--border-subtle) !important; }

button[kind="primary"], .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-gold), var(--accent-amber)) !important;
    color: #0b0e14 !important; font-weight: 600 !important;
    border: none !important; border-radius: var(--radius-md) !important;
}

.stExpander { border: 1px solid var(--border-subtle) !important; border-radius: var(--radius-md) !important; background: var(--bg-card) !important; }
.stAlert { border-radius: var(--radius-md) !important; }

/* Custom scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(232,168,56,0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(232,168,56,0.35); }

/* ───── PAGE TITLE ───── */
.page-eyebrow {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 3px;
    text-transform: uppercase; color: var(--accent-gold); margin-bottom: 4px;
}
.page-title {
    font-size: 2.6rem; font-weight: 800; color: var(--text-primary);
    line-height: 1.15; margin-bottom: 6px; letter-spacing: -0.5px;
}
.page-title em {
    font-style: normal;
    background: linear-gradient(135deg, var(--accent-gold), var(--accent-amber));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.page-desc { font-size: 1.05rem; color: var(--text-secondary); line-height: 1.6; max-width: 680px; }

/* ───── SECTION HEADERS ───── */
.sh { display: flex; align-items: center; gap: 12px; margin: 36px 0 16px 0; }
.sh-icon {
    width: 36px; height: 36px; border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.sh-icon.gold   { background: rgba(232,168,56,0.12); }
.sh-icon.teal   { background: rgba(63,185,160,0.12); }
.sh-icon.blue   { background: rgba(88,166,255,0.12); }
.sh-icon.violet { background: rgba(167,139,250,0.12); }
.sh-icon.coral  { background: rgba(224,108,96,0.12); }
.sh-icon.rose   { background: rgba(244,114,182,0.12); }

.sh-text { font-size: 1.35rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.3px; }
.sh-line { flex: 1; height: 1px; background: var(--border-subtle); }

/* ───── CARDS ───── */
.card {
    background: var(--bg-card); border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg); padding: 24px;
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
.card:hover { border-color: var(--border-accent); box-shadow: var(--shadow-glow); }
.card h4 { color: var(--text-primary); margin-top: 0; font-size: 1.05rem; font-weight: 600; }
.card p, .card li  { color: var(--text-secondary); line-height: 1.65; font-size: 0.92rem; }

.card--bordered-gold  { border-left: 3px solid var(--accent-gold); }
.card--bordered-teal  { border-left: 3px solid var(--accent-teal); }
.card--bordered-coral { border-left: 3px solid var(--accent-coral); }
.card--bordered-blue  { border-left: 3px solid var(--accent-blue); }
.card--bordered-violet{ border-left: 3px solid var(--accent-violet); }

.card--highlight {
    background: linear-gradient(135deg, rgba(232,168,56,0.06) 0%, var(--bg-card) 60%);
    border-color: rgba(232,168,56,0.15);
}

/* ───── KPI TILES EXCLUSIVOS CREADOS POR MI ───── */
.kpi {
    background: var(--bg-card); border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg); padding: 20px; text-align: center;
    position: relative; overflow: hidden; transition: transform 0.2s ease, border-color 0.2s ease;
}
.kpi:hover { transform: translateY(-2px); border-color: var(--border-accent); }
.kpi::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent-gold), var(--accent-amber));
    opacity: 0; transition: opacity 0.25s ease;
}
.kpi:hover::before { opacity: 1; }
.kpi-val { font-size: 1.6rem; font-weight: 800; color: var(--text-primary); line-height: 1.15; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.kpi-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-muted); margin-top: 6px; }
.kpi-sub { font-size: 0.78rem; color: var(--accent-teal); margin-top: 2px; }

/* ───── DIVIDER ───── */
.sep { height: 1px; background: var(--border-subtle); margin: 28px 0; }

/* ───── OTRAS UTILIDADES ───── */
.tag {
    display: inline-block; font-size: 0.68rem; font-weight: 600; letter-spacing: 1px;
    text-transform: uppercase; padding: 3px 10px; border-radius: 6px;
}
.tag--gold   { background: rgba(232,168,56,0.12); color: var(--accent-gold); }
.tag--teal   { background: rgba(63,185,160,0.12); color: var(--accent-teal); }
.tag--coral  { background: rgba(224,108,96,0.12); color: var(--accent-coral); }
.tag--blue   { background: rgba(88,166,255,0.12); color: var(--accent-blue); }
.tag--violet { background: rgba(167,139,250,0.12); color: var(--accent-violet); }

.text-gold   { color: var(--accent-gold); }
.text-teal   { color: var(--accent-teal); }
.text-coral  { color: var(--accent-coral); }
.text-blue   { color: var(--accent-blue); }
.text-violet { color: var(--accent-violet); }
</style>
"""

CHART_COLORS = [
    '#e8a838', '#3fb9a0', '#58a6ff', '#a78bfa', '#f472b6',
    '#e06c60', '#f0983e', '#34d399', '#818cf8', '#fb923c',
    '#38bdf8', '#c084fc',
]

CHART_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans, sans-serif', color='#8b949e'),
    title_x=0.5, title_y=0.97, title_xanchor='center', title_yanchor='top',
    title_font=dict(size=16, color='#e2e8f0', family='Plus Jakarta Sans, sans-serif'),
    margin=dict(l=60, r=30, t=80, b=130),
    coloraxis_showscale=False,
    legend=dict(
        orientation='h', yanchor='top', y=-0.32, xanchor='center', x=0.5,
        title=dict(text=''),
        font=dict(size=11, color='#8b949e')
    ),
    xaxis=dict(
        gridcolor='rgba(201,209,217,0.06)',
        zerolinecolor='rgba(201,209,217,0.06)',
        title_standoff=25,
        automargin=True,
    ),
    yaxis=dict(
        gridcolor='rgba(201,209,217,0.06)',
        zerolinecolor='rgba(201,209,217,0.06)',
        title_standoff=20,
        automargin=True,
    ),
)

SCALE_GOLD  = ['#151a25', '#2a2520', '#5c4a20', '#8a6e1e', '#b8911e', '#e8a838']
SCALE_TEAL  = ['#151a25', '#152520', '#1a3a30', '#1f5040', '#2a7a5a', '#3fb9a0']
SCALE_CORAL = ['#151a25', '#251a1a', '#3a2020', '#5c3030', '#8a4a40', '#e06c60']

def apply_layout(fig, **overrides):
    layout = {**CHART_LAYOUT, **overrides}
    fig.update_layout(**layout)
    return fig

def section_header(icon, title, color='gold'):
    return f"""
    <div class="sh">
        <div class="sh-icon {color}">{icon}</div>
        <span class="sh-text">{title}</span>
        <span class="sh-line"></span>
    </div>"""

def kpi_tile(value, label, subtitle=''):
    sub_html = f'<div class="kpi-sub">{subtitle}</div>' if subtitle else ''
    return f"""
    <div class="kpi">
        <div class="kpi-val">{value}</div>
        <div class="kpi-label">{label}</div>
        {sub_html}
    </div>"""

def sidebar_nav():
    import streamlit as st
    st.sidebar.markdown('---')
    st.sidebar.markdown(
        '<p style="font-size:0.72rem;color:#545d68;text-align:center;">'
        '© 2026 · Proyecto CDE-AC<br>Análisis Criminológico Internacional</p>',
        unsafe_allow_html=True
    )
