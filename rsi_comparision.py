import pandas as pd
from tradingview_indicators import RSI  # <- update this with your actual module path
# from .moving_average must already be wired inside the RSI function

# Step 1: Load data
df = pd.read_csv("reliance_1d_spot.csv")
df["datetime"] = pd.to_datetime(df["date"])  # if there's a datetime column
df.set_index("datetime", inplace=True)  # optional, if you'd like datetime as index

# Step 2: Extract close prices
closes = df["close"]

# Step 3: Compare RSI methods
def compare_rsi_methods(
    closes: pd.Series,
    periods: int = 14,
    baseline: str = "rma",
):
    methods = ["sma", "ema", "dema", "tema", "rma"]
    rsi_df = pd.concat(
    {
        f"rsi_{m}": RSI(closes, periods=14 if m == "rma" else 10, ma_method=m)
        for m in methods
    },
        axis=1,
    ).dropna()

    base_col = f"rsi_{baseline}"
    for m in methods:
        if m == baseline:
            continue
        rsi_df[f"diff_to_{m}"] = (rsi_df[base_col] - rsi_df[f"rsi_{m}"])

    return rsi_df

def rsi_summary_stats(rsi_df: pd.DataFrame) -> pd.DataFrame:
    # Calculate daily difference between rma and dema
    rsi_df["abs_diff_dema"] = (rsi_df["rsi_rma"] - rsi_df["rsi_dema"])

    # Sort by difference
    sorted_diff = rsi_df.sort_values("abs_diff_dema", ascending=False)

    # Show top rows
    print(sorted_diff[["rsi_rma", "rsi_dema", "abs_diff_dema"]].head(10))


    return pd.DataFrame({
        col: {
            "max_abs_err": rsi_df[col].max(),
            "min_abs_err": rsi_df[col].min(),
            "mean_abs_err": rsi_df[col].abs().mean()
        }
        for col in rsi_df.columns if col.startswith("diff_to_")
    }).T.sort_values("mean_abs_err")

# Step 4: Run comparison
rsi_result = compare_rsi_methods(closes)
rsi_summary_stats(rsi_result)
# print(rsi_summary_stats(rsi_result))

# Optional: Visual check
# rsi_result[["rsi_rma", "rsi_ema", "rsi_dema", "rsi_tema", "rsi_sma"]].plot(figsize=(12, 5))
