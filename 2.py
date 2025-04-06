import pandas as pd

df = pd.read_csv('f_and_o.csv')

# Get unique values for all columns
unique_values = df.apply(lambda x: x.unique())

print(unique_values.get("symbol"))
