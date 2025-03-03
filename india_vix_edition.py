import pandas as pd
df = pd.read_csv('hist_india_vix_-02-03-2024-to-02-03-2025.csv')

df.columns = df.columns.str.strip()

yesterday_open = df["Open"].shift(1)
df["open %change"] = (df["Open"] - yesterday_open) / yesterday_open * 100


yesterday_low = df["Low"].shift(1)
df["low %change"] = (df["Open"] - yesterday_low) / yesterday_open * 100


yesterday_high = df["High"].shift(1)
df["high %change"] = (df["Open"] - yesterday_high) / yesterday_open * 100

df = df[['Date', "open %change", 'low %change', "high %change", "Open"]]
df.to_csv("india_test_data.csv", index=False)