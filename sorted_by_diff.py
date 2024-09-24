import pandas as pd

df = pd.read_csv('BTCUSD_last_few_years_1d.csv')
df = df.sort_values(by=['difference'], ascending=[False])
x = df.tail(int(len(df)//7))
print(len(x))
y = x['day_name'].value_counts()
print(y)

x = df.tail(int(len(df)//14))
print(len(x))
y = x['day_name'].value_counts()
print(y)


df = pd.read_csv('BTCUSD_last_few_years_1d.csv')
df = df[df['year']==2024]
df = df.sort_values(by=['difference'], ascending=[False])
x = df.tail(int(len(df)//7))
print(len(x))
y = x['day_name'].value_counts()
print(y)


df = pd.read_csv('BTCUSD_last_few_years_1d.csv')
df = df[df['year']==2024]
df = df.sort_values(by=['difference'], ascending=[False])
x = df.tail(int(len(df)//7))
print(len(x))
y = x['day_name'].value_counts()
print(y)

df = pd.read_csv('BTCUSD_last_few_years_1d.csv')
df = df[df['year']==2023]
df = df.sort_values(by=['difference'], ascending=[False])
x = df.tail(int(len(df)//7))
print(len(x))
y = x['day_name'].value_counts()
print(y)