from fastapi import FastAPI, UploadFile
import os
import json

app = FastAPI()

SESSIONS_DIR = "sessions"
LOGS_FILE = "logs.json"

os.makedirs(SESSIONS_DIR, exist_ok=True)

# 🔹 проверка
@app.get("/")
async def root():
    return {"status": "OK"}

# 🔹 получить список сессий
@app.get("/sessions")
async def get_sessions():
    files = os.listdir(SESSIONS_DIR)
    return {"sessions": files}

# 🔹 загрузка сессии
@app.post("/upload")
async def upload_session(file: UploadFile):
    path = os.path.join(SESSIONS_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"status": "uploaded"}

# 🔹 лог сообщений
@app.post("/log")
async def log(data: dict):
    if not os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, "w") as f:
            json.dump([], f)

    with open(LOGS_FILE, "r+") as f:
        logs = json.load(f)
        logs.append(data)
        f.seek(0)
        json.dump(logs, f, indent=2)

    return {"status": "saved"}
