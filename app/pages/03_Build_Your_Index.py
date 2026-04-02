import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.scoring import load_data, compute_scores
from utils.styles  import apply_theme, eyebrow, GOLD, PARCH, MUTED, SURFACE, BORDER

st.set_page_config(page_title="Build Your Index · City Livability Index", page_icon="◎", layout="wide")
apply_theme()

df = load_data()

# ── sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<p style='font-size:10px;color:{MUTED};letter-spacing:0.2em;text-transform:uppercase;margin-bottom:16px'>Your priorities</p>", unsafe_allow_html=True)
    w_air    = st.slider("Air quality",    0, 100, 25, key="bi_air")
    w_cost   = st.slider("Cost of living", 0, 100, 30, key="bi_cost")
    w_safety = st.slider("Safety",         0, 100, 25, key="bi_safety")
    w_urban  = st.slider("Urban density",  0, 100, 20, key="bi_urban")
    st.divider()
    cost_model = st.radio("Cost model", ["absolute", "affordability"],
                          format_func=lambda x: "Absolute cost" if x=="absolute" else "Affordability ratio",
                          key="bi_model")
    st.divider()
    total = w_air + w_cost + w_safety + w_urban
    if total > 0:
        st.markdown(f"""
        <div style='background:{SURFACE};border:1px solid {BORDER};border-radius:6px;padding:12px'>
            <p style='font-size:10px;color:{MUTED};letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px'>Weight breakdown</p>
            <p style='font-size:11px;color:{GOLD};margin:3px 0'>Air quality &nbsp;&nbsp; {w_air/total*100:.0f}%</p>
            <p style='font-size:11px;color:{GOLD};margin:3px 0'>Cost &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {w_cost/total*100:.0f}%</p>
            <p style='font-size:11px;color:{GOLD};margin:3px 0'>Safety &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {w_safety/total*100:.0f}%</p>
            <p style='font-size:11px;color:{GOLD};margin:3px 0'>Urban &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {w_urban/total*100:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)

df = compute_scores(df, w_air, w_cost, w_safety, w_urban, cost_model)
df['city'] = df['city'].str.title()

# ── header ────────────────────────────────────────────────
eyebrow("Personalised ranking · Project Daedalus")
st.markdown("<h1>Build your index</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{MUTED};font-size:13px;margin-bottom:28px'>Move the sliders to reflect what matters to you. Rankings recalculate instantly.</p>", unsafe_allow_html=True)

with st.expander("◈  How to use this page"):
    st.markdown(f"""
    <div style='color:{MUTED};font-size:13px;line-height:1.9'>
        <p style='color:{PARCH};margin-bottom:8px'>Adjust the four sliders to reflect what matters most to you.</p>
        <p><span style='color:{GOLD}'>Air quality</span> — Move right if clean air is a priority.
        Cities with low AQI and PM2.5 rank higher.</p>
        <p><span style='color:{GOLD}'>Cost of living</span> — Move right to prioritise affordability.
        Toggle between absolute cost (cheapest cities win) and affordability ratio
        (cost relative to local salary — better for remote workers).</p>
        <p><span style='color:{GOLD}'>Safety</span> — Move right if safety is non-negotiable.
        Cities with low crime index and high safety index rank higher.</p>
        <p><span style='color:{GOLD}'>Urban density</span> — Move right to favour walkable,
        moderately dense cities with lower congestion.</p>
        <br>
        <p style='color:{MUTED};font-size:11px'>
        Weights are auto-normalised — they always sum to 100% regardless of absolute values.
        Setting all sliders equal means each pillar contributes 25%.
        </p>
    </div>
    """, unsafe_allow_html=True)

if total == 0:
    st.warning("Set at least one weight above zero.")
    st.stop()
# ── top row — pie + top 10 ────────────────────────────────
col_pie, col_top = st.columns([1, 2])

with col_pie:
    st.markdown(f"<h2 style='margin-bottom:16px'>Your weights</h2>", unsafe_allow_html=True)
    fig_pie = go.Figure(go.Pie(
        labels=['Air quality', 'Cost', 'Safety', 'Urban'],
        values=[w_air, w_cost, w_safety, w_urban],
        hole=0.55,
        marker=dict(
            colors=['#4a7a8a', '#c9a96e', '#7b9e7b', '#8b7355'],
            line=dict(color=SURFACE, width=2),
        ),
        textfont=dict(color=PARCH, size=10, family='Inter'),
        hovertemplate='<b>%{label}</b><br>%{percent}<extra></extra>',
    ))
    fig_pie.update_layout(
        height=300,
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        showlegend=True,
        legend=dict(
            font=dict(color=MUTED, size=10, family='Inter'),
            bgcolor=SURFACE,
            bordercolor=BORDER,
            borderwidth=1,
        ),
        margin=dict(l=0, r=0, t=10, b=10),
        annotations=[dict(
            text=f'<b>{total}</b><br><span style="font-size:9px">total</span>',
            x=0.5, y=0.5, font=dict(color=GOLD, size=14, family='Inter'),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_top:
    st.markdown(f"<h2 style='margin-bottom:16px'>Your top 10</h2>", unsafe_allow_html=True)
    top10 = df.head(10)
    for i, (_, row) in enumerate(top10.iterrows()):
        bar_pct = row['livability_score'] / 100
        rank_color = GOLD if i == 0 else PARCH
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:12px;margin-bottom:10px;
                    padding:10px 14px;background:{SURFACE};border:1px solid {BORDER};
                    border-radius:6px'>
            <div style='font-size:11px;color:{rank_color};width:20px;
                        font-family:"Playfair Display",serif;flex-shrink:0'>
                {i+1}
            </div>
            <div style='flex:1;min-width:0'>
                <div style='font-size:13px;color:{PARCH};margin-bottom:4px;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>
                    {row['city']}
                    <span style='font-size:10px;color:{MUTED};margin-left:6px'>
                        {row['country']}
                    </span>
                </div>
                <div style='background:{BORDER};border-radius:2px;height:3px'>
                    <div style='background:{GOLD};width:{bar_pct*100:.0f}%;
                                height:100%;border-radius:2px'></div>
                </div>
            </div>
            <div style='font-size:13px;color:{GOLD};font-weight:500;
                        flex-shrink:0;width:36px;text-align:right'>
                {row['livability_score']:.1f}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── full bar chart ────────────────────────────────────────
st.divider()
st.markdown("<h2 style='margin-bottom:16px'>Top 30 — score breakdown</h2>", unsafe_allow_html=True)

cost_col = 'cost_score_absolute' if cost_model == 'absolute' else 'cost_score_affordability'
top30 = df.head(30)

fig_bar = go.Figure()
pillar_cfg = [
    ('air_quality_score', 'Air quality', '#4a7a8a'),
    (cost_col,            'Cost',        '#c9a96e'),
    ('safety_score',      'Safety',      '#7b9e7b'),
    ('urban_score',       'Urban',       '#8b7355'),
]

for col, label, color in pillar_cfg:
    contrib = top30[col] * ([w_air, w_cost, w_safety, w_urban][
        ['air_quality_score', cost_col, 'safety_score', 'urban_score'].index(col)
    ] / total)
    fig_bar.add_trace(go.Bar(
        x=contrib,
        y=top30['city'],
        orientation='h',
        name=label,
        marker_color=color,
        hovertemplate=f'<b>%{{y}}</b><br>{label}: %{{x:.1f}}<extra></extra>',
    ))

fig_bar.update_layout(
    barmode='stack',
    height=680,
    paper_bgcolor=SURFACE,
    plot_bgcolor=SURFACE,
    xaxis=dict(
        gridcolor=BORDER,
        tickfont=dict(color=MUTED, size=9),
        linecolor=BORDER,
        title=dict(text='Composite score', font=dict(color=MUTED, size=10)),
    ),
    yaxis=dict(
        tickfont=dict(color=PARCH, size=11),
        linecolor=BORDER,
        autorange='reversed',
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom', y=1.01,
        xanchor='left', x=0,
        font=dict(color=MUTED, size=10, family='Inter'),
        bgcolor=SURFACE,
        bordercolor=BORDER,
        borderwidth=1,
    ),
    margin=dict(l=0, r=20, t=40, b=10),
    font=dict(family='Inter'),
)
st.plotly_chart(fig_bar, use_container_width=True)

# ── full table ────────────────────────────────────────────
st.divider()
st.markdown("<h2>Full personalised rankings</h2>", unsafe_allow_html=True)

display = df[['rank', 'city', 'country', 'livability_score',
              'air_quality_score', cost_col, 'safety_score', 'urban_score']].copy()
display['country'] = display['country'].str.title()
display = display.rename(columns={
    'livability_score':  'Score',
    'air_quality_score': 'Air',
    cost_col:            'Cost',
    'safety_score':      'Safety',
    'urban_score':       'Urban',
}).set_index('rank')

st.dataframe(display, use_container_width=True, height=420)