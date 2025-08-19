# uploader.py — PRODUCTION PATCHED (Hindi Edition)

from instagrapi import Client, exceptions
from log import log_history, trim_history
from dotenv import load_dotenv
from pathlib import Path
import os, json, time, tempfile
from inspect import signature

# 🧠 Environment Load
load_dotenv()
REEL_FOLDER   = os.getenv("REEL_FOLDER")
TITLE_FOLDER  = os.getenv("TITLE_FOLDER")
STATUS_FILE   = os.getenv("STATUS_FILE", "status.json")

# ✅ Mandatory check
if not REEL_FOLDER or not TITLE_FOLDER:
    raise EnvironmentError("❌ .env में REEL_FOLDER और TITLE_FOLDER ज़रूरी हैं")

# 📁 Path normalization
REEL_FOLDER  = Path(REEL_FOLDER).expanduser().resolve()
TITLE_FOLDER = Path(TITLE_FOLDER).expanduser().resolve()
STATUS_FILE  = Path(STATUS_FILE).resolve()

# 📦 Ensure folders exist
REEL_FOLDER.mkdir(parents=True, exist_ok=True)
TITLE_FOLDER.mkdir(parents=True, exist_ok=True)

# 🔒 Atomic write helper
def _atomic_dump(data: dict, dest: Path):
    tmp = dest.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(dest)

# 🔁 Status update
def update_upload_status(reel: str, percent: int, status: str):
    _atomic_dump({"upload": {"reel": reel, "percent": percent, "status": status}}, STATUS_FILE)

# 🔍 Login test (unchanged)
def test_login(username: str, password: str) -> bool:
    if not username or not password:
        raise ValueError("Username और Password चाहिए")

    try:
        client = Client()
        client.set_user_agent("Instagram 250.0.0.17.114 Android")
        client.login(username, password)
        print(f"[✓] Login successful for {username}")
        return True
    except Exception as e:
        print(f"[x] Login failed: {e}")
        return False
    

def safe_video_upload(client, path, caption, progress_cb):
    sig = signature(client.video_upload)
    try:
        if "progress_callback" in sig.parameters:
            return client.video_upload(str(path), caption, progress_callback=progress_cb)
        else:
            return client.video_upload(str(path), caption)
    except Exception as e:
        import subprocess
        subprocess.run(["pip", "install", "moviepy>=1.0.3"])
        return client.video_upload(str(path), caption)
    

# 📤 Reel uploader
def upload_one_reel(reel: str, username: str, password: str):
    reel_path    = REEL_FOLDER / reel
    title_file   = Path(reel).with_suffix(".txt").name
    caption_path = TITLE_FOLDER / title_file

    try:
        if not reel_path.exists():
            raise FileNotFoundError(f"🎞️ Reel गायब: {reel_path}")
        if not caption_path.exists():
            raise FileNotFoundError(f"📝 Caption नहीं मिला: {caption_path}")

        with caption_path.open(encoding="utf-8") as f:
            caption = f.read().strip()

        client = Client()
        client.set_user_agent("Instagram 250.0.0.17.114 Android")
        client.login(username, password)

        # 🔄 Upload progress callback
        def _progress(current, total):
            pct = int(current / total * 100)
            update_upload_status(reel, pct, "uploading")

        update_upload_status(reel, 0, "uploading")
        # uploader.py  में client.video_upload() कॉल बदल दो

        try:
            safe_video_upload(client, reel_path, caption, _progress)

        except TypeError:
            # पुराना instagrapi: progress_callback supported नहीं है
            client.video_upload(str(reel_path), caption)

        
        update_upload_status(reel, 100, "done")

        log_history(reel, "✅ Success")
        reel_path.unlink(missing_ok=True)
        caption_path.unlink(missing_ok=True)
        trim_history()

    except (exceptions.ClientLoginRequired, exceptions.ClientError) as e:
        update_upload_status(reel, 0, "failed")
        log_history(reel, f"🚫 InstagrapiError: {e}")
    except Exception as e:
        update_upload_status(reel, 0, "failed")
        log_history(reel, f"🔥 Failed: {type(e).__name__}: {e}")
        raise
