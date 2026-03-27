from flask import Flask, request
import os

app = Flask(__name__)

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return "No file", 400

    filepath = os.path.join(SESSIONS_DIR, file.filename)
    file.save(filepath)

    return "OK", 200


@app.route("/")
def home():
    return "Server is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
