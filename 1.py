import pandas as pd
import json

df = pd.read_csv("f_and_o.csv")

# Group by sector and create dictionary
sector_dict = df.groupby('sector')['symbol'].apply(lambda x: list(set(x))).to_dict()

with open('sector_stocks.txt', 'w') as f:
    json.dump(sector_dict, f, indent=4)