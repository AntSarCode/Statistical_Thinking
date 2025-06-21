#imports
import sqlite3
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

#SqLite Bridge
conn = sqlite3.connect(r'C:/Users/takis/PycharmProjects/Statistical_Thinking/lendingclub.db')

#SQL Import
df = pd.read_sql_query("""
SELECT
    variant,
    COUNT(*) AS total_users,
    SUM(conversion) AS total_conversions,
    AVG(conversion) AS conversion_rate
FROM accepted_loans
GROUP BY variant;
""", conn)

# -- Prepare lift distribution (sampled for dashboard speed) --
group_A = pd.read_sql_query("SELECT conversion FROM accepted_loans WHERE variant = 'A'", conn)['conversion'].sample(5000).values
group_B = pd.read_sql_query("SELECT conversion FROM accepted_loans WHERE variant = 'B'", conn)['conversion'].sample(5000).values

boot_lifts = []
for _ in range(500):
    b_A = np.random.choice(group_A, size=5000, replace=True)
    b_B = np.random.choice(group_B, size=5000, replace=True)
    boot_lifts.append(np.mean(b_B) - np.mean(b_A))

conn.close()

# -- DASH APP --
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("A/B Test Dashboard - Lending Club", style={"textAlign": "center"}),

    dcc.Tabs([
        dcc.Tab(label='Conversion Rates', children=[
            dcc.Graph(
                figure=px.bar(
                    df,
                    x='variant',
                    y='conversion_rate',
                    color='variant',
                    text=df['conversion_rate'].round(3),
                    labels={'conversion_rate': 'Conversion Rate'},
                    title='Conversion Rate by Variant'
                )
            )
        ]),

        dcc.Tab(label='Lift Distribution', children=[
            dcc.Graph(
                figure=px.histogram(
                    boot_lifts,
                    nbins=50,
                    title="Bootstrapped Lift Distribution (B - A)",
                    labels={'value': 'Lift in Conversion Rate'},
                ).add_vline(
                    x=0, line_dash='dash', line_color='red', annotation_text='Zero Lift', annotation_position='top left'
                )
            )
        ]),

        dcc.Tab(label='Confidence Intervals', children=[
            dcc.Graph(
                figure=go.Figure([
                    go.Scatter(
                        x=['A', 'B'],
                        y=df['conversion_rate'],
                        error_y=dict(
                            type='data',
                            symmetric=False,
                            array=[0.015, 0.015],  # Placeholder values for visual purposes
                            arrayminus=[0.015, 0.015]
                        ),
                        mode='markers',
                        marker=dict(size=10, color='blue')
                    )
                ]).update_layout(
                    title="Conversion Rates with 95% Confidence Intervals",
                    yaxis_title="Conversion Rate",
                    xaxis_title="Variant"
                )
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
