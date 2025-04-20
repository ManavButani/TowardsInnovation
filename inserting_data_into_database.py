import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

# 1. Connect to SQLite database
engine = create_engine('sqlite:///stocks.db')

# 2. Read symbols from CSV and format them
df = pd.read_csv('f_and_o.csv')
df["symbol"] = df["symbol"] + ".NS"
symbols = df['symbol'].unique()

# 3. Create and insert into symbol_table
symbol_df = pd.DataFrame({'symbol': symbols})
symbol_df.reset_index(inplace=True)
symbol_df.rename(columns={'index': 'id'}, inplace=True)
symbol_df.to_sql('symbol_table', engine, if_exists='replace', index=False)

# Create a mapping: symbol -> symbol_id
symbol_id_map = dict(zip(symbol_df['symbol'], symbol_df['id']))

# 4. Initialize containers
all_dates = set()
symbol_data_list = []

# 5. Fetch and prepare data for each symbol
for symbol in symbols:
    print(f"📥 Downloading data for {symbol}...")
    data = yf.download(symbol, start='2025-01-01', end='2025-04-20', interval='1d')

    if data.empty:
        print(f"⚠️ No data for {symbol}, skipping.")
        continue

    data = data.reset_index()[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    data['symbol'] = symbol
    data.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']

    all_dates.update(data['date'])
    symbol_data_list.append(data)
    print(f"✅ Data fetched for {symbol}")

# 6. Combine all data into one DataFrame
combined_df = pd.concat(symbol_data_list, ignore_index=True)

# 7. Create and insert into date_table
date_df = pd.DataFrame({'date': sorted(all_dates)})
date_df.reset_index(inplace=True)
date_df.rename(columns={'index': 'id'}, inplace=True)
date_df.to_sql('date_table', engine, if_exists='replace', index=False)

# Create a mapping: date -> date_id
date_id_map = dict(zip(date_df['date'], date_df['id']))

# 8. Map foreign keys
combined_df['symbol_id'] = combined_df['symbol'].map(symbol_id_map)
combined_df['date_id'] = combined_df['date'].map(date_id_map)

# 9. Prepare and insert final OHLC data
ohlc_final = combined_df[['symbol_id', 'date_id', 'open', 'high', 'low', 'close', 'volume']]
ohlc_final.to_sql('ohlc_table', engine, if_exists='replace', index=False)

print("🎉 All data successfully inserted into:")
print("🧩 symbol_table (symbols)")
print("📅 date_table (unique dates)")
print("📊 ohlc_table (linked with symbol_id and date_id)")
