import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

performance = pd.read_csv("data/raw/07_scheme_performance.csv")
top_sharpe = performance.nlargest(10,'sharpe_ratio')

fig, ax = plt.subplots(figsize=(12,6))
ax.barh(top_sharpe['scheme_name'], top_sharpe['sharpe_ratio'], color='teal')
ax.set_title('Top 10 Funds by Sharpe Ratio')
ax.set_xlabel('Sharpe Ratio')
plt.tight_layout()
plt.savefig('reports/chart7_sharpe_ratio.png')
plt.close()
print("Chart 7 done!")

transactions = pd.read_csv("data/processed/clean_transactions.csv")
fig, ax = plt.subplots(figsize=(8,8))
tx_type = transactions['transaction_type'].value_counts()
ax.pie(tx_type.values, labels=tx_type.index, autopct='%1.1f%%', colors=['#2196F3','#4CAF50','#FF5722'])
ax.set_title('Transaction Type Split')
plt.tight_layout()
plt.savefig('reports/chart8_transaction_split.png')
plt.close()
print("Chart 8 done!")
print("All charts complete!")
