import pandas as pd
df = pd.read_csv('./india_vix.csv')

df.columns = df.columns.str.strip()

yesterday_open = df["Open"].shift(1)
df["open %change"] = (df["Open"] - yesterday_open) / yesterday_open * 100


yesterday_low = df["Low"].shift(1)
df["low %change"] = (df["Open"] - yesterday_low) / yesterday_open * 100


yesterday_high = df["High"].shift(1)
df["high %change"] = (df["Open"] - yesterday_high) / yesterday_open * 100


df.to_csv("india_vix_updated_version.csv")