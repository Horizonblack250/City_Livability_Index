# City Livability Index
### Codename: Project Daedalus

> *Daedalus — the Greek master craftsman who built the Labyrinth. This project is named after him deliberately. Building a livability index is an act of architecture — taking messy CSVs of crime rates, air quality readings, rent prices, and population densities, and turning them into a cohesive blueprint of a city's health. It bridges the gap between cold, hard numbers and the actual human experience of a place.*

---

## Live Demo

**Streamlit App** → [citylivabilityindex.streamlit.app](https://citylivabilityindex-twuqumynbzx7zmnr8qtrjv.streamlit.app/)

**GitHub** → [Horizonblack250/City_Livability_Index](https://github.com/Horizonblack250/City_Livability_Index)

---

## What is this?

A data-driven composite index that ranks **336 global cities** across four pillars of livability — air quality, cost of living, safety, and urban density. The index is fully interactive: adjust the pillar weights and rankings recalculate in real time, reflecting what *you* consider important in a place to live.

This is not a static report. It is a tool.

---

## The Four Pillars

| Pillar | Weight (default) | Source | Logic |
|---|---|---|---|
| Air Quality | 25% | IQAir / Global AQI Dataset | AQI + PM2.5. Lower pollution = higher score |
| Cost of Living | 30% | Numbeo | Two models: absolute cost OR affordability ratio (cost vs local salary) |
| Safety | 25% | Numbeo Crime Index 2023 | Crime index + safety index. Higher safety = higher score |
| Urban Density | 20% | Urban Research Dataset | Moderate density preference curve + traffic congestion |

---

## Key Findings

- Only **59 out of 336 cities (17.6%)** are both safe AND affordable — the dual constraint most people face when choosing where to live
- **238 cities** are affordable but carry elevated crime risk
- **Tampere, Finland** ranks #1 overall — clean air (AQI 31), high safety, reasonable cost, walkable density
- **Delhi, India** ranks last — driven primarily by severe air quality (AQI 170+) and high population density
- **Abu Dhabi** is the world's safest city in this dataset (Safety Index: 100)
- The affordability model tells a different story than absolute cost — **New York** ranks highly on affordability because salaries offset costs, while cheap cities with low wages score poorly
- Rent and salary are strongly positively correlated (r ≈ 0.78) — expensive cities generally pay more

---

## Tech Stack

```
Data Pipeline      Python · pandas · numpy
Database           SQLite (via sqlite3)
Analysis           Jupyter Notebooks · seaborn · matplotlib
Scoring Model      Custom weighted composite index
Web App            Streamlit · Plotly
BI Dashboard       Power BI Desktop
Version Control    Git · GitHub
```

---

## Project Structure

```
City_Livability_Index/
│
├── data/
│   ├── raw/                    ← original source CSVs (untouched)
│   ├── processed/              ← cleaned & merged dataset
│   ├── final/                  ← scored & ranked dataset
│   └── daedalus.db             ← SQLite database
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_scoring_model.ipynb
│   ├── 04_eda.ipynb
│   └── 05_sql_analysis.ipynb
│
├── app/                        ← Streamlit application
│   ├── Home.py
│   ├── pages/
│   │   ├── 01_Map.py
│   │   ├── 02_Leaderboard.py
│   │   ├── 03_Build_Your_Index.py
│   │   └── 04_Compare_Cities.py
│   └── utils/
│       ├── scoring.py
│       └── styles.py
│
├── outputs/
│   ├── charts/                 ← EDA plots + dashboard screenshots
│   └── reports/                ← Power BI .pbix file
│
└── requirements.txt
```

---

## Data Sources

| Dataset | Source | Cities |
|---|---|---|
| Global Air Pollution | Kaggle — IQAir | 23,463 entries |
| Cost of Living | Kaggle — Numbeo | 4,956 cities |
| Population Density & Congestion | Figshare — Urban Research | 513 cities |
| World Crime & Safety Index 2023 | Kaggle — Numbeo | 416 cities |

---

## Methodology

### Data Pipeline
Five datasets were cleaned, standardized, and merged on city name. Key challenges:
- **Column mapping** — the Numbeo dataset uses anonymous column names (x1–x55) requiring manual mapping against official documentation
- **City name standardization** — accent removal, case normalization, and 30+ manual overrides for metro area names (e.g. `dallas-fort worth` → `dallas`)
- **Currency normalization** — identified and corrected systematic data quality issues where some cost columns were in local currency rather than USD
- **Coverage** — after inner joining on cities with real density data, the final dataset covers 336 cities across 94 countries

### Scoring Model
Each pillar is normalized to 0–100 using min-max scaling where 100 = best:
- Air quality: inverted (lower AQI = higher score)
- Cost — absolute: inverted (lower cost = higher score)
- Cost — affordability: monthly living cost as % of local salary, inverted
- Safety: weighted composite of safety index (60%) and inverted crime index (40%)
- Urban density: Gaussian curve peaking at median density — penalizes both extremes

The composite score is a weighted average of the four pillar scores, normalized so weights always sum to 100%.

### SQL Analysis
Six analytical queries were run against the SQLite database, including:
- Hidden gem cities (high livability, rent under $500/month)
- Safety vs affordability quadrant analysis
- Best cities for remote workers (air quality > 60, safety > 60, affordability > 60, rent < $800)

---

## Streamlit App — Features

| Page | What it does |
|---|---|
| Home | Overview, methodology, top 5 cities |
| Global Map | All 336 cities on a choropleth map, colored by score |
| Leaderboard | Top 20 and bottom 20 with full sortable rankings table |
| Build Your Index | Adjust 4 pillar weights → rankings update in real time |
| Compare Cities | Radar chart + raw stats for any 2–4 cities side by side |

---

## Power BI Dashboard — Pages

| Page | Visuals |
|---|---|
| Overview | 4 KPI cards · Top 10 bar chart · City count by country donut |
| Air Quality & Safety | 4 KPI cards · AQI vs Safety scatter plot |
| Cost of Living | 4 KPI cards · Rent vs Salary scatter · Top 10 affordable cities |
| City Explorer | Country slicer · AQI filter · Score range slider · Full data table |

---

## Running Locally

```bash
git clone https://github.com/Horizonblack250/City_Livability_Index.git
cd City_Livability_Index
pip install -r requirements.txt
cd app
streamlit run Home.py
```

---

## Notebooks — Run Order

```
01_data_exploration.ipynb   → understand the raw datasets
02_data_cleaning.ipynb      → clean, standardize, merge
03_scoring_model.ipynb      → build the composite index
04_eda.ipynb                → exploratory analysis + charts
05_sql_analysis.ipynb       → SQL queries on SQLite database
```

---

*Built with Python, pandas, SQLite, Plotly, Streamlit and Power BI.*
*Data vintage: 2022–2023.*
