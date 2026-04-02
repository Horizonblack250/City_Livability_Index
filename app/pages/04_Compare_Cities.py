import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.scoring import load_data, compute_scores
from utils.styles  import apply_theme, eyebrow, GOLD, PARCH, MUTED, SURFACE, BORDER

st.set_page_config(page_title="Compare Cities · City Livability Index", page_icon="◎", layout="wide")
apply_theme()

df = load_data()

# ── sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<p style='font-size:10px;color:{MUTED};letter-spacing:0.2em;text-transform:uppercase;margin-bottom:16px'>Pillar weights</p>", unsafe_allow_html=True)
    w_air    = st.slider("Air quality",    0, 100, 25, key="cc_air")
    w_cost   = st.slider("Cost of living", 0, 100, 30, key="cc_cost")
    w_safety = st.slider("Safety",         0, 100, 25, key="cc_safety")
    w_urban  = st.slider("Urban density",  0, 100, 20, key="cc_urban")
    st.divider()
    cost_model = st.radio("Cost model", ["absolute", "affordability"],
                          format_func=lambda x: "Absolute cost" if x=="absolute" else "Affordability ratio",
                          key="cc_model")

df = compute_scores(df, w_air, w_cost, w_safety, w_urban, cost_model)
df['city'] = df['city'].str.title()

# ── header ────────────────────────────────────────────────
eyebrow("Head-to-head analysis · Project Daedalus")
st.markdown("<h1>Compare cities</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{MUTED};font-size:13px;margin-bottom:28px'>Select 2 to 4 cities to compare across all pillars.</p>", unsafe_allow_html=True)

# ── city selector ─────────────────────────────────────────
cities = sorted(df['city'].unique())
selected = st.multiselect(
    "Select cities",
    cities,
    default=['Tampere', 'Ljubljana', 'Munich'],
    max_selections=4,
    placeholder="Search for a city..."
)

if len(selected) < 2:
    st.markdown(f"<p style='color:{MUTED};font-size:13px;margin-top:20px'>Select at least 2 cities to begin comparison.</p>", unsafe_allow_html=True)
    st.stop()

subset  = df[df['city'].isin(selected)].drop_duplicates(subset='city')
colors  = ['#c9a96e', '#7b9e7b', '#4a7a8a', '#8b7355']
cost_col = 'cost_score_absolute' if cost_model == 'absolute' else 'cost_score_affordability'

# ── score cards ───────────────────────────────────────────
st.divider()
cols = st.columns(len(selected))
for i, (_, row) in enumerate(subset.iterrows()):
    with cols[i]:
        color = colors[i % len(colors)]
        st.markdown(f"""
        <div style='background:{SURFACE};border:1px solid {color};border-radius:8px;
                    padding:20px;text-align:center'>
            <div style='font-size:10px;color:{MUTED};letter-spacing:0.15em;
                        text-transform:uppercase;margin-bottom:8px'>
                #{int(row['rank'])} globally
            </div>
            <div style='font-size:18px;color:{PARCH};margin-bottom:4px;
                        font-family:"Playfair Display",serif'>
                {row['city']}
            </div>
            <div style='font-size:11px;color:{MUTED};margin-bottom:16px'>
                {row['country']}
            </div>
            <div style='font-size:32px;color:{color};font-family:"Playfair Display",serif;
                        font-weight:400;margin-bottom:4px'>
                {row['livability_score']:.1f}
            </div>
            <div style='font-size:10px;color:{MUTED}'>composite score</div>
        </div>
        """, unsafe_allow_html=True)

# ── radar chart ───────────────────────────────────────────
st.divider()
col_radar, col_bars = st.columns([1, 1])

with col_radar:
    st.markdown("<h2 style='margin-bottom:16px'>Pillar comparison</h2>", unsafe_allow_html=True)
    categories = ['Air quality', 'Cost', 'Safety', 'Urban density']
    score_cols = ['air_quality_score', cost_col, 'safety_score', 'urban_score']

    fig_radar = go.Figure()
    for i, (_, row) in enumerate(subset.iterrows()):
        values = [row[c] for c in score_cols]
        values += [values[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=row['city'],
            line=dict(color=colors[i % len(colors)], width=2),
            fillcolor=colors[i % len(colors)],
            opacity=0.25,
            hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}<extra>' + row['city'] + '</extra>',
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor=SURFACE,
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color=MUTED, size=8),
                gridcolor=BORDER,
                linecolor=BORDER,
            ),
            angularaxis=dict(
                tickfont=dict(color=PARCH, size=11),
                gridcolor=BORDER,
                linecolor=BORDER,
            ),
        ),
        paper_bgcolor=SURFACE,
        height=420,
        legend=dict(
            font=dict(color=MUTED, size=10, family='Inter'),
            bgcolor=SURFACE,
            bordercolor=BORDER,
            borderwidth=1,
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family='Inter'),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_bars:
    st.markdown("<h2 style='margin-bottom:16px'>Score breakdown</h2>", unsafe_allow_html=True)
    pillar_labels = {
        'air_quality_score':        'Air quality',
        cost_col:                   'Cost',
        'safety_score':             'Safety',
        'urban_score':              'Urban density',
    }

    fig_bars = go.Figure()
    for i, (_, row) in enumerate(subset.iterrows()):
        fig_bars.add_trace(go.Bar(
            name=row['city'],
            x=list(pillar_labels.values()),
            y=[row[c] for c in pillar_labels.keys()],
            marker_color=colors[i % len(colors)],
            opacity=0.85,
            hovertemplate='<b>%{x}</b><br>%{y:.1f}<extra>' + row['city'] + '</extra>',
        ))

    fig_bars.update_layout(
        barmode='group',
        height=420,
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        xaxis=dict(
            gridcolor=BORDER,
            tickfont=dict(color=PARCH, size=11),
            linecolor=BORDER,
        ),
        yaxis=dict(
            range=[0, 100],
            gridcolor=BORDER,
            tickfont=dict(color=MUTED, size=9),
            linecolor=BORDER,
        ),
        legend=dict(
            font=dict(color=MUTED, size=10, family='Inter'),
            bgcolor=SURFACE,
            bordercolor=BORDER,
            borderwidth=1,
        ),
        margin=dict(l=0, r=0, t=10, b=10),
        font=dict(family='Inter'),
    )
    st.plotly_chart(fig_bars, use_container_width=True)

# ── raw stats table ───────────────────────────────────────
st.divider()
st.markdown("<h2 style='margin-bottom:16px'>Raw data comparison</h2>", unsafe_allow_html=True)

display_cols = {
    'city':                  'City',
    'country':               'Country',
    'livability_score':      'Score',
    'aqi_value':             'AQI',
    'air_quality_score':     'Air quality',
    cost_col:                'Cost score',
    'safety_score':          'Safety score',
    'urban_score':           'Urban score',
    'rent_1br_outside_usd':  'Rent 1BR (USD)',
    'basic_utilities_usd':   'Utilities (USD)',
    'avg_net_salary_usd':    'Avg salary (USD)',
    'crime_index':           'Crime index',
    'densitycity':           'Pop. density',
    'congestion2019':        'Congestion',
}

table = subset[list(display_cols.keys())].copy()
table['rent_1br_outside_usd'] = table['rent_1br_outside_usd'].round(0).astype(int)
table['basic_utilities_usd']  = table['basic_utilities_usd'].round(0).astype(int)
table['avg_net_salary_usd']   = table['avg_net_salary_usd'].round(0).astype(int)
table['densitycity']          = table['densitycity'].round(0).astype(int)
table['congestion2019']       = table['congestion2019'].round(1)
table = table.rename(columns=display_cols).set_index('City')

st.dataframe(table.T, use_container_width=True)

# ── insight callout ───────────────────────────────────────
st.divider()
best_air    = subset.loc[subset['air_quality_score'].idxmax(), 'city']
best_safety = subset.loc[subset['safety_score'].idxmax(), 'city']
best_cost   = subset.loc[subset[cost_col].idxmax(), 'city']
best_urban  = subset.loc[subset['urban_score'].idxmax(), 'city']
best_overall= subset.loc[subset['livability_score'].idxmax(), 'city']

st.markdown(f"""
<div style='background:{SURFACE};border:1px solid {BORDER};border-radius:8px;padding:24px'>
    <p style='font-size:10px;color:{MUTED};letter-spacing:0.2em;text-transform:uppercase;margin-bottom:16px'>
        Insights from this comparison
    </p>
    <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px'>
        <div>
            <span style='font-size:11px;color:{MUTED}'>Best air quality</span><br>
            <span style='font-size:14px;color:{GOLD}'>{best_air}</span>
        </div>
        <div>
            <span style='font-size:11px;color:{MUTED}'>Safest city</span><br>
            <span style='font-size:14px;color:{GOLD}'>{best_safety}</span>
        </div>
        <div>
            <span style='font-size:11px;color:{MUTED}'>Best cost score</span><br>
            <span style='font-size:14px;color:{GOLD}'>{best_cost}</span>
        </div>
        <div>
            <span style='font-size:11px;color:{MUTED}'>Best urban score</span><br>
            <span style='font-size:14px;color:{GOLD}'>{best_urban}</span>
        </div>
    </div>
    <div style='margin-top:16px;padding-top:16px;border-top:1px solid {BORDER}'>
        <span style='font-size:11px;color:{MUTED}'>Overall winner</span><br>
        <span style='font-size:18px;color:{GOLD};font-family:"Playfair Display",serif'>{best_overall}</span>
    </div>
</div>
""", unsafe_allow_html=True)