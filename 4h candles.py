import pandas as pd
import os
import mplfinance as mpf

df = pd.read_csv('BTC_USD_4_HOUR_DF.csv')
# df = df[(df['hour'].isin([3,4,5,6,7,8,9,10,11,12,13]))&(~df['day_name'].isin(['Sunday','Saturday']))]


# Example: To display the groups
for i, group in df.groupby(by=['year','month','day']):
    first = group.iloc[0]
    last = group.iloc[-1]
    first_year = first.year
    first_month = first.month
    first_day = first.day
    directory_path = f"{os.getcwd()}/4H/{str(first_year)}_{str(first_month)}"
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    group.index = pd.to_datetime([f"{first_year}-{first_month}-{first_day}"] * len(group))
    mpf.plot(group, type='candle', style='charles', title=f'{first_day}_{first_month}_{first_year}', ylabel='Price', savefig=os.path.join(directory_path,str(first_day)))