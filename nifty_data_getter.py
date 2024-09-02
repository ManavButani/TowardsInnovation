import yfinance as yf
import pandas as pd
ticker_symbol = '^NSEI'
df = yf.download(ticker_symbol, start='2022-06-01', end='2022-12-31', interval='1h')
df.index.name = df.index.name.lower()
df.columns = df.columns.str.lower()


df['year'] = df.index.year
df['month'] = df.index.month
df['hour'] = df.index.hour
df['day_name'] = df.index.day_name()
df['max'] = df[['open', 'high', 'low', 'close']].max(axis=1)
df['min'] = df[['open', 'high', 'low', 'close']].min(axis=1)
df['difference'] = df['max'] - df['min']
df['candle_body'] = df['open'] - df['close']
df['high_shadow'] = df['high'] - df['open']
df['low_shadow'] = df['close'] - df['low']
df['trend'] = df['candle_body'].apply(lambda x: "UP" if x > 0 else "ZERO" if x == 0 else "DOWN")
df.to_csv('nifty_1h_2022.csv', index=False)
