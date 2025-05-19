"""
This version has IST timezone for the data.
"""

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta


def connect_db():
    return create_engine('sqlite:///stocks_5m.db')


def get_symbols_from_csv(file_path='f_and_o.csv'):
    df = pd.read_csv(file_path)
    df["symbol"] = df["symbol"] + ".NS"
    return df['symbol'].unique()


def create_symbol_table(symbols, engine):
    df = pd.DataFrame({'symbol': symbols})
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'id'}, inplace=True)
    df.to_sql('symbol_table', engine, if_exists='replace', index=False)
    return dict(zip(df['symbol'], df['id']))


def determine_date_range(engine):
    try:
        df = pd.read_sql('SELECT MAX(date) as max_date FROM date_table', engine)
        max_date = df['max_date'][0]
        if pd.isna(max_date):
            raise ValueError
        start = pd.to_datetime(max_date).strftime('%Y-%m-%d')
    except:
        start = (datetime.now() - timedelta(days=50)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    return start, end


def fetch_5min_data(symbols, start_date, end_date):
    all_dates, all_hours, all_minutes = set(), set(), set()
    symbol_data = []

    for symbol in symbols:
        print(f"📥 Fetching {symbol}...")
        try:
            data = yf.download(symbol, start=start_date, end=end_date, interval='5m', progress=False)
        except Exception as e:
            print(f"❌ Failed for {symbol}: {e}")
            continue

        if data.empty:
            print(f"⚠️ No data for {symbol}, skipping.")
            continue

        # Convert to IST
        if data.index.tz is not None:
            data.index = data.index.tz_convert("Asia/Kolkata")
        else:
            data.index = data.index.tz_localize("UTC").tz_convert("Asia/Kolkata")

        # Filter to Indian market hours only
        data = data.between_time("09:15", "15:30")

        data = data.reset_index()[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        data['symbol'] = symbol
        data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'symbol']
        data['date'] = data['datetime'].dt.date
        data['hour'] = data['datetime'].dt.hour
        data['minute'] = data['datetime'].dt.minute

        all_dates.update(data['date'])
        all_hours.update(data['hour'])
        all_minutes.update(data['minute'])

        symbol_data.append(data)

    return symbol_data, all_dates, all_hours, all_minutes


def update_dimension_table(name, values, engine):
    df = pd.DataFrame({name[:-6]: sorted(values)})
    try:
        existing = pd.read_sql(f'SELECT {name[:-6]} FROM {name}', engine)
        df = df[~df[name[:-6]].isin(existing[name[:-6]])]
    except:
        pass
    if not df.empty:
        df.reset_index(drop=True, inplace=True)
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'id'}, inplace=True)
        df.to_sql(name, engine, if_exists='append', index=False)


def get_dimension_maps(engine):
    date_map = dict(zip(pd.to_datetime(pd.read_sql('SELECT * FROM date_table', engine)['date']).dt.date,
                        pd.read_sql('SELECT * FROM date_table', engine)['id']))
    hour_map = dict(zip(pd.read_sql('SELECT * FROM hour_table', engine)['hour'],
                        pd.read_sql('SELECT * FROM hour_table', engine)['id']))
    minute_map = dict(zip(pd.read_sql('SELECT * FROM minute_table', engine)['minute'],
                          pd.read_sql('SELECT * FROM minute_table', engine)['id']))
    return date_map, hour_map, minute_map


def insert_ohlc_data(dataframes, symbol_map, date_map, hour_map, minute_map, engine):
    combined = pd.concat(dataframes, ignore_index=True)
    combined['symbol_id'] = combined['symbol'].map(symbol_map)
    combined['date_id'] = combined['date'].map(date_map)
    combined['hour_id'] = combined['hour'].map(hour_map)
    combined['minute_id'] = combined['minute'].map(minute_map)

    final = combined[['symbol_id', 'date_id', 'hour_id', 'minute_id', 'open', 'high', 'low', 'close', 'volume']]
    final.to_sql('ohlc_5m_table', engine, if_exists='append', index=False)


def main():
    engine = connect_db()
    symbols = get_symbols_from_csv()
    symbol_map = create_symbol_table(symbols, engine)
    start_date, end_date = determine_date_range(engine)

    print(f"📅 Fetching 5m data from {start_date} to {end_date}")
    dataframes, dates, hours, minutes = fetch_5min_data(symbols, start_date, end_date)

    if not dataframes:
        print("🛑 No new data to update.")
        return

    update_dimension_table('date_table', dates, engine)
    update_dimension_table('hour_table', hours, engine)
    update_dimension_table('minute_table', minutes, engine)

    date_map, hour_map, minute_map = get_dimension_maps(engine)
    insert_ohlc_data(dataframes, symbol_map, date_map, hour_map, minute_map, engine)

    print("✅ All 5-minute data inserted and dimension tables updated.")


if __name__ == "__main__":
    main()
