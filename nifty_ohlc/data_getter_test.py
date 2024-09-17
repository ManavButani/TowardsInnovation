import yfinance as yf
import pandas as pd

# Fetch 5-minute interval data for the last 60 days
data = yf.download('^NSEI', period='5y', interval='5m')

# Convert the index to a DatetimeIndex if not already
data.index = pd.to_datetime(data.index)

# # Filter the data for exactly 60 days ago
# sixty_days_ago = pd.Timestamp.now() - pd.Timedelta(days=60)
# data_60_days_ago = data.loc[sixty_days_ago.strftime('%Y-%m-%d')]

# # Display the filtered data
# print(data_60_days_ago)
