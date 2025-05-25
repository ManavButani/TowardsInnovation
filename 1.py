from tradingview_indicators import *
import pandas as pd
import math
from trading_view_indicators.DMI import DMI
from trading_view_indicators.parabolic_sar import FAST_SAR, SAR
from trading_view_indicators.supertrend import SUPERTREND
df = pd.read_csv("reliance_1d_spot.csv")

# df['rsi_rma'] = RSI(source=df['close'], ma_method="rma")


# macd_result = MACD(
#     source=df['close'],
#     fast_length=12,    # 12-period fast EMA
#     slow_length=26,    # 26-period slow EMA
#     signal_length=9    # 9-period signal line
# )

# df['macd'] = macd_result['macd']
# df['macd_signal'] = macd_result['signal']
# df['macd_histogram'] = macd_result['histogram']

# df['typical_price'] = (df['high'] + df['low'] + df['close'])/3
# df['cci_sma'] = CCI(source=df['typical_price'], method="sma")["CCI"]

DMI_result = DMI(
    dataframe=df,
    close="close",
    high="high",
    low="low"
)

df['dmi_atr'] = DMI_result.atr(10)
# adx, plus, minus =  DMI_result.adx()
# df['dmi_adx'] = adx
# df['dmi_plus'] = plus
# df['dmi_minus'] = minus

# df['parabolic_sar'] = SAR(df, af_start=0.02, af_step=0.02, af_max=0.2)

# df['parabolic_sar'] = FAST_SAR(df['high'].values, df['low'].values)


df.to_csv("reliance_1d_spot_supertrend.csv", index=False)

