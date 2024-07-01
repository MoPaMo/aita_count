import pandas as pd
df = pd.read_csv('aita_results.csv')
print(df.head())
print(f"Number of rows in aita_results.csv: {len(df)}")
