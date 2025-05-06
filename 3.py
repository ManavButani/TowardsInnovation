import pandas as pd

df = pd.read_csv('nifty_50.csv')

# Get unique values for all columns
unique_values = df.apply(lambda x: x.unique())

with open('nifty_50_stocks.txt', 'w') as f:
    f.write(str(list([i + ".NS" for i in unique_values.get("symbol")])))