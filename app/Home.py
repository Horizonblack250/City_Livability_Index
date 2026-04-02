import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.scoring import load_data
from utils.styles  import apply_theme, eyebrow, GOLD, PARCH, MUTED, SURFACE, BORDER

st.set_page_config(
    page_title="City Livability Index",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_theme()

df = load_data()
df['city'] = df['city'].str.title()
top5    = df.sort_values('livability_score_absolute', ascending=False).head(5)
top_city = top5.iloc[0]

# ── hero ──────────────────────────────────────────────────
eyebrow("Data-driven urban intelligence")
st.markdown("""
<h1 style='font-size:42px; margin-bottom:8px; line-height:1.15'>
    Where in the world<br>would you live?
</h1>
""", unsafe_allow_html=True)

st.markdown(f"""
<p style='font-size:14px; color:{MUTED}; max-width:540px; line-height:1.8; margin-bottom:32px'>
A composite livability index across {len(df)} global cities —
built from air quality, cost of living, safety, and urban density data.
Adjust the weights. Explore the map. Find your city.
</p>
""", unsafe_allow_html=True)

# ── metrics ───────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cities ranked",   len(df),           "across 6 continents")
c2.metric("Top city",        top_city['city'],  f"{top_city['livability_score_absolute']:.1f} / 100")
c3.metric("Avg score",       f"{df['livability_score_absolute'].mean():.1f}", "out of 100")
c4.metric("Source datasets", "5",               "4 scoring pillars")

st.divider()

# ── pillar explainer ──────────────────────────────────────
st.markdown("<h2 style='margin-bottom:20px'>The four pillars</h2>", unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)

def pillar_card(col, symbol, name, desc, score_col):
    avg = df[score_col].mean()
    col.markdown(f"""
    <div style='background:{SURFACE};border:1px solid {BORDER};border-radius:8px;
                padding:20px;height:160px'>
        <div style='font-size:22px;margin-bottom:10px;color:{GOLD}'>{symbol}</div>
        <div style='font-size:13px;color:{PARCH};font-weight:500;
                    margin-bottom:6px'>{name}</div>
        <div style='font-size:11px;color:{MUTED};line-height:1.6;
                    margin-bottom:10px'>{desc}</div>
        <div style='font-size:10px;color:{GOLD}'>avg {avg:.0f} / 100</div>
    </div>
    """, unsafe_allow_html=True)

pillar_card(p1, "◌", "Air quality",    "AQI + PM2.5 levels",             "air_quality_score")
pillar_card(p2, "◈", "Cost of living", "Rent, utilities, transport",      "cost_score_absolute")
pillar_card(p3, "◉", "Safety",         "Crime + safety indices",          "safety_score")
pillar_card(p4, "◎", "Urban density",  "Population density + congestion", "urban_score")

st.divider()

# ── top 5 — FIXED ─────────────────────────────────────────
st.markdown("<h2 style='margin-bottom:20px'>Current top 5 cities</h2>", unsafe_allow_html=True)

for i, (_, row) in enumerate(top5.iterrows()):
    medal = ["◆", "◇", "◇", "◇", "◇"][i]
    col_medal, col_city, col_country, col_score, col_bar = st.columns([0.3, 2, 2, 1, 3])
    col_medal.markdown(
        f"<span style='color:{GOLD};font-size:16px'>{medal}</span>",
        unsafe_allow_html=True)
    col_city.markdown(
        f"<span style='color:{PARCH};font-size:14px'>{row['city']}</span>",
        unsafe_allow_html=True)
    col_country.markdown(
        f"<span style='color:{MUTED};font-size:12px'>{row['country']}</span>",
        unsafe_allow_html=True)
    col_score.markdown(
        f"<span style='color:{GOLD};font-size:14px;font-weight:500'>{row['livability_score_absolute']:.1f}</span>",
        unsafe_allow_html=True)
    pct = row['livability_score_absolute'] / 100
    col_bar.markdown(f"""
    <div style='background:{BORDER};border-radius:2px;height:6px;margin-top:8px'>
        <div style='background:{GOLD};width:{pct*100:.0f}%;height:100%;border-radius:2px'></div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── methodology note ──────────────────────────────────────
with st.expander("About this index — methodology & data sources"):
    st.markdown(f"""
    <div style='color:{MUTED};font-size:13px;line-height:1.8'>
        <p style='color:{PARCH};font-size:14px;margin-bottom:12px'>How scores are calculated</p>
        <p>Each city is scored across four pillars, each normalized to a 0–100 scale where
        100 is best. The composite score is a weighted average of the four pillar scores.</p>
        <br>
        <p style='color:{GOLD}'>Air quality (default 25%)</p>
        <p>Based on AQI value and PM2.5 concentration. Lower pollution = higher score.
        Source: IQAir / global air pollution dataset.</p>
        <br>
        <p style='color:{GOLD}'>Cost of living (default 30%)</p>
        <p>Two models available — absolute cost (lower rent/utilities = better) and
        affordability ratio (cost relative to local salary). Source: Numbeo.</p>
        <br>
        <p style='color:{GOLD}'>Safety (default 25%)</p>
        <p>Composite of crime index and safety index. Higher safety = higher score.
        Source: Numbeo Crime Index 2023.</p>
        <br>
        <p style='color:{GOLD}'>Urban density (default 20%)</p>
        <p>Uses a moderate-density preference curve — very high and very low density
        both score lower. Combined with traffic congestion data.
        Source: Urban research dataset.</p>
        <br>
        <p style='color:{MUTED};font-size:11px'>
        333 cities · 5 source datasets · Data vintage: 2022–2023
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<p style='font-size:11px;color:{MUTED};text-align:center;margin-top:32px'>
City Livability Index · Built with Python, pandas, SQLite, Plotly & Streamlit
</p>""", unsafe_allow_html=True)