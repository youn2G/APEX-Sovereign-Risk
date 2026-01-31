# 🛰️ APEX: Sovereign Risk Intelligence Terminal

**APEX** is a quantitative monitoring solution designed to model and forecast global macro-financial stress. It aggregates multi-factor data to provide a unified risk score for sovereign entities.

## 🎯 Project Vision
In an increasingly volatile global economy, traditional static reports are insufficient. **APEX** transforms raw data from international institutions (IMF, World Bank) into an interactive, predictive terminal for decision-makers.

## 🧠 Key Features
- **Dynamic Risk Scoring:** A composite index based on 4 pillars: Solvency, Liquidity, Stability, and Inflation.
- **Predictive Engine (ML):** Implementation of a Time-Series regression model to forecast risk trajectories at 6 months.
- **Geospatial Analytics:** High-contrast command map for immediate identification of global risk clusters.
- **Institutional UI/UX:** Minimalist terminal design inspired by Bloomberg and Reuters.

## 💻 Tech Stack
- **Backend:** Python 3.10
- **Data & ML:** Pandas, NumPy, Scikit-Learn (Linear Regression & EMA)
- **Frontend:** Streamlit with Custom CSS (Dark Mode / Institutional Purple)
- **Visuals:** Plotly (Radar Charts & Choropleth Maps)

## 🛠️ Setup
1. `pip install -r requirements.txt`
2. `streamlit run app.py`

---
*Developed by Youn Goger-Le Goux*