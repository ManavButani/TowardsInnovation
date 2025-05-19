import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

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

# 4. Determine date range
try:
    date_df_existing = pd.read_sql('SELECT MAX(date) as max_date FROM date_table', engine)
    max_date = date_df_existing['max_date'][0]

    if pd.isna(max_date):
        start_date = '2024-01-01'
    else:
        start_date = pd.to_datetime(max_date).strftime('%Y-%m-%d')
except Exception:
    start_date = '2024-01-01'

end_date = datetime.now().strftime('%Y-%m-%d')

print(f"📅 Fetching data from {start_date} to {end_date}")

# 5. Initialize containers
all_dates = set()
symbol_data_list = []

# 6. Fetch and prepare data for each symbol
for symbol in symbols:
    print(f"📥 Downloading data for {symbol}...")
    data = yf.download(symbol, start=start_date, end=end_date, interval='1d')

    if data.empty:
        print(f"⚠️ No data for {symbol}, skipping.")
        continue

    data = data.reset_index()[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    data['symbol'] = symbol
    data.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']

    all_dates.update(data['date'])
    symbol_data_list.append(data)
    print(f"✅ Data fetched for {symbol}")

# Stop if there's no new data
if not symbol_data_list:
    print("🛑 No new data to update.")
    exit()

# 7. Combine all data into one DataFrame
combined_df = pd.concat(symbol_data_list, ignore_index=True)

# 8. Update or create date_table
date_df_new = pd.DataFrame({'date': sorted(all_dates)})
date_df_new = date_df_new[~date_df_new['date'].isin(pd.read_sql('SELECT date FROM date_table', engine)['date'])]
if not date_df_new.empty:
    try:
        existing_dates_df = pd.read_sql('SELECT date FROM date_table', engine)
        existing_dates = pd.to_datetime(existing_dates_df['date'])
        date_df_new = pd.DataFrame({'date': sorted(all_dates)})
        date_df_new = date_df_new[~date_df_new['date'].isin(existing_dates)]
    except Exception:
        # First run, so all dates are new
        date_df_new = pd.DataFrame({'date': sorted(all_dates)})

# Refresh date_id mapping
date_df_all = pd.read_sql('SELECT * FROM date_table', engine)
date_id_map = dict(zip(pd.to_datetime(date_df_all['date']), date_df_all['id']))

# 9. Map foreign keys
combined_df['symbol_id'] = combined_df['symbol'].map(symbol_id_map)
combined_df['date_id'] = combined_df['date'].map(lambda d: date_id_map.get(pd.to_datetime(d)))

# 10. Prepare and insert final OHLC data
ohlc_final = combined_df[['symbol_id', 'date_id', 'open', 'high', 'low', 'close', 'volume']]
ohlc_final.to_sql('ohlc_table', engine, if_exists='append', index=False)

print("🎉 All data successfully updated:")
print("🧩 symbol_table (symbols)")
print("📅 date_table (unique dates)")
print("📊 ohlc_table (linked with symbol_id and date_id)")
