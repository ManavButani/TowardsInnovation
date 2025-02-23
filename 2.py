import pandas as pd
df = pd.read_csv('merged_data.csv')

yesterday_open = df["Open"].shift(1)
df["open %change"] = (yesterday_open - df["Open"]) / yesterday_open * 100

df = df[~df["Type"].isin(["CE", "PE"])]
df["Trade"] = df["P/L"].apply(lambda x: 0 if x < 700 else 1)
df = df[['Close', '% Change', 'Trade', "open %change", "Open"]]

df.to_csv('data_class.csv')