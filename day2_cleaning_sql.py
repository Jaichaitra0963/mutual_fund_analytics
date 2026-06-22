import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

# Load all datasets
fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")
aum = pd.read_csv("data/raw/03_aum_by_fund_house.csv")
sip = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")
category = pd.read_csv("data/raw/05_category_inflows.csv")
folio = pd.read_csv("data/raw/06_industry_folio_count.csv")
performance = pd.read_csv("data/raw/07_scheme_performance.csv")
transactions = pd.read_csv("data/raw/08_investor_transactions.csv")
holdings = pd.read_csv("data/raw/09_portfolio_holdings.csv")
benchmark = pd.read_csv("data/raw/10_benchmark_indices.csv")

# Clean nav_history
nav_history['date'] = pd.to_datetime(nav_history['date'])
nav_history = nav_history.sort_values(['amfi_code','date'])
nav_history = nav_history.drop_duplicates()
nav_history = nav_history[nav_history['nav'] > 0]
nav_history.to_csv("data/processed/clean_nav.csv", index=False)
print(f"clean_nav: {nav_history.shape}")

# Clean transactions
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
transactions = transactions[transactions['amount_inr'] > 0]
transactions = transactions.drop_duplicates()
transactions.to_csv("data/processed/clean_transactions.csv", index=False)
print(f"clean_transactions: {transactions.shape}")

# Clean performance
performance = performance.dropna(subset=['sharpe_ratio'])
performance.to_csv("data/processed/clean_performance.csv", index=False)
print(f"clean_performance: {performance.shape}")

# Save all others
fund_master.to_csv("data/processed/clean_fund_master.csv", index=False)
aum.to_csv("data/processed/clean_aum.csv", index=False)
sip.to_csv("data/processed/clean_sip.csv", index=False)
benchmark.to_csv("data/processed/clean_benchmark.csv", index=False)
holdings.to_csv("data/processed/clean_holdings.csv", index=False)

# Create SQLite database
engine = create_engine('sqlite:///data/db/bluestock_mf.db')
os.makedirs("data/db", exist_ok=True)
engine = create_engine('sqlite:///data/db/bluestock_mf.db')

fund_master.to_sql('dim_fund', engine, if_exists='replace', index=False)
nav_history.to_sql('fact_nav', engine, if_exists='replace', index=False)
transactions.to_sql('fact_transactions', engine, if_exists='replace', index=False)
performance.to_sql('fact_performance', engine, if_exists='replace', index=False)
aum.to_sql('fact_aum', engine, if_exists='replace', index=False)
sip.to_sql('fact_sip', engine, if_exists='replace', index=False)
benchmark.to_sql('fact_benchmark', engine, if_exists='replace', index=False)
holdings.to_sql('fact_holdings', engine, if_exists='replace', index=False)

print("\nDatabase created successfully!")
print("All tables loaded into bluestock_mf.db")
