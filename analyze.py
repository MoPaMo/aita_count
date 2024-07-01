import pandas as pd
df = pd.read_csv('aita_results.csv')
print(df.head())
print(f"Number of rows in aita_results.csv: {len(df)}")

print(df.verdict.value_counts())
#relative distribution
print(df.verdict.value_counts(normalize=True))
# only store hour for time
df['hour'] = df['time'].str.split(':').str[0]


print(df.groupby(df.hour).verdict.value_counts(normalize=True))

# only store month for date
df['month'] = df['date'].str.split('-').str[1]


print(df.groupby(df.month).verdict.value_counts(normalize=True))