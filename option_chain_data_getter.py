import deribit_api

client = deribit_api.RestClient()

# Get BTC options instruments
btc_options = client.getinstruments(currency='BTC', kind='option')

for option in btc_options:
    print(f"Strike: {option['strike']}, Expiry: {option['expiration_timestamp']}, Option Type: {option['option_type']}")
