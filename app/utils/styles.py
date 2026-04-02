import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@300;400;500&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* App background */
    .stApp {
        background-color: #0f1318;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0a0d11 !important;
        border-right: 1px solid #1e2530 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #6b7280 !important;
    }
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stRadio label {
        color: #6b7280 !important;
        font-size: 12px !important;
        letter-spacing: 0.05em !important;
    }

    /* Slider accent */
    .stSlider > div > div > div > div {
        background-color: #c9a96e !important;
    }

    /* Headings */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #e8dcc8 !important;
        font-weight: 400 !important;
        letter-spacing: -0.01em !important;
    }
    h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #c9a96e !important;
        font-weight: 400 !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background-color: #0a0d11 !important;
        border: 1px solid #1e2530 !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    [data-testid="metric-container"] label {
        color: #4a5568 !important;
        font-size: 10px !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #e8dcc8 !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 28px !important;
        font-weight: 400 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #c9a96e !important;
    }

    /* Dataframe */
    .stDataFrame {
        border: 1px solid #1e2530 !important;
        border-radius: 8px !important;
    }

    /* Divider */
    hr {
        border-color: #1e2530 !important;
    }

    /* Selectbox / multiselect */
    .stMultiSelect > div, .stSelectbox > div {
        background-color: #0a0d11 !important;
        border-color: #1e2530 !important;
    }

    /* Plotly chart background */
    .js-plotly-plot {
        border-radius: 8px !important;
        border: 1px solid #1e2530 !important;
    }

    /* Page title eyebrow style */
    .eyebrow {
        font-size: 10px;
        color: #4a5568;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def eyebrow(text):
    st.markdown(f'<p class="eyebrow">{text}</p>', unsafe_allow_html=True)

PLOTLY_THEME = dict(
    paper_bgcolor='#0a0d11',
    plot_bgcolor='#0a0d11',
    font=dict(family='Inter', color='#6b7280', size=11),
    xaxis=dict(gridcolor='#1e2530', linecolor='#1e2530', tickcolor='#1e2530'),
    yaxis=dict(gridcolor='#1e2530', linecolor='#1e2530', tickcolor='#1e2530'),
    colorway=['#c9a96e', '#7b9e87', '#8b7355', '#5a7a8a', '#9e7b7b'],
)

GOLD    = '#c9a96e'
PARCH   = '#e8dcc8'
MUTED   = '#4a5568'
SURFACE = '#0a0d11'
BORDER  = '#1e2530'