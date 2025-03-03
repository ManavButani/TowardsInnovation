import yfinance as yf
import pandas as pd


start_date =  '2025-01-01'
end_date = '2025-03-01'

ticker_symbol = '^INDIAVIX'
df = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1m')
df.index.name = df.index.name.lower()
df.columns = df.columns.str.lower()

df['year'] = df.index.year.astype(int)
df['month'] = df.index.month.astype(int)
df['day'] = df.index.day.astype(int)
df['day_name'] = df.index.day_name()
df['minute'] = df.index.minute.astype(int)
df['hour'] = df.index.hour.astype(int)
df['max'] = df[['open', 'high', 'low', 'close']].max(axis=1)
df['min'] = df[['open', 'high', 'low', 'close']].min(axis=1)
df['difference'] = df['max'] - df['min']
df['candle_body'] = df['open'] - df['close']
df['high_shadow'] = df['high'] - df[['open', 'close']].max(axis=1)
df['low_shadow'] = df['low'] - df[['open', 'close']].min(axis=1)
df['low-open'] = df['low'] - df['open']
df['high-open'] = df['high'] - df['open']
df['trend'] = df['candle_body'].apply(lambda x: "UP" if x < 0 else "ZERO" if x == 0 else "DOWN")

df.to_csv('BTCUSD_last_few_years_1h_2023.csv', index=True)