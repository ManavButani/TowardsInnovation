from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def job():
    print(f"🔁 Running job at {datetime.now()}")

scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=10)
scheduler.start()

print("🚀 Scheduler started.")
try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("🛑 Scheduler stopped.")
