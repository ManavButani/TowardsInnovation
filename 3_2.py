import pandas as pd
df = pd.read_csv('merged_data.csv') 
df = df[~df['% Change'].between(-10, 10) & ~df["Type"].isin(["CE", "PE"]) & ~df['Vix'].between(12, 15)]
df.to_csv('hari.csv')