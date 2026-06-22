import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("reports", exist_ok=True)

nav = pd.read_csv("data/processed/clean_nav.csv")
nav['date'] = pd.to_datetime(nav['date'])
fund_master = pd.read_csv("data/raw/01_fund_master.csv")
aum = pd.read_csv("data/raw/03_aum_by_fund_house.csv")
sip = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")
transactions = pd.read_csv("data/processed/clean_transactions.csv")
performance = pd.read_csv("data/raw/07_scheme_performance.csv")
folio = pd.read_csv("data/raw/06_industry_folio_count.csv")

# Chart 1: NAV trend for 5 funds
fig, ax = plt.subplots(figsize=(12,6))
top5 = [119551, 120503, 125497, 119092, 120841]
labels = ['SBI Bluechip','ICICI Bluechip','HDFC Top100','Axis Bluechip','Kotak Bluechip']
for code, label in zip(top5, labels):
    data = nav[nav['amfi_code']==code].sort_values('date')
    ax.plot(data['date'], data['nav'], label=label)
ax.set_title('NAV Trend 2022-2026')
ax.set_xlabel('Date')
ax.set_ylabel('NAV (Rs.)')
ax.legend()
plt.tight_layout()
plt.savefig('reports/chart1_nav_trend.png')
plt.close()
print("Chart 1 done")

# Chart 2: AUM by fund house
fig, ax = plt.subplots(figsize=(12,6))
aum['date'] = pd.to_datetime(aum['date'])
latest_aum = aum.groupby('fund_house')['aum_lakh_crore'].max().sort_values(ascending=False)
latest_aum.plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('AUM by Fund House (Latest)')
ax.set_ylabel('AUM (Lakh Crore)')
ax.set_xlabel('Fund House')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('reports/chart2_aum_by_fundhouse.png')
plt.close()
print("Chart 2 done")

# Chart 3: SIP inflow trend
fig, ax = plt.subplots(figsize=(12,6))
sip['month'] = pd.to_datetime(sip['month'])
ax.plot(sip['month'], sip['sip_inflow_crore'], color='green', marker='o', markersize=3)
ax.set_title('Monthly SIP Inflow Trend 2022-2025')
ax.set_ylabel('SIP Inflow (Rs. Crore)')
ax.set_xlabel('Month')
plt.tight_layout()
plt.savefig('reports/chart3_sip_trend.png')
plt.close()
print("Chart 3 done")

# Chart 4: Age group distribution
fig, ax = plt.subplots(figsize=(8,8))
age_counts = transactions['age_group'].value_counts()
ax.pie(age_counts.values, labels=age_counts.index, autopct='%1.1f%%')
ax.set_title('Investor Age Group Distribution')
plt.tight_layout()
plt.savefig('reports/chart4_age_distribution.png')
plt.close()
print("Chart 4 done")

# Chart 5: SIP amount by state
fig, ax = plt.subplots(figsize=(10,8))
state_sip = transactions[transactions['transaction_type']=='SIP'].groupby('state')['amount_inr'].sum().sort_values()
state_sip.plot(kind='barh', ax=ax, color='coral')
ax.set_title('SIP Amount by State')
ax.set_xlabel('Total Amount (INR)')
plt.tight_layout()
plt.savefig('reports/chart5_sip_by_state.png')
plt.close()
print("Chart 5 done")

# Chart 6: Folio count growth
fig, ax = plt.subplots(figsize=(12,6))
folio['month'] = pd.to_datetime(folio['month'])
ax.plot(folio['month'], folio['total_folios_crore'], color='purple', marker='o')
ax.set_title('Total MF Folio Count Growth')
ax.set_ylabel('Folios (Crore)')
plt.tight_layout()
plt.savefig('reports/chart6_folio_growth.png')
plt.close()
print("Chart 6 done")

# Chart 7: Sharpe ratio comparison
fig, ax = plt.subplots(figsize=(12,6))
perf = performance.merge(fund_master[['amfi_code','scheme_name']], on='amfi_code')
top_sharpe = perf.nlargest(10,'sharpe_ratio')
ax.barh(top_sharpe['scheme_name'], top_sharpe['sharpe_ratio'], color='teal')
ax.set_title('Top 10 Funds by Sharpe Ratio')
ax.set_xlabel('Sharpe Ratio')
plt.tight_layout()
plt.savefig('reports/chart7_sharpe_ratio.png')
plt.close()
print("Chart 7 done")

# Chart 8: Transaction type split
fig, ax = plt.subplots(figsize=(8,8))
tx_type = transactions['transaction_type'].value_counts()
ax.pie(tx_type.values, labels=tx_type.index, autopct='%1.1f%%', colors=['#2196F3','#4CAF50','#FF5722'])
ax.set_title('Transaction Type Split')
plt.tight_layout()
plt.savefig('reports/chart8_transaction_split.png')
plt.close()
print("Chart 8 done")

print("\nAll 8 charts saved in reports/ folder!")
