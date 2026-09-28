# ⚽ Austrian Bundesliga: Tactical Hybrid KPI Platform

A football performance analytics engine integrating **High-Intensity Running (HIR/HSR)** physical metrics with **tactical pressing and turnover events** across the Austrian Bundesliga.

🔗 **Live Interactive App:** [footballhybridanalytics.streamlit.app](https://footballhybridanalytics-96yzzwgqwxbrxgunu74pat.streamlit.app/)

---

## 📌 Methodology & Concept
Traditional metrics evaluate physical distance and event volume in silos. This project implements a **Hybrid Pressing Efficiency (HPE)** framework:
- **Attacking 3rd Pressures (Weight: 1.8x)**: High-danger zone disruption.
- **Midfield Pressures (Weight: 1.0x)**: Build-up delay and transition containment.
- **Turnovers Forced (Weight: 3.0x)**: Net ball recoveries within 5 seconds.
- **Physical Load Normalization**: Calculated per unit of High-Intensity Running.

## 🚀 Key Features
- **Hybrid Decision Matrix**: Scatter-plot mapping physical load vs. weighted tactical threat.
- **Archetype Profiling**: Distinguishes clinical positional pressers (e.g., Guido Burgstaller) from high-volume engines (e.g., Matthias Seidl, Mika Biereth).
- **Player Radar Comparison**: 5-axis head-to-head tactical profile analysis.
- **Export Engine**: Filtered tactical reports exportable to CSV.

## 🛠️ Tech Stack
- **Python 3.12**
- **Streamlit** (Interactive Dashboard)
- **Pandas / NumPy** (Data Modeling)
- **Matplotlib** (Visualizations)

## 💻 Local Setup
```bash
git clone [https://github.com/sacelikk/football_hybrid_analytics.git](https://github.com/sacelikk/football_hybrid_analytics.git)
cd football_hybrid_analytics
pip install -r requirements.txt
streamlit run app.py
