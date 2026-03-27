from flask import Flask, request
import os

app = Flask(__name__)

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    path = os.path.join(SESSIONS_DIR, file.filename)
    file.save(path)

    print(f"✅ Получена сессия: {file.filename}")

    return "OK"

app.run(host="0.0.0.0", port=3000)