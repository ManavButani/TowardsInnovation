import yfinance as yf

# Function to get futures contract expiry dates for a given symbol
def get_futures_expiry(symbol):
    try:
        asset = yf.Ticker(symbol)
        expirations = asset.options  # Returns list of expiration dates
        return expirations
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Example: Gold futures
gold_symbol = "GC=F"  # Gold Futures symbol in Yahoo Finance
gold_expiry = get_futures_expiry(gold_symbol)

print("Gold Expirations:", gold_expiry)

# Example: Bitcoin Futures
bitcoin_symbol = "BTC-USD"  # You might need a proper symbol from a data provider
bitcoin_expiry = get_futures_expiry(bitcoin_symbol)

print("Bitcoin Expirations:", bitcoin_expiry)
