import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

engine = create_engine("sqlite:///stocks.db")

# from_date = "2025-04-10 00:00:00.000000"
from_date = datetime.now() - timedelta(days=14)
from_date = from_date.strftime("%Y-%m-%d")


# 1. Load all necessary data
ohlc = pd.read_sql("SELECT * FROM ohlc_table", engine)
symbols = pd.read_sql("SELECT * FROM symbol_table", engine)
dates = pd.read_sql(f"SELECT * FROM date_table where date >= '{from_date}'", engine)

symbols.set_index('id', inplace=True)
dates.set_index('id', inplace=True)

# 2. Merge symbol and date info
merged = ohlc.merge(symbols, left_on='symbol_id', right_index=True)
merged = merged.merge(dates, left_on='date_id', right_index=True)
merged['date'] = pd.to_datetime(merged['date'])

# 3. Sort for time-based ops
merged.sort_values(['symbol', 'date'], inplace=True)

# 4. Compute weekly data for each symbol (based on end-of-week days)
def compute_weekly(df):
    df = df.copy()
    df.set_index('date', inplace=True)

    # Use label='left' to use first date of the week (Monday by default)
    weekly = df.resample('W-MON', label='left', closed='left').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna().reset_index()

    weekly['symbol'] = df['symbol'].iloc[0]
    return weekly

weekly_all = pd.concat([
    compute_weekly(g) for _, g in merged.groupby('symbol')
])

weekly_all['pct_change'] = weekly_all.groupby('symbol')['close'].pct_change() * 100

# 5. Apply filtering logic on actual daily dates
results = []

for symbol, daily_df in merged.groupby('symbol'):
    daily_df = daily_df.sort_values('date').reset_index(drop=True)
    weekly_df = weekly_all[weekly_all['symbol'] == symbol].sort_values('date').reset_index(drop=True)

    for i in range(2, len(daily_df)):
        day1 = daily_df.iloc[i - 1]  # One day ago
        today = daily_df.iloc[i]

        # Find the closest previous two *weekly* closes before 'today'
        prev_weeks = weekly_df[weekly_df['date'] < today['date']]
        if len(prev_weeks) < 2:
            continue

        prev_week = prev_weeks.iloc[-2]
        latest_week = prev_weeks.iloc[-1]

        # Convert the latest_week with the today close
        # 1. 1 week ago % change < 5
        pct_change = (latest_week['close'] - prev_week['close']) / prev_week['close'] * 100
        if pct_change >= 5:
            continue

        # 2. weekly close > prev week high
        if (latest_week['close'] <= prev_week['high']):
            continue

        # 3. weekly close > day1 close * 1.02
        if latest_week['close'] <= day1['close'] * 1.02:
            continue

        # 4. today Open >= day1 low
        if today['open'] >= day1['low']:
            results.append({
                'date': today['date'],
                'symbol': symbol
            })


# 6. Save results to DB or return as DataFrame
passed_df = pd.DataFrame(results).drop_duplicates()
if not passed_df.empty:
    passed_df.sort_values('date', inplace=True)

    passed_df.to_csv(f"bullish_for_week_{datetime.now()}.csv")


# Optional: save to DB
# passed_df.to_sql("passed_stock_days", engine, if_exists="replace", index=False)

print("✅ Final dates where all conditions passed saved to 'passed_stock_days'")