from datetime import date
from jugaad_data.nse import stock_df

df = stock_df(
    symbol="SBIN",
    from_date=date(2023, 1, 1),  # Replace with your desired start date
    to_date=date(2023, 1, 30),  # Replace with your desired end date
    interval="5min",
    series="EQ"  # Or "FO" for futures and options
)

print(df)  # Print to console
# df.to_csv("sbin_data.csv")  # Save to CSV