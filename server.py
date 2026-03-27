from flask import Flask, request, jsonify

app = Flask(__name__)

sessions = []

@app.route("/add", methods=["POST"])
def add():
    sessions.append(request.json)
    return {"ok": True}

@app.route("/sessions")
def get_sessions():
    return jsonify(sessions)

app.run(host="0.0.0.0", port=3000)
