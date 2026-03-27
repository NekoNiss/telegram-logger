from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

SESSIONS_DIR = "sessions"

# создаём папку если нет
os.makedirs(SESSIONS_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"status": "OK"}

# ✅ ВОТ ЭТО ГЛАВНОЕ
@app.get("/sessions")
async def get_sessions():
    files = os.listdir(SESSIONS_DIR)
    return {"sessions": files}

# загрузка сессий
@app.post("/upload")
async def upload_session(file: UploadFile = File(...)):
    path = os.path.join(SESSIONS_DIR, file.filename)
    
    with open(path, "wb") as f:
        f.write(await file.read())

    return {"status": "uploaded"}
