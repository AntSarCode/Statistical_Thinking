#imports
import sqlite3
import pandas as pd
#Statistics
from statsmodels.stats.proportion import proportions_ztest

#SqLite Bridge
conn = sqlite3.connect(r'C:/Users/takis/PycharmProjects/Statistical_Thinking/lendingclub.db')

#SQL Import
query = """
SELECT
    al.variant,
    COUNT(*) AS total_users,
    SUM(al.conversion) AS total_conversions,
    ROUND(AVG(al.conversion) * 100.0, 2) AS conversion_rate_pct
FROM accepted_loans al
GROUP BY variant;
"""

#DataFrame
df = pd.read_sql_query(query, conn)

#Proportions Z-Test
successes = df['total_conversions'].values
n = df['total_users'].values
stat, pval = proportions_ztest(successes, n)

print(f"Z-Statistic: {stat:.3f}")
print(f"P-value: {pval:.4f}")


conn.close()