import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///stocks.db')

data = yf.download("RELIANCE.NS", start='2023-01-01', end='2025-05-18', interval='1d')

if data.empty:
    print(f"⚠️ No data for RELIANCE.NS, skipping.")
    exit()

data = data.reset_index()[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
data['symbol'] = "RELIANCE.NS"
data.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']

data.to_csv("reliance_1d_spot.csv", index=False)