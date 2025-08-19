🎬 Instagram Reel Auto-Uploader

An automated Instagram Reel scheduling and uploading tool built with Flask, APScheduler, and Instagrapi.
This app allows you to:

Log in securely with Instagram credentials

Schedule bulk reel uploads at fixed intervals

Track real-time upload progress and status

Maintain an upload history with success/failure logs

Automatically remove uploaded reels and captions

🚀 Features

✅ Login & Session Handling – Secure login with your Instagram account
✅ Upload Scheduling – Schedule reels at custom intervals (minutes, hours, days)
✅ Automatic Cleanup – Deletes reel + caption after successful upload
✅ Upload Progress Tracking – Real-time progress shown via status.json
✅ Upload History – Maintains history.json log with last 50 events
✅ Web Dashboard – Flask-based UI with Login, Dashboard & Status pages
✅ Error Handling – Detects missing files, bad credentials, API errors

🛠️ Tech Stack

Backend: Flask + APScheduler

Instagram API: instagrapi

Frontend: HTML (layout, login, dashboard, status pages)

Utilities: dotenv for environment config, Pillow for images, moviepy for video support

📂 Project Structure
├── app.py              # Flask app (routes, login, UI, scheduler integration)
├── uploader.py         # Core uploader logic (upload reels + captions)
├── scheduler.py        # Scheduling jobs via APScheduler
├── log.py              # Thread-safe logging (history.json)
├── history.py          # Legacy logging helper
├── requirements.txt    # Python dependencies
├── history.json        # Upload history log (success/fail status)
├── status.json         # Live upload progress
└── (create your own .env file – not included for security)

⚙️ Setup
1️⃣ Clone Repository
git clone https://github.com/Ganesh-Sonune77/Instagram-Reel-Auto-Uploader.git
cd Instagram-Reel-Auto-Uploader

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Create .env File

⚠️ Important: The .env file is not included in this repo.
You must create it manually in the project root:

SECRET_KEY=your_flask_secret
REEL_FOLDER=/absolute/path/to/static/reels
TITLE_FOLDER=/absolute/path/to/static/titles
UPLOAD_HISTORY=history.json
STATUS_FILE=status.json


REEL_FOLDER → folder containing .mp4 reel videos

TITLE_FOLDER → folder containing matching .txt caption files

Example: reel1.mp4 → reel1.txt

4️⃣ Run App
flask run


App will be available at:
👉 http://127.0.0.1:5000

🎯 Usage

Open the app in browser

Login with Instagram username + password

Navigate to Dashboard

Enter upload interval (e.g., 10 minutes)

The system will:

Pick reels from REEL_FOLDER

Match captions from TITLE_FOLDER

Upload them in order at defined intervals

View progress on Status page

📜 Logging

status.json → live progress (reel name, % uploaded, status)

history.json → permanent log of last 50 uploads

Example (history.json):

{
  "time": "2025-08-04T17:43:52.348215",
  "reel": "reel3.mp4",
  "status": "✅ Success"
}

🔧 Troubleshooting

Caption missing → Ensure reelx.txt exists in TITLE_FOLDER

moviepy not installed → Install via pip install moviepy>=1.0.3

Instagrapi progress_callback error → Auto-handled via fallback uploader

🚀 Deployment

For production, run with Gunicorn:

gunicorn -w 4 app:app

👨‍💻 Author

Developed by Ganesh Sonune ✨
Feel free to contribute, suggest features, or report bugs.
