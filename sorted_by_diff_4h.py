import pandas as pd

# df = pd.read_csv('BTCUSD_2023_4h.csv')
# df = df[~df['day_name'].isin(['Saturday', 'Sunday'])]

# df = df.sort_values(by=['difference'], ascending=[False])
# x = df.tail(int(len(df)//24))
# print(len(x))
# y = x['hour'].value_counts()
# print(y)

# x = df.tail(int(len(df)//48))
# print(len(x))
# y = x['hour'].value_counts()
# print(y)



df = pd.read_csv('BTCUSD_2024_4h.csv')
df = df[~df['day_name'].isin(['Saturday', 'Sunday'])]
df = df.sort_values(by=['difference'], ascending=[False])
x = df.tail(int(len(df)//24))
print(len(x))
y = x['hour'].value_counts()
print(y)

x = df.tail(int(len(df)//48))
print(len(x))
y = x['hour'].value_counts()
print(y)

print(df.groupby('hour')['difference'].sum())
