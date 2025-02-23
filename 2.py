import pandas as pd
df = pd.read_csv('merged_data.csv') 
df = df[~df["Type"].isin(["CE", "PE"])]
df["Trade"] = df["P/L"].apply(lambda x: 0 if x < 700 else 1)
df = df[['Close', '% Change', 'Trade']]

df.to_csv('data_class.csv')