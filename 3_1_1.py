import pandas as pd
df = pd.read_csv('data_class.csv') 
df = df[(df['open %change'] > 10) & ~df['Open'].between(12, 15)]
df.to_csv('3_1_1.csv')