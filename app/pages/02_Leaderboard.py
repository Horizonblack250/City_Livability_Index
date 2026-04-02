import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.scoring import load_data, compute_scores
from utils.styles  import apply_theme, eyebrow, GOLD, PARCH, MUTED, SURFACE, BORDER

st.set_page_config(page_title="Leaderboard · City Livability Index", page_icon="◎", layout="wide")
apply_theme()

df = load_data()

# ── sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
<p style='color:{MUTED};font-size:13px;margin-bottom:28px'>
Ranked by composite livability score using current sidebar weights.
Default weights: air quality 25%, cost 30%, safety 25%, urban density 20%.
Adjust the sliders to personalise the ranking.
</p>
""", unsafe_allow_html=True)
    w_air    = st.slider("Air quality",    0, 100, 25, key="lb_air")
    w_cost   = st.slider("Cost of living", 0, 100, 30, key="lb_cost")
    w_safety = st.slider("Safety",         0, 100, 25, key="lb_safety")
    w_urban  = st.slider("Urban density",  0, 100, 20, key="lb_urban")
    st.divider()
    cost_model = st.radio("Cost model", ["absolute", "affordability"],
                          format_func=lambda x: "Absolute cost" if x=="absolute" else "Affordability ratio",
                          key="lb_model")
    st.divider()
    n = st.slider("Cities to show", 5, 30, 20, key="lb_n")

df = compute_scores(df, w_air, w_cost, w_safety, w_urban, cost_model)

# ── header ────────────────────────────────────────────────
eyebrow("Global rankings · Project Daedalus")
st.markdown("<h1>Leaderboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{MUTED};font-size:13px;margin-bottom:28px'>Ranked by composite livability score. Adjust weights in the sidebar to personalise.</p>", unsafe_allow_html=True)

top    = df.head(n).copy()
bottom = df.tail(n).copy().sort_values('livability_score', ascending=True)
top['city']    = top['city'].str.title()
bottom['city'] = bottom['city'].str.title()

col1, col2 = st.columns(2)

# ── top cities chart ──────────────────────────────────────
with col1:
    st.markdown(f"<h2 style='margin-bottom:16px'>Top {n} cities</h2>", unsafe_allow_html=True)
    fig_top = go.Figure()
    fig_top.add_trace(go.Bar(
        x=top['livability_score'],
        y=top['city'],
        orientation='h',
        marker=dict(
            color=top['livability_score'],
            colorscale=[
                [0.0, '#5a7a5a'],
                [0.5, '#7b9e7b'],
                [1.0, '#c9a96e'],
            ],
            showscale=False,
        ),
        text=top['livability_score'].apply(lambda x: f"{x:.1f}"),
        textposition='outside',
        textfont=dict(color=GOLD, size=10, family='Inter'),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>',
    ))
    fig_top.update_layout(
        height=520,
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        xaxis=dict(
            range=[60, 100],
            gridcolor=BORDER,
            tickfont=dict(color=MUTED, size=9),
            linecolor=BORDER,
        ),
        yaxis=dict(
            tickfont=dict(color=PARCH, size=11),
            linecolor=BORDER,
        ),
        margin=dict(l=0, r=60, t=10, b=10),
        font=dict(family='Inter'),
    )
    st.plotly_chart(fig_top, use_container_width=True)

# ── bottom cities chart ───────────────────────────────────
with col2:
    st.markdown(f"<h2 style='margin-bottom:16px'>Bottom {n} cities</h2>", unsafe_allow_html=True)
    fig_bot = go.Figure()
    fig_bot.add_trace(go.Bar(
        x=bottom['livability_score'],
        y=bottom['city'],
        orientation='h',
        marker=dict(
            color=bottom['livability_score'],
            colorscale=[
                [0.0, '#7b2d2d'],
                [0.5, '#8b5a3a'],
                [1.0, '#8b6914'],
            ],
            showscale=False,
        ),
        text=bottom['livability_score'].apply(lambda x: f"{x:.1f}"),
        textposition='outside',
        textfont=dict(color='#c97a6e', size=10, family='Inter'),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>',
    ))
    fig_bot.update_layout(
        height=520,
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        xaxis=dict(
            range=[0, 65],
            gridcolor=BORDER,
            tickfont=dict(color=MUTED, size=9),
            linecolor=BORDER,
        ),
        yaxis=dict(
            tickfont=dict(color=PARCH, size=11),
            linecolor=BORDER,
        ),
        margin=dict(l=0, r=60, t=10, b=10),
        font=dict(family='Inter'),
    )
    st.plotly_chart(fig_bot, use_container_width=True)

# ── full table ────────────────────────────────────────────
st.divider()
st.markdown("<h2>Full rankings</h2>", unsafe_allow_html=True)

cost_col = 'cost_score_absolute' if cost_model == 'absolute' else 'cost_score_affordability'

display = df[['rank', 'city', 'country', 'livability_score',
              'air_quality_score', cost_col, 'safety_score', 'urban_score',
              'aqi_value', 'rent_1br_outside_usd', 'avg_net_salary_usd', 'crime_index']].copy()

display['city']    = display['city'].str.title()
display['country'] = display['country'].str.title()
display['rent_1br_outside_usd']  = display['rent_1br_outside_usd'].round(0).astype(int)
display['avg_net_salary_usd']    = display['avg_net_salary_usd'].round(0).astype(int)
display['crime_index']           = display['crime_index'].round(1)

display = display.rename(columns={
    'livability_score':        'Score',
    'air_quality_score':       'Air',
    cost_col:                  'Cost',
    'safety_score':            'Safety',
    'urban_score':             'Urban',
    'aqi_value':               'AQI',
    'rent_1br_outside_usd':    'Rent (USD)',
    'avg_net_salary_usd':      'Salary (USD)',
    'crime_index':             'Crime',
}).set_index('rank')

st.dataframe(display, use_container_width=True, height=500)