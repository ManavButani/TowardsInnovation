from jugaad_data.nse import NSELive

# Initialize NSELive
n = NSELive()

# Replace 'RELIANCE' with the desired stock symbol
stock_symbol = "ANGELONE"

# Fetch live stock data
quote = n.stock_quote(stock_symbol)
print(quote)

# Extract and display relevant price information
price_info = quote.get("priceInfo", {})
print(f"Stock: {stock_symbol}")
print(f"Last Price: {price_info.get('lastPrice')}")
print(f"Change: {price_info.get('change')}")
print(f"Percent Change: {price_info.get('pChange')}%")
print(f"Open: {price_info.get('open')}")
print(f"Day High: {price_info.get('intraDayHighLow', {}).get('max')}")
print(f"Day Low: {price_info.get('intraDayHighLow', {}).get('min')}")
