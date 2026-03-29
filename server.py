from fastapi import FastAPI, UploadFile, File
import os
import shutil

app = FastAPI()

SESSIONS_DIR = "sessions"

os.makedirs(SESSIONS_DIR, exist_ok=True)

print("🚀 SERVER START")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/sessions")
async def get_sessions():
    files = os.listdir(SESSIONS_DIR)
    return {"sessions": files}


@app.post("/upload")
async def upload_session(file: UploadFile = File(...)):
    path = os.path.join(SESSIONS_DIR, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"status": "uploaded", "file": file.filename}
