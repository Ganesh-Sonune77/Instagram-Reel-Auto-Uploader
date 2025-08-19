# log.py
import json
from datetime import datetime
from threading import Lock
from dotenv import load_dotenv
import os

load_dotenv()
HISTORY_FILE = os.getenv("UPLOAD_HISTORY")
log_lock = Lock()

def log_history(filename, status):
    entry = {
        "time": datetime.now().isoformat(),
        "reel": filename,
        "status": status
    }
    with log_lock:
        try:
            with open(HISTORY_FILE, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        except FileNotFoundError:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([entry], f, indent=2)

def trim_history():
    try:
        with open(HISTORY_FILE, "r+", encoding="utf-8") as f:
            data = json.load(f)
            if len(data) > 50:
                data = data[-50:]
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
    except:
        pass

def get_recent_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)[-50:]
    except:
        return []
