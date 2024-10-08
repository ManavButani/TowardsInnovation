import pandas as pd
import os
import mplfinance as mpf

df = pd.read_csv('BTCUSD_last_few_years_1h_2023.csv')
df = df[(df['hour'].isin([12,13,14,15,16,17,18]))&(~df['day_name'].isin(['Sunday','Saturday']))]


# Example: To display the groups
for i, group in df.groupby(by=['year','month','day']):
    first = group.iloc[0]
    last = group.iloc[-1]
    first_year = first.year
    first_month = first.month
    first_day = first.day
    directory_path = f"{os.getcwd()}/630_730/{str(first_year)}_{str(first_month)}"
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    group.index = pd.to_datetime([f"{first_year}-{first_month}-{first_day}"] * len(group))
    mpf.plot(group, type='candle', style='charles', title=f'{first_day}_{first_month}_{first_year}', ylabel='Price', savefig=os.path.join(directory_path,str(first_day)))