from concurrent.futures import ThreadPoolExecutor, as_completed
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



def fetch_symbol(symbol):
    try:
        data = n.stock_quote(symbol)
        info = data['priceInfo']
        return {
            'symbol': symbol,
            'timestamp': datetime.now(),
            'open': info['open'],
            'high': info['intraDayHighLow']['max'],
            'low': info['intraDayHighLow']['min'],
            'close': info['lastPrice'],
            'change': info['change'],
            'pchange': info['pChange'],
            'volume': info.get('totalTradedVolume')
        }
    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
        return None

def fetch_and_store():
    print(f"🔄 Job triggered at {datetime.now()}")
    try:
        records = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_symbol, sym) for sym in symbols]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    records.append(result)

        if records:
            df = pd.DataFrame(records)
            df.to_sql('live_ohlc_table', engine, if_exists='append', index=False)
            print(f"✅ Inserted {len(records)} records at {datetime.now()}")
        else:
            print("⚠️ No data fetched.")
    except Exception as e:
        print(f"🔥 Unexpected error in job: {e}")


# Scheduler setup
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store, 'interval', minutes=1)
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
