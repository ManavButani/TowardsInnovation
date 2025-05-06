import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

engine = create_engine("sqlite:///stocks.db")

nifty_stocks = ['BAJFINANCE.NS', 'BEL.NS', 'CIPLA.NS', 'SBIN.NS', 'TITAN.NS', 'DRREDDY.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'TRENT.NS', 'GRASIM.NS', 'ONGC.NS', 'RELIANCE.NS', 'HINDALCO.NS', 'TATASTEEL.NS', 'LT.NS', 'M&M.NS', 'TATAMOTORS.NS', 'HINDUNILVR.NS', 'NESTLEIND.NS', 'TATACONSUM.NS', 'ASIANPAINT.NS', 'ITC.NS', 'EICHERMOT.NS', 'WIPRO.NS', 'APOLLOHOSP.NS', 'SHRIRAMFIN.NS', 'ADANIENT.NS', 'JIOFIN.NS', 'NIFTY.NS', 'SUNPHARMA.NS', 'SBILIFE.NS', 'HDFCLIFE.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'AXISBANK.NS', 'HCLTECH.NS', 'BHARTIARTL.NS', 'MARUTI.NS', 'ULTRACEMCO.NS', 'TCS.NS', 'NTPC.NS', 'TECHM.NS', 'POWERGRID.NS', 'ADANIPORTS.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'COALINDIA.NS', 'ZOMATO.NS']

# 1. Load all necessary data
ohlc = pd.read_sql("SELECT * FROM ohlc_table", engine)
symbols = pd.read_sql("SELECT * FROM symbol_table", engine)
dates = pd.read_sql(f"SELECT * FROM date_table", engine)

symbols.isin(nifty_stocks)
symbols.set_index('id', inplace=True)
dates.set_index('id', inplace=True)

# 2. Merge symbol and date info
merged = ohlc.merge(symbols, left_on='symbol_id', right_index=True)
merged = merged.merge(dates, left_on='date_id', right_index=True)
merged['date'] = pd.to_datetime(merged['date'])

# 3. Sort for time-based ops
merged.sort_values(['symbol', 'date'], inplace=True)


merged['pct_change'] = merged.groupby('symbol')['close'].pct_change() * 100

merged.sort_values(by=["date", "pct_change"], ascending=[True, False], inplace=True)
merged = merged[~merged['pct_change'].isna()]
merged = merged[["symbol", "date", "pct_change"]]
merged.to_csv(f"index_performer_{datetime.now()}.csv", index=False)
