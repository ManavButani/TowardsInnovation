import requests
from datetime import datetime, timedelta
import math
import pandas as pd


valid_intervals = ["1m","5m","15m","10m","1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]

company_name = input("Enter Company Name::" ) or "WIPRO" 
company_name += ".BO"
total_days = int(input("Enter Total Number of Days")) or 7
interval = input("Enter interval") or "1m"

if interval not in valid_intervals:
  print("Invalid Interval:::", interval)
  exit()

start_time = ""
end_time = ""
current_time = datetime.now()

if start_time:
  start_time = math.ceil(datetime.timestamp(current_time - timedelta(days=total_days)))

if not end_time:
  # Convert current time to a timestamp
  end_time = math.ceil(datetime.timestamp(current_time))
  print("end_time:", current_time)

url = f"https://query2.finance.yahoo.com/v8/finance/chart/{company_name}?period1={start_time}&period2={end_time}&interval={interval}&includePrePost=true&events=div%7Csplit%7Cearn&&lang=en-US&region=US"



payload = {}
headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'cookie': 'A1=d=AQABBGMiZGYCEA6mVsU3tsuikDzIZ17QItgFEgEBAQFzZWZuZlkPyyMA_eMAAA&S=AQAAAkRRIzuUW5q1ttRVxkMia2Y; A3=d=AQABBGMiZGYCEA6mVsU3tsuikDzIZ17QItgFEgEBAQFzZWZuZlkPyyMA_eMAAA&S=AQAAAkRRIzuUW5q1ttRVxkMia2Y; A1S=d=AQABBGMiZGYCEA6mVsU3tsuikDzIZ17QItgFEgEBAQFzZWZuZlkPyyMA_eMAAA&S=AQAAAkRRIzuUW5q1ttRVxkMia2Y; cmp=t=1717838438&j=0&u=1---; gpp=DBAA; gpp_sid=-1; axids=gam=y-W.xNEUNE2uJZitqUMURHF0eoETd66Ftz~A&dv360=eS1wSExCa1QxRTJ1RzNjR3ZRTENwU0tkc05aTDZLR2lqc35B&ydsp=y-uLcjyvNE2uKgDBJENbFfN1v7g7sluMNC~A&tbla=y-kiTywH1E2uJIyIHICIPW7nqx5OduZvlN~A; tbla_id=ebb4b35b-c461-4416-90a7-d68103893e7d-tuctd5da7e7; PRF=t%3DSUZLON.BO',
  'origin': 'https://finance.yahoo.com',
  'priority': 'u=1, i',
  'referer': 'https://finance.yahoo.com/quote/SUZLON.BO/',
  'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)
result = response.json().get("chart").get("result")[0]
timestamp = result.get("timestamp")
indicators = result.get("indicators").get("quote")[0]

df = pd.DataFrame({
    'time': list(map(lambda x: datetime.utcfromtimestamp(x) + timedelta(hours=5,minutes=30), timestamp)),
    'open': indicators.get('open'),
    'high':indicators.get('high'),
    'low':indicators.get('low'),
    'close':indicators.get('close'),
    'volume':indicators.get('volume')
})

print(df)
# print(response.text)
