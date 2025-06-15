import pandas as pd
from trading_view_indicators.DMI import DMI

# ---------------- full history ----------------
df_full = pd.read_csv("reliance_1d_spot.csv")
df_full["datetime"] = pd.to_datetime(df_full["date"])
df_full.set_index("datetime", inplace=True)

dmi_full = DMI(df_full, close="close", high="high", low="low")
df_full["dmi_atr"]   = dmi_full.atr(10)
df_full["dmi_adx"], df_full["dmi_plus"], df_full["dmi_minus"] = dmi_full.adx()

# ---------------- last 100 rows ----------------
df_partial = (
    pd.read_csv("reliance_1d_spot.csv")
      .tail(200)                       # grab tail first…
      .assign(datetime=lambda d: pd.to_datetime(d["date"]))
      .set_index("datetime")
)

dmi_part = DMI(df_partial, close="close", high="high", low="low")
df_partial["dmi_atr"]   = dmi_part.atr(10)
df_partial["dmi_adx"], df_partial["dmi_plus"], df_partial["dmi_minus"] = dmi_part.adx()

df_partial = df_partial.iloc[100:]      # keep only the most‑recent 50 rows

# ---------------- comparison helper ----------------
def compare(column: str):
    """Join the two series, then report mean and max‑abs difference."""
    joined = (
        df_full[[column]]                  # full column → give it a suffix
          .join(
              df_partial[[column]],
              how="left",
              lsuffix="_full",
              rsuffix="_partial"
          )
    )

    diff = joined[f"{column}_full"] - joined[f"{column}_partial"]
    diff = diff.dropna()                  # only rows present in both

    print(f"\n{column.upper():8}  rows compared: {len(diff)}")
    print(f"    mean  diff: {diff.mean():.6f}")
    print(f"    max |diff|: {diff.abs().max():.6f}")

for col in ["dmi_atr", "dmi_adx", "dmi_plus", "dmi_minus"]:
    compare(col)
