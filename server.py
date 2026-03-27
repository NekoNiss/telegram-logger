from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

SESSIONS_DIR = "sessions"

# создаём папку
os.makedirs(SESSIONS_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"status": "OK"}

@app.get("/sessions")
async def get_sessions():
    try:
        files = os.listdir(SESSIONS_DIR)
        return {"sessions": files}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload")
async def upload_session(file: UploadFile = File(...)):
    try:
        path = os.path.join(SESSIONS_DIR, file.filename)

        with open(path, "wb") as f:
            f.write(await file.read())

        return {"status": "uploaded"}
    except Exception as e:
        return {"error": str(e)}
