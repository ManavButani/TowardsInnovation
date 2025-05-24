from apscheduler.schedulers.background import BackgroundScheduler
from jugaad_data.nse import NSELive
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import time


# Initialize
n = NSELive()
engine = create_engine('sqlite:///stocks_5m.db')
symbols = ["RELIANCE", "TCS", "ANGELONE"]  # Load from DB or CSV in prod


def fetch_and_store():
    print(f"⏰ Fetching data at {datetime.now().strftime('%H:%M:%S')}")
    records = []

    for symbol in symbols:
        try:
            data = n.stock_quote(symbol)
            info = data['priceInfo']
            records.append({
                'symbol': symbol,
                'timestamp': datetime.now(),
                'open': info['open'],
                'high': info['intraDayHighLow']['max'],
                'low': info['intraDayHighLow']['min'],
                'close': info['lastPrice'],
                'change': info['change'],
                'pchange': info['pChange'],
                'volume': info.get('totalTradedVolume')
            })
        except Exception as e:
            print(f"❌ Error for {symbol}: {e}")

    if records:
        df = pd.DataFrame(records)
        df.to_sql('live_ohlc_table', engine, if_exists='append', index=False)
        print(f"✅ Inserted {len(records)} records.")
    else:
        print("⚠️ No data fetched.")


# Scheduler setup
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store, 'interval', minutes=5)
    scheduler.start()

    print("🚀 Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("🛑 Scheduler stopped.")


if __name__ == "__main__":
    start_scheduler()
