import pandas as pd
df = pd.read_csv('merged_data.csv') 
df = df[(df['% Change'] > 10) & ~df['Vix'].between(12, 15) & ~df["Type"].isin(["CE", "PE"])]
df.to_csv('manav.csv')