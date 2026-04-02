import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.scoring import load_data, compute_scores
from utils.styles  import apply_theme, eyebrow, GOLD, PARCH, MUTED, SURFACE, BORDER, PLOTLY_THEME

st.set_page_config(page_title="Map · City Livability Index", page_icon="◎", layout="wide")
apply_theme()

df = load_data()

# ── sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<p style='font-size:10px;color:{MUTED};letter-spacing:0.2em;text-transform:uppercase;margin-bottom:16px'>Pillar weights</p>", unsafe_allow_html=True)
    w_air    = st.slider("Air quality",    0, 100, 25, key="map_air")
    w_cost   = st.slider("Cost of living", 0, 100, 30, key="map_cost")
    w_safety = st.slider("Safety",         0, 100, 25, key="map_safety")
    w_urban  = st.slider("Urban density",  0, 100, 20, key="map_urban")
    st.divider()
    cost_model = st.radio("Cost model", ["absolute", "affordability"],
                          format_func=lambda x: "Absolute cost" if x=="absolute" else "Affordability ratio",
                          key="map_model")

df = compute_scores(df, w_air, w_cost, w_safety, w_urban, cost_model)

# ── header ────────────────────────────────────────────────
eyebrow("Global livability · 333 cities")
st.markdown("<h1>Global map</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{MUTED};font-size:13px;margin-bottom:24px'>Each point is a city. Color encodes composite livability score. Hover for details.</p>", unsafe_allow_html=True)

# ── filters ───────────────────────────────────────────────
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    countries = sorted(df['country'].dropna().unique())
    selected_countries = st.multiselect("Filter by country", countries,
                                        placeholder="All countries shown")
with col_f2:
    min_score = st.slider("Min score", 0, 100, 0, key="map_minscore")

filtered = df.copy()
if selected_countries:
    filtered = filtered[filtered['country'].isin(selected_countries)]
filtered = filtered[filtered['livability_score'] >= min_score]

# ── map ───────────────────────────────────────────────────
fig = px.scatter_geo(
    filtered,
    locations='country',
    locationmode='country names',
    color='livability_score',
    hover_name='city',
    hover_data={
        'country':           True,
        'livability_score':  ':.1f',
        'air_quality_score': ':.1f',
        'safety_score':      ':.1f',
        'urban_score':       ':.1f',
        'aqi_value':         True,
        'crime_index':       ':.1f',
    },
    color_continuous_scale=[
        [0.0,  '#7b2d2d'],
        [0.3,  '#8b6914'],
        [0.6,  '#7b9e87'],
        [0.8,  '#c9a96e'],
        [1.0,  '#e8dcc8'],
    ],
    range_color=[30, 95],
    size='livability_score',
    size_max=14,
    projection='natural earth',
)

fig.update_layout(
    height=560,
    paper_bgcolor=SURFACE,
    plot_bgcolor=SURFACE,
    geo=dict(
        bgcolor=SURFACE,
        landcolor='#141920',
        oceancolor='#0a0d11',
        lakecolor='#0a0d11',
        coastlinecolor='#1e2530',
        countrycolor='#1e2530',
        showland=True,
        showocean=True,
        showlakes=True,
        showcountries=True,
        showcoastlines=True,
        framecolor='#1e2530',
    ),
    coloraxis_colorbar=dict(
        title=dict(text="Score", font=dict(color=MUTED, size=10)),
        tickfont=dict(color=MUTED, size=9),
        bgcolor=SURFACE,
        bordercolor=BORDER,
        borderwidth=1,
        thickness=12,
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    font=dict(family='Inter', color=MUTED),
)
st.plotly_chart(fig, use_container_width=True)

# ── stats row ─────────────────────────────────────────────
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cities shown",    len(filtered))
c2.metric("Highest score",   f"{filtered['livability_score'].max():.1f}",
          filtered.loc[filtered['livability_score'].idxmax(), 'city'].title())
c3.metric("Lowest score",    f"{filtered['livability_score'].min():.1f}",
          filtered.loc[filtered['livability_score'].idxmin(), 'city'].title())
c4.metric("Average score",   f"{filtered['livability_score'].mean():.1f}")

# ── table ─────────────────────────────────────────────────
st.divider()
st.markdown("<h2>City rankings</h2>", unsafe_allow_html=True)

display = filtered[['rank', 'city', 'country', 'livability_score',
                     'air_quality_score', 'safety_score', 'urban_score',
                     'aqi_value', 'rent_1br_outside_usd', 'crime_index']]\
            .copy()
display['city']    = display['city'].str.title()
display['country'] = display['country'].str.title()
display = display.rename(columns={
    'livability_score':   'Score',
    'air_quality_score':  'Air',
    'safety_score':       'Safety',
    'urban_score':        'Urban',
    'aqi_value':          'AQI',
    'rent_1br_outside_usd': 'Rent (USD)',
    'crime_index':        'Crime idx',
}).set_index('rank')

st.dataframe(display, use_container_width=True, height=420)