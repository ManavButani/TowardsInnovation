import pandas as pd

# Load VIX data with explicit header handling
vix_df = pd.read_csv("india_vix.csv", skipinitialspace=True)

# Load Trade data
trade_df = pd.read_csv("trade.csv", skipinitialspace=True)

# Trim column names to remove unwanted spaces
vix_df.columns = vix_df.columns.str.strip()
trade_df.columns = trade_df.columns.str.strip()

# Check column names before proceeding
print("VIX Columns:", vix_df.columns)
print("Trade Columns:", trade_df.columns)

# Rename columns if needed
if "Date" not in vix_df.columns:
    print("Error: 'Date' column not found in VIX data. Check CSV formatting.")
else:
    # Convert VIX date format (DD-MMM-YYYY) to datetime
    vix_df["Date"] = pd.to_datetime(vix_df["Date"], format="%d-%b-%Y")

    # Convert Trade date format (YYYY-MM-DD) to datetime
    trade_df["Entry Date"] = pd.to_datetime(trade_df["Entry Date"], format="%Y-%m-%d")

    # Merge on date (renaming for clarity)
    merged_df = trade_df.merge(vix_df, left_on="Entry Date", right_on="Date", how="inner")

    # Drop redundant 'Date' column from VIX data
    merged_df.drop(columns=["Date"], inplace=True)

    # Save the merged data
    merged_df.to_csv("merged_data.csv", index=False)

    print("Merge completed! File saved as merged_data.csv")
