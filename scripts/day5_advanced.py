import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs("reports", exist_ok=True)

nav = pd.read_csv("data/processed/returns_computed.csv")
nav['date'] = pd.to_datetime(nav['date'])

# 1. VaR and CVaR
var_rows = []
for code, group in nav.groupby('amfi_code'):
    returns = group['daily_return'].dropna()
    if len(returns) > 30:
        var_95 = round(np.percentile(returns, 5)*100, 3)
        cvar_95 = round(returns[returns <= np.percentile(returns,5)].mean()*100, 3)
        var_rows.append({'amfi_code': code, 'var_95_pct': var_95, 'cvar_95_pct': cvar_95})
var_df = pd.DataFrame(var_rows)
var_df.to_csv("data/processed/var_cvar_report.csv", index=False)
print("VaR and CVaR computed")

# 2. Rolling Sharpe for top 5 funds
top5 = [119551, 120503, 125497, 119092, 120841]
labels = ['SBI Bluechip','ICICI Bluechip','HDFC Top100','Axis Bluechip','Kotak Bluechip']
fig, ax = plt.subplots(figsize=(14,6))
for code, label in zip(top5, labels):
    group = nav[nav['amfi_code']==code].sort_values('date')
    rolling_sharpe = group['daily_return'].rolling(90).mean() / group['daily_return'].rolling(90).std() * np.sqrt(252)
    ax.plot(group['date'], rolling_sharpe, label=label)
ax.set_title('Rolling 90-day Sharpe Ratio')
ax.set_ylabel('Sharpe Ratio')
ax.legend()
plt.tight_layout()
plt.savefig('reports/chart10_rolling_sharpe.png')
plt.close()
print("Rolling Sharpe chart saved")

# 3. Investor cohort analysis
tx = pd.read_csv("data/processed/clean_transactions.csv")
tx['transaction_date'] = pd.to_datetime(tx['transaction_date'])
tx['year'] = tx['transaction_date'].dt.year
cohort = tx.groupby(['investor_id','year']).agg(
    total_invested=('amount_inr','sum'),
    num_transactions=('amount_inr','count')
).reset_index()
cohort_summary = cohort.groupby('year').agg(
    avg_invested=('total_invested','mean'),
    avg_transactions=('num_transactions','mean'),
    num_investors=('investor_id','nunique')
).reset_index()
cohort_summary.to_csv("data/processed/cohort_analysis.csv", index=False)
print("Cohort analysis done")

# 4. Fund Recommender
perf = pd.read_csv("data/raw/07_scheme_performance.csv")
fund_master = pd.read_csv("data/raw/01_fund_master.csv")
merged = perf.merge(fund_master[['amfi_code','risk_category']], on='amfi_code')

def recommend(risk_appetite):
    mapping = {'Low':'Low', 'Moderate':'Moderate', 'High':'High'}
    filtered = merged[merged['risk_category']==mapping[risk_appetite]]
    top3 = filtered.nlargest(3,'sharpe_ratio')[['scheme_name','sharpe_ratio','return_3yr_pct']]
    return top3

print("\nRecommendations for LOW risk investor:")
print(recommend('Low'))
print("\nRecommendations for HIGH risk investor:")
print(recommend('High'))

rec_low = recommend('Low')
rec_low['risk_appetite'] = 'Low'
rec_high = recommend('High')
rec_high['risk_appetite'] = 'High'
pd.concat([rec_low, rec_high]).to_csv("data/processed/recommendations.csv", index=False)

print("\nDay 5 Advanced Analytics Complete!")
