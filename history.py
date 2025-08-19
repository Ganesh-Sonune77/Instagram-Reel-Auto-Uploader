# history.py
import json
from datetime import datetime

def log_history(reel, status):
    entry = {
        "time": datetime.now().isoformat(),
        "reel": reel,
        "status": status
    }
    try:
        with open("history.json", "r+") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except:
        with open("history.json", "w") as f:
            json.dump([entry], f, indent=2)
