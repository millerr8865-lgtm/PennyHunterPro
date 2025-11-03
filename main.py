import webbrowser
import os
import urllib.request
import tempfile

# === AUTO-UPDATE FROM GITHUB ===
def download_file(url, path):
    try:
        urllib.request.urlretrieve(url, path)
        print(f"Updated: {path}")
    except:
        print(f"Failed to update: {url}")

# GitHub Raw Links (PASTE YOURS HERE)
APP_URL = "https://raw.githubusercontent.com/YOURNAME/PennyHunterPro/main/app.py"
SCANNER_URL = "https://raw.githubusercontent.com/YOURNAME/PennyHunterPro/main/scanner.py"
HTML_URL = "https://raw.githubusercontent.com/YOURNAME/PennyHunterPro/main/templates/index.html"

# Temp folder
temp_dir = tempfile.gettempdir()
app_path = os.path.join(temp_dir, "app.py")
scanner_path = os.path.join(temp_dir, "scanner.py")
templates_dir = os.path.join(temp_dir, "templates")
html_path = os.path.join(templates_dir, "index.html")

# Create folders
os.makedirs(templates_dir, exist_ok=True)

# Download latest code
download_file(APP_URL, app_path)
download_file(SCANNER_URL, scanner_path)
download_file(HTML_URL, html_path)

# === RUN UPDATED CODE ===
import importlib.util
spec = importlib.util.spec_from_file_location("app", app_path)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

if __name__ == "__main__":
    print("Penny Hunter Pro — LIVE FROM CLOUD")
    webbrowser.open("http://127.0.0.1:5000")
    app_module.app.run(host="0.0.0.0", port=5000, debug=False)