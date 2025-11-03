from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
found_items = []
scanning = False
user_phone = None

# Load/Save phone
PHONE_FILE = "user_phone.txt"
if os.path.exists(PHONE_FILE):
    with open(PHONE_FILE, "r") as f:
        user_phone = f.read().strip()

@app.route("/")
def index():
    return render_template("index.html", items=found_items, scanning=scanning)

@app.route("/save_phone", methods=["POST"])
def save_phone():
    global user_phone
    data = request.get_json()
    user_phone = data["phone"]
    with open(PHONE_FILE, "w") as f:
        f.write(user_phone)
    return jsonify({"status": "saved"})

@app.route("/start")
def start():
    global scanning
    if not scanning:
        scanning = True
        from scanner import scan_all_stores
        import threading, asyncio
        def run():
            global found_items
            while scanning:
                items = asyncio.run(scan_all_stores("90210"))  # Change ZIP later
                if items:
                    found_items = items[:10]
                    for item in items:
                        if item["score"] > 50 and user_phone:
                            from scanner import send_sms
                            send_sms(item["title"], item["url"], item["score"])
                asyncio.run(asyncio.sleep(60))
        threading.Thread(target=run, daemon=True).start()
    return jsonify({"status": "running"})

@app.route("/stop")
def stop():
    global scanning
    scanning = False
    return jsonify({"status": "stopped"})
