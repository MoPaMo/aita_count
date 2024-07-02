import pandas as pd

# Read the CSV file
df = pd.read_csv('aita_results_all.csv')
print(df.head())
print(f"Number of rows in aita_results.csv: {len(df)}")

# Print verdict counts
print(df.verdict.value_counts())
# Relative distribution
print(df.verdict.value_counts(normalize=True))

# Extract hour and ensure all hours are represented
df['hour'] = df['time'].str.split(':').str[0]
hourly_counts = df.groupby(df.hour).verdict.value_counts(normalize=True).unstack(fill_value=0)
print(hourly_counts)

# Extract month and ensure all months are represented
df['month'] = df['date'].str.split('-').str[1]
monthly_counts = df.groupby(df.month).verdict.value_counts(normalize=True).unstack(fill_value=0)
print(monthly_counts)

# Extract year and get verdict counts
df['year'] = df['date'].str.split('-').str[0]
yearly_counts = df.groupby(df.year).verdict.value_counts(normalize=False).unstack(fill_value=0)
print(yearly_counts)