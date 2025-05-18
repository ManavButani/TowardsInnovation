import pandas as pd
import tradingview_indicators as ta

df = pd.read_csv("reliance_1d_spot.csv")

# Add RSI
df['rsi'] = ta.RSI(df['close'], periods=14)

# Add MACD - if it returns a DataFrame
macd_df = ta.MACD(df['close'], fast_length=12, slow_length=26, signal_length=9)
df['macd'] = macd_df['macd']
df['macd_signal'] = macd_df['signal']
df['macd_histogram'] = macd_df['histogram']

# Add Bollinger Bands - if it returns a DataFrame
bb_df = ta.bollinger_bands(df['close'], length=20, mult=2)
df['bb_upper'] = bb_df['upper']
df['bb_middle'] = bb_df['basis']
df['bb_lower'] = bb_df['lower']

# Add EMA and SMA
df['ema'] = ta.ema(df['close'], length=20)
df['sma'] = ta.sma(df['close'], length=20)

# Save to CSV
df.to_csv("reliance_1d_spot_indicators.csv", index=False)
