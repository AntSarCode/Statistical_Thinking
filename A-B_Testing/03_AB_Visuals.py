#imports
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#Statistics
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import bootstrap

#SqLite Bridge
conn = sqlite3.connect(r'C:/Users/takis/PycharmProjects/Statistical_Thinking/lendingclub.db')

#SQL Import
query = """

SELECT
    al.variant,
    COUNT(*) AS total_users,
    SUM(al.conversion) AS total_conversions,
    AVG(al.conversion) AS conversion_rate
FROM accepted_loans al
GROUP BY variant;
"""

#DataFrame
df = pd.read_sql_query(query, conn)

#Conversion Arrays
group_A = pd.read_sql_query(
    "SELECT conversion FROM accepted_loans WHERE variant = 'A'", conn)['conversion'].values
group_B = pd.read_sql_query(
    "SELECT conversion FROM accepted_loans WHERE variant = 'B'", conn)['conversion'].values

#Proportions Z-Test
successes = df['total_conversions'].values
n = df['total_users'].values
z_stat, p_val = proportions_ztest(successes, n)

#Bootstrap: Conversion Rate Differential
def boot_diff(a, b, axis):
    return np.mean(b, axis=axis) - np.mean(a, axis=axis)
sample_A = np.random.choice(group_A, size=5000, replace=False)
sample_B = np.random.choice(group_B, size=5000, replace=False)
boot_result = bootstrap(
    (group_A, group_B),
    statistic=boot_diff,
    vectorized=True,
    confidence_level=0.95,
    method='percentile',
    n_resamples=1000
)
ci_low = boot_result.confidence_interval.low.item()
ci_high = boot_result.confidence_interval.high.item()

# -- Chart 1: Bar Plot + Boostrap Error Bars

# Mean conversion rates from bootstrapped samples
mean_A = np.mean(sample_A)
mean_B = np.mean(sample_B)

# Clamp CI bounds
ci_low_clamped = min(ci_low, mean_A, mean_B)
ci_high_clamped = max(ci_high, mean_A, mean_B)

# Error values (ensure non-negative)
error_lower = [max(0, mean_A - ci_low_clamped), max(0, mean_B - ci_low_clamped)]
# noinspection PyTypeChecker
error_upper = [max(0, ci_high_clamped - mean_A), max(0, ci_high_clamped - mean_B)]

# -- Chart 1: Bar Plot + Boostrap Error Bars

plt.errorbar(
    x=[0, 1],
    y=[mean_A, mean_B],
    yerr=[error_lower, error_upper],
    fmt='none', c='black', capsize=5
)

# -- Chart 2: Bootstrap Distribution of Lift --

bootstrap_samples = []
for _ in range(1000):
    b_A = np.random.choice(sample_A, size=5000, replace=True)
    b_B = np.random.choice(sample_B, size=5000, replace=True)
    # noinspection PyTypeChecker
    lift = np.mean(b_B) - np.mean(b_A)
    bootstrap_samples.append(lift)

plt.figure(figsize=[6, 4])
sns.histplot(bootstrap_samples, kde=True, color='skyblue')
plt.axvline(x=0, color='red', linestyle='--', label='Zero Lift')
plt.axvline(ci_low, color='black', linestyle='--', label=f"95% CI [{ci_low:.4f}, {ci_high:.4f}]")
plt.axvline(ci_high, color='black', linestyle='--')
plt.title("Bootstrapped Lift Distribution (B - A)")
plt.xlabel("Lift in Conversion Rate")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()

# -- Chart 3: Error Bars Only (CI as Range) --

plt.figure(figsize=[6, 4])
means = df['conversion_rate'].values
errors = np.abs([
    means - ci_low,
    ci_high - means
])
plt.errorbar(
    ['A', 'B'],
    df['conversion_rate'].values,
    yerr=errors,
    fmt='o',
    capsize=10,
    color='blue',
    ecolor='black',
    linewidth=2
)

plt.title('Conversion Rate with 95% Confidence Interval')
plt.ylabel('Conversion Rate')
plt.grid(True)
plt.tight_layout()
plt.show()

conn.close()