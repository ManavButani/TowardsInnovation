import pandas as pd
import os
import mplfinance as mpf

df = pd.read_csv('BTCUSD_last_few_years_1d.csv')

# Initialize an empty list to store groups
groups = []
group = []

# Loop through the DataFrame and collect rows until 'Sunday' is reached
for index, row in df.iterrows():
    group.append(row)
    
    if row['day_name'] == 'Sunday':
        # When we hit Sunday, append the group and reset
        groups.append(pd.DataFrame(group))
        group = []

# If any leftover group exists (in case the last group doesn't end with Sunday)
if group:
    groups.append(pd.DataFrame(group))

# Example: To display the groups
for i, group in enumerate(groups):
    first = group.iloc[0]
    last = group.iloc[-1]
    first_year = first.year
    first_month = first.month
    first_day = first.day
    last_year = last.year
    last_month = last.month
    last_day = last.day
    directory_path = f"{os.getcwd()}/sat_sun_hug/{str(first_year)}_{str(first_month)}"
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    group.index = pd.to_datetime([f"{first_year}-{first_month}-{first_day}"] * len(group))
    mpf.plot(group, type='candle', style='charles', title=f'{first_day}_{first_month}_{first_year}---{last_day}_{last_month}_{last_year}', ylabel='Price', savefig=os.path.join(directory_path,str(last_day)))