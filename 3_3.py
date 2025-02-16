import pandas as pd
df = pd.read_csv('merged_data.csv') 
df = df[~df['% Change'].between(-10, 10) & ~df["Type"].isin(["CE", "PE"])]
df.to_csv('krenil.csv')