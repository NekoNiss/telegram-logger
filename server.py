from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = os.path.join(SESSIONS_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    return {"status": "ok"}


@app.get("/sessions")
def get_sessions():
    return os.listdir(SESSIONS_DIR)
