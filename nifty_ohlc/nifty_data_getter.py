import yfinance as yf
import pandas as pd


ticker_symbol = '^NSEI'
start_date =  '2024-09-01'
end_date = '2024-09-21'

df = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
df.index.name = df.index.name.lower()
df.columns = df.columns.str.lower()


df['year'] = df.index.year
df['month'] = df.index.month
df['hour'] = df.index.hour
df['day'] = df.index.day
df['day_name'] = df.index.day_name()
df['hour'] = df.index.hour
df['minute'] = df.index.minute
df['hour'] = df.index.hour
df['max'] = df[['open', 'high', 'low', 'close']].max(axis=1)
df['min'] = df[['open', 'high', 'low', 'close']].min(axis=1)
df['difference'] = df['max'] - df['min']
df['candle_body'] = df['open'] - df['close']
df['high_shadow'] = df['high'] - df[['open', 'close']].max(axis=1)
df['low_shadow'] = df['low'] - df[['open', 'close']].min(axis=1)
df['low-open'] = df['low'] - df['open']
df['high-open'] = df['high'] - df['open']
df['trend'] = df['candle_body'].apply(lambda x: "DOWN" if x < 0 else "ZERO" if x == 0 else "UP")
df.to_csv('./nifty_ohlc/nifty_1d_september_2024.csv', index=True)


# df = yf.download(ticker_symbol, start=start_date, end=end_date, interval='5m')
# df.index.name = df.index.name.lower()
# df.columns = df.columns.str.lower()


# df['year'] = df.index.year
# df['month'] = df.index.month
# df['hour'] = df.index.hour
# df['day'] = df.index.day
# df['day_name'] = df.index.day_name()
# df['max'] = df[['open', 'high', 'low', 'close']].max(axis=1)
# df['min'] = df[['open', 'high', 'low', 'close']].min(axis=1)
# df['difference'] = df['max'] - df['min']
# df['candle_body'] = df['open'] - df['close']
# df['high_shadow'] = df['high'] - df['open']
# df['low_shadow'] = df['close'] - df['low']
# df['trend'] = df['candle_body'].apply(lambda x: "UP" if x > 0 else "ZERO" if x == 0 else "DOWN")
# df.to_csv('./nifty_ohlc/nifty_5m_august_2024.csv', index=True)