"""
This version has IST timezone for the data. Resume download from the last saved datetime.
"""

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta, time
import pytz

IST = pytz.timezone("Asia/Kolkata")
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 25)  # last interval is 3:25 PM

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


def get_latest_saved_datetime(engine):
    try:
        query = """
        SELECT d.date, h.hour, m.minute
        FROM ohlc_5m_table o
        JOIN date_table d ON o.date_id = d.id
        JOIN hour_table h ON o.hour_id = h.id
        JOIN minute_table m ON o.minute_id = m.id
        ORDER BY d.date DESC, h.hour DESC, m.minute DESC
        LIMIT 1
        """
        df = pd.read_sql(query, engine)
    except:
        return None

    if df.empty:
        return None

    latest_date = df.iloc[0]['date']
    latest_hour = int(df.iloc[0]['hour'])
    latest_minute = int(df.iloc[0]['minute'])

    # Construct datetime in IST
    dt_naive = datetime.combine(pd.to_datetime(latest_date).date(), time(latest_hour, latest_minute))
    dt_ist = IST.localize(dt_naive)
    print(f"Latest saved datetime: {dt_ist}")
    return dt_ist


def determine_date_range(engine):
    now_ist = datetime.now(IST)
    latest_dt = get_latest_saved_datetime(engine)

    # If no data in DB, start 50 days ago
    if latest_dt is None:
        start = (now_ist - timedelta(days=50)).replace(
            hour=MARKET_OPEN.hour, minute=MARKET_OPEN.minute, second=0, microsecond=0
        )
    else:
        # Already up to date for today
        if latest_dt.date() == now_ist.date() and latest_dt.time() >= MARKET_CLOSE:
            print("✅ Database is already up to date.")
            return None, None

        # Continue from next slot
        start = latest_dt + timedelta(minutes=5)

        # If after market close, shift to next market open
        if start.time() > MARKET_CLOSE:
            start = start + timedelta(days=1)
            start = start.replace(hour=MARKET_OPEN.hour, minute=MARKET_OPEN.minute, second=0, microsecond=0)

    # Skip weekends/holidays: move start to next weekday if needed
    while start.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        start += timedelta(days=1)
        start = start.replace(hour=MARKET_OPEN.hour, minute=MARKET_OPEN.minute)

    # If start is in future, no update needed
    if start.date() > now_ist.date() or (start.date() == now_ist.date() and start.time() > MARKET_CLOSE):
        print("✅ No new data to download. Already up to date.")
        return None, None

    # Define end time: today @ 15:25 or now, whichever is earlier
    if now_ist.time() > MARKET_CLOSE:
        end = now_ist.replace(hour=MARKET_CLOSE.hour, minute=MARKET_CLOSE.minute, second=0, microsecond=0)
    else:
        end = now_ist

    # Convert to UTC (naive) for yfinance
    start_utc = start.astimezone(pytz.UTC).replace(tzinfo=None)
    end_utc = end.astimezone(pytz.UTC).replace(tzinfo=None)

    print(f"📅 Fetching from {start_utc} to {end_utc} (UTC)")
    return start_utc, end_utc


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
