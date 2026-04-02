import pandas as pd
import sqlite3
import os

DB_PATH   = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'daedalus.db')
FINAL_CSV = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'final', 'daedalus_scored.csv')

import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv(FINAL_CSV)
    df['city'] = df['city'].str.title()
    return df

def compute_scores(df, w_air, w_cost, w_safety, w_urban, cost_model='absolute'):
    weights_sum = w_air + w_cost + w_safety + w_urban
    if weights_sum == 0:
        return df

    cost_col = 'cost_score_absolute' if cost_model == 'absolute' else 'cost_score_affordability'

    df = df.copy()
    df['livability_score'] = (
        df['air_quality_score'] * (w_air    / weights_sum) +
        df[cost_col]            * (w_cost   / weights_sum) +
        df['safety_score']      * (w_safety / weights_sum) +
        df['urban_score']       * (w_urban  / weights_sum)
    ).round(2)

    df['rank'] = df['livability_score'].rank(ascending=False).astype(int)
    return df.sort_values('rank')

PILLAR_COLORS = {
    'air_quality_score': '#4C9BE8',
    'cost_score':        '#F4A623',
    'safety_score':      '#2ECC71',
    'urban_score':       '#9B59B6',
}