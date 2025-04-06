import pandas as pd

# Sample data (you can replace this with your own DataFrame)
# TESTING OF 6TH APRIL SO DATE IS WRONG
data = {
    'date': pd.date_range(start='2024-01-01', periods=10, freq='W'),
    'value': [896.8, 894.8, 844.65, 852.35, 829, 871.65, 801.55, 855.85, 896.75, 941.55]
}
df = pd.DataFrame(data)

# Set the date as index (optional but useful for time series)
df.set_index('date', inplace=True)

# Calculate week-over-week percentage change
df['pct_change_week'] = df['value'].pct_change(periods=1) * 100

# Show the result
print(df)


import pandas as pd

series = pd.Series([896.8, 894.8, 844.65, 852.35, 829, 871.65, 801.55, 855.85, 896.75, 941.55])

# Manual pct_change
previous = series.shift(1)
pct_change = (series - previous) / previous * 100

print(pct_change)
