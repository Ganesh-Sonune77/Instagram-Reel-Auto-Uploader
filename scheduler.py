from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from uploader import upload_one_reel
from dotenv import load_dotenv
import os, json

load_dotenv()
REEL_FOLDER = os.getenv("REEL_FOLDER")
STATUS_FILE = "status.json"
scheduler = BackgroundScheduler()

def get_interval_seconds(value, unit):
    if unit == "m": return value * 60
    if unit == "h": return value * 3600
    if unit == "d": return value * 86400

def set_schedule(value, unit, username, password):
    os.makedirs(REEL_FOLDER, exist_ok=True)
    reels = sorted(f for f in os.listdir(REEL_FOLDER) if f.endswith(".mp4"))
    if not reels:
        print("⚠️ No reels found.")
        return

    interval = get_interval_seconds(int(value), unit)
    if interval <= 0:
        print("❌ Invalid interval value.")
        return

    start_time = datetime.now()
    for index, reel in enumerate(reels):
        run_time = start_time + timedelta(seconds=interval * index)
        if index == 0:
            with open(STATUS_FILE, "r+", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except:
                    data = {}
                data["next_upload"] = run_time.isoformat()
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()

        scheduler.add_job(
            upload_one_reel,
            'date',
            run_date=run_time,
            args=[reel, username, password],
            id=f"{reel}_{run_time.isoformat()}",
            replace_existing=True
        )
        print(f"🎬 Scheduled: {reel} at {run_time.strftime('%H:%M:%S')}")

    if not scheduler.running:
        scheduler.start()
