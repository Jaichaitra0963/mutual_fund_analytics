-- 1. Top 5 funds by 3yr return
SELECT scheme_name, return_3yr_pct 
FROM fact_performance fp
JOIN dim_fund df ON fp.amfi_code = df.amfi_code
ORDER BY return_3yr_pct DESC LIMIT 5;

-- 2. Average NAV per month for HDFC Top 100
SELECT strftime('%Y-%m', date) as month, ROUND(AVG(nav),2) as avg_nav
FROM fact_nav WHERE amfi_code = 125497
GROUP BY month ORDER BY month;

-- 3. Total SIP inflow per year
SELECT substr(month,1,4) as year, ROUND(SUM(sip_inflow_crore),2) as total_sip
FROM fact_sip GROUP BY year ORDER BY year;

-- 4. Transactions by state
SELECT state, COUNT(*) as total_tx, ROUND(SUM(amount_inr)/1000000,2) as total_amt_million
FROM fact_transactions GROUP BY state ORDER BY total_tx DESC;

-- 5. Funds with expense ratio less than 1%
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

-- 6. Top 5 funds by Sharpe ratio
SELECT df.scheme_name, fp.sharpe_ratio
FROM fact_performance fp
JOIN dim_fund df ON fp.amfi_code = df.amfi_code
ORDER BY sharpe_ratio DESC LIMIT 5;

-- 7. AUM by fund house latest quarter
SELECT fund_house, ROUND(MAX(aum_lakh_crore),2) as latest_aum
FROM fact_aum GROUP BY fund_house
ORDER BY latest_aum DESC;

-- 8. SIP transaction count by age group
SELECT age_group, COUNT(*) as count, ROUND(AVG(amount_inr),2) as avg_amount
FROM fact_transactions WHERE transaction_type='SIP'
GROUP BY age_group ORDER BY age_group;

-- 9. Funds with highest max drawdown risk
SELECT df.scheme_name, fp.max_drawdown_pct
FROM fact_performance fp
JOIN dim_fund df ON fp.amfi_code = df.amfi_code
ORDER BY max_drawdown_pct LIMIT 5;

-- 10. Category wise transaction volume
SELECT category, COUNT(*) as transactions, ROUND(SUM(amount_inr)/10000000,2) as crore
FROM fact_transactions ft
JOIN dim_fund df ON ft.amfi_code = df.amfi_code
GROUP BY category ORDER BY crore DESC;
