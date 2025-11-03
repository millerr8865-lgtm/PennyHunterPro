from flask import Flask, render_template, jsonify
from scanner import scan_all_stores
import asyncio
import threading
from datetime import datetime

app = Flask(__name__)
found_items = []
scanning = False

def async_scan_loop(zip_code):
    global found_items, scanning
    while scanning:
        new_items = asyncio.run(scan_all_stores(zip_code))
        if new_items:
            found_items = new_items + found_items[:20]  # Keep top 20
            found_items.sort(key=lambda x: x['score'], reverse=True)
        time.sleep(60)  # Scan every minute (faster for demo; change to 900 for 15min)

@app.route("/")
def index():
    return render_template("index.html", items=found_items, scanning=scanning)

@app.route("/start")
def start():
    global scanning
    if not scanning:
        scanning = True
        threading.Thread(target=lambda: async_scan_loop("60622"), daemon=True).start()  # Change ZIP
    return jsonify({"status": "running", "items": found_items})

@app.route("/stop")
def stop():
    global scanning
    scanning = False
    return jsonify({"status": "stopped"})