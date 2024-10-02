import pandas as pd
import os
import mplfinance as mpf

df = pd.read_csv('BTCUSD_last_few_years_1h_2023.csv')

# Example: To display the groups
for i, group in df[(df['hour'].isin(list(range(4,10))))&(df['day_name'].isin(['Wednesday', 'Thursday']))].groupby(by=['year','month','day']):
    first = group.iloc[0]
    last = group.iloc[-1]
    first_year = first.year
    first_month = first.month
    first_day = first.day
    last_year = last.year
    last_month = last.month
    last_day = last.day
    last_day_name = last.day_name
    directory_path = f"{os.getcwd()}/night_to_morning_wednesday_thrusday/{str(first_year)}_{str(first_month)}_04_09"
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    group.index = pd.to_datetime([f"{first_year}-{first_month}-{first_day}"] * len(group))
    mpf.plot(group, type='candle', style='charles', title=f'{first_day}_{first_month}_{first_year} {last_day_name}', ylabel='Price', savefig=os.path.join(directory_path,str(last_day)))