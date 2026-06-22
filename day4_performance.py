import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs("reports", exist_ok=True)

nav = pd.read_csv("data/processed/clean_nav.csv")
nav['date'] = pd.to_datetime(nav['date'])
nav = nav.sort_values(['amfi_code','date'])

nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()
nav.to_csv("data/processed/returns_computed.csv", index=False)
print("Daily returns computed")

rf = 0.065/252
sharpe_rows = []
sortino_rows = []
dd_rows = []

for code, group in nav.groupby('amfi_code'):
    returns = group['daily_return'].dropna()
    if len(returns) > 30:
        excess = returns - rf
        sharpe = (excess.mean() / returns.std()) * np.sqrt(252)
        sharpe_rows.append({'amfi_code': code, 'sharpe_ratio': round(sharpe,3)})
        downside = returns[returns < 0].std()
        sortino = (excess.mean() / downside) * np.sqrt(252) if downside > 0 else 0
        sortino_rows.append({'amfi_code': code, 'sortino_ratio': round(sortino,3)})
    roll_max = group['nav'].cummax()
    drawdown = (group['nav'] - roll_max) / roll_max
    dd_rows.append({'amfi_code': code, 'max_drawdown_pct': round(drawdown.min()*100,2)})

pd.DataFrame(sharpe_rows).to_csv("data/processed/sharpe_values.csv", index=False)
pd.DataFrame(sortino_rows).to_csv("data/processed/sortino_values.csv", index=False)
pd.DataFrame(dd_rows).to_csv("data/processed/max_drawdown.csv", index=False)
print("Sharpe, Sortino, Max Drawdown computed")

perf = pd.read_csv("data/raw/07_scheme_performance.csv")
scorecard = perf[['amfi_code','scheme_name','return_3yr_pct','sharpe_ratio','alpha','expense_ratio_pct','max_drawdown_pct']].copy()
scorecard['return_rank'] = scorecard['return_3yr_pct'].rank(pct=True)
scorecard['sharpe_rank'] = scorecard['sharpe_ratio'].rank(pct=True)
scorecard['alpha_rank'] = scorecard['alpha'].rank(pct=True)
scorecard['expense_rank'] = 1 - scorecard['expense_ratio_pct'].rank(pct=True)
scorecard['drawdown_rank'] = 1 - scorecard['max_drawdown_pct'].rank(pct=True)
scorecard['composite_score'] = (
    scorecard['return_rank']*0.30 +
    scorecard['sharpe_rank']*0.25 +
    scorecard['alpha_rank']*0.20 +
    scorecard['expense_rank']*0.15 +
    scorecard['drawdown_rank']*0.10
) * 100
scorecard['composite_score'] = scorecard['composite_score'].round(1)
scorecard = scorecard.sort_values('composite_score', ascending=False)
scorecard.to_csv("data/processed/fund_scorecard.csv", index=False)
print("Fund scorecard created")

fig, ax = plt.subplots(figsize=(12,6))
top10 = scorecard.head(10)
ax.barh(top10['scheme_name'], top10['composite_score'], color='steelblue')
ax.set_title('Top 10 Funds by Composite Score')
ax.set_xlabel('Score (0-100)')
plt.tight_layout()
plt.savefig('reports/chart9_fund_scorecard.png')
plt.close()
print("Chart saved!")
print("\nDay 4 Complete!")
