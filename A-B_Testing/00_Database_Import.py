import pandas as pd
from sqlalchemy import create_engine

csv_file_path = r"C:\Users\takis\PycharmProjects\Statistical_Thinking\.venv\accepted_2007_to_2018q4.csv\accepted_2007_to_2018Q4.csv"
db_file_path = r"C:/Users/takis/PycharmProjects/Statistical_Thinking/lendingclub.db"
table_name = 'accepted_loans'

df = pd.read_csv(csv_file_path, low_memory=False)

keep_cols = [
    'id','loan_amnt', 'term', 'int_rate', 'grade', 'sub_grade', 'emp_length',
    'home_ownership', 'annual_inc', 'purpose', 'addr_state', 'dti', 'loan_status',
    'application_type', 'issue_d', 'earliest_cr_line', 'open_acc', 'revol_util', 'total_acc', 'verification_status'
    ]
df_filtered = df[keep_cols]
engine = create_engine(f'sqlite:///{db_file_path}')
df_filtered.to_sql('accepted_loans_cleaned', con=engine, if_exists='replace', index=False)

df.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"Imoprted {len(df)} rows into {db_file_path} as '{table_name}'")