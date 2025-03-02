import pandas as pd
df = pd.read_csv('merged_data.csv')

yesterday_open = df["Open"].shift(1)
df["open %change"] = (yesterday_open - df["Open"]) / yesterday_open * 100

yesterday_low = df["Low"].shift(1)
df["low %change"] = (yesterday_low - df["Open"]) / yesterday_low * 100

df = df[~df["Type"].isin(["CE", "PE"])]
df["Trade"] = df["P/L"].apply(lambda x: 0 if x < 700 else 1)
df = df[['P/L','Close', '% Change', 'Trade', "open %change", "Open", "low %change"]]

df.to_csv('data_class.csv')