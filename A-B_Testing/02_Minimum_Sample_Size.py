#imports
import sqlite3
import pandas as pd
#Statistics
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

#SqLite Bridge
conn = sqlite3.connect(r'C:/Users/takis/PycharmProjects/Statistical_Thinking/lendingclub.db')

#SQL Import
query = """
SELECT
    COUNT(*) AS n,
    SUM(al.conversion) AS conversions,
    ROUND(AVG(al.conversion), 4) AS conversion_rate
FROM accepted_loans al
WHERE variant = 'A';
"""

#DataFrame
df = pd.read_sql_query(query, conn)

#Baseline Rate
p1 = float(df['conversion_rate'][0])
#Rise (absolute)
mde = 0.02
#Target Rate: 'B'
p2 = p1 + mde

#Variables
effect_size = proportion_effectsize(p1, p2)
analysis = NormalIndPower()
sample_size = analysis.solve_power(
    effect_size=effect_size,
    power = 0.80,
    alpha = 0.05,
    alternative='two-sided'
)

#Sample Size Condition
print(f"Minimum sample size per group: {round(sample_size)}")


conn.close()