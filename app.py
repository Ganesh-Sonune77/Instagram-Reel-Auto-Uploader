from flask import Flask, request, render_template, redirect, session, jsonify
from uploader import test_login
from scheduler import set_schedule, scheduler
from log import get_recent_history
import os, json
from dotenv import load_dotenv
import moviepy.editor as mp


try:
    import moviepy.editor
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "moviepy>=1.0.3"])


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if test_login(username, password):
        session["username"] = username
        session["password"] = password
        return redirect("/schedule")
    return "❌ Invalid login"

@app.route("/schedule")
def schedule_ui():
    if "username" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/schedule", methods=["POST"])
def schedule_upload():
    if "username" not in session:
        return redirect("/")
    value = request.form["gap_value"]
    unit = request.form["gap_unit"]
    set_schedule(value, unit, session["username"], session["password"])
    return redirect("/status")

@app.route("/status")
def status():
    history = get_recent_history()
    return render_template("status.html", history=history)

@app.route("/pause")
def pause():
    scheduler.pause()
    return redirect("/status")

@app.route("/resume")
def resume():
    scheduler.resume()
    return redirect("/status")

@app.route("/upload_status")
def upload_status():
    try:
        with open("status.json", "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({
            "upload": {
                "reel": "",
                "percent": 0,
                "status": "idle"
            },
            "next_upload": ""
        })
