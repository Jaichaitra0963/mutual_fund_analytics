# Bluestock Fintech - Mutual Fund Analytics Platform

## Project Overview
End-to-End Mutual Fund Analytics Platform built for Bluestock Fintech Capstone Project.

## Tech Stack
- Python, Pandas, NumPy, Matplotlib, Seaborn
- SQLite, SQLAlchemy
- Git, GitHub

## Project Structure
- data/raw/ — Original 10 CSV datasets
- data/processed/ — Cleaned and computed data
- data/db/ — SQLite database
- reports/ — Charts and visualizations

## How to Run
```bash
pip install -r requirements.txt
python data_ingestion.py
python day2_cleaning_sql.py
python day3_eda.py
python day4_performance.py
python day5_advanced.py
```

## Key Results
- 40 mutual fund schemes analyzed
- 46,000+ NAV data points processed
- 32,000+ investor transactions analyzed
- 10 SQL analytical queries
- 10 visualization charts
- Fund scorecard and recommender built

## Deliverables
- data_ingestion.py
- live_nav_fetch.py
- day2_cleaning_sql.py — Cleaned data + SQLite DB
- day3_eda.py — 8 EDA charts
- day4_performance.py — Sharpe, Sortino, CAGR, Scorecard
- day5_advanced.py — VaR, CVaR, Cohort Analysis, Recommender
