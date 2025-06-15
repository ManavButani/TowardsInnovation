import pandas as pd
from tradingview_indicators import RSI          # adjust import as needed

# ---------- full history ----------
df_full = pd.read_csv("bhel_1d_spot.csv")
df_full["datetime"] = pd.to_datetime(df_full["date"])
df_full.set_index("datetime", inplace=True)

df_full["rsi_full"] = RSI(df_full["close"], periods=14)

# ---------- last 66 rows ----------
df_partial = (
    pd.read_csv("bhel_1d_spot.csv")
      .tail(100)
      .assign(datetime=lambda d: pd.to_datetime(d["date"]))
      .set_index("datetime")
)

df_partial["rsi_partial"] = RSI(df_partial["close"], periods=14)
df_partial = df_partial.iloc[50:]

# ---------- align on the index ----------
# Option 1: use .join (cleanest when the index is already aligned)
df_combined = (
    df_full[["rsi_full"]]              # keep just the column we need
        .join(df_partial[["rsi_partial"]], how="left")
)

# Option 2: with merge (identical result)
# df_combined = df_full[["rsi_full"]].merge(
#     df_partial[["rsi_partial"]], left_index=True, right_index=True, how="left"
# )

# Option 3: concat works too
# df_combined = pd.concat([df_full["rsi_full"], df_partial["rsi_partial"]], axis=1)

print(df_combined.tail(10))   # show the most‑recent 10 rows


# Only keep rows where both RSI values are not NaN
valid = df_combined.dropna(subset=["rsi_full", "rsi_partial"])

# Mean difference (can be signed)
mean_diff = (valid["rsi_full"] - valid["rsi_partial"]).mean()

# Maximum absolute difference
max_abs_diff = (valid["rsi_full"] - valid["rsi_partial"]).abs().max()

print(f"Mean difference: {mean_diff:.6f}")
print(f"Max absolute difference: {max_abs_diff:.6f}")
