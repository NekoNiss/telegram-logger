import os
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

SESSIONS_DIR = "sessions"
LOG_FILE = "logs.txt"

os.makedirs(SESSIONS_DIR, exist_ok=True)

@app.get("/sessions")
def get_sessions():
    try:
        sessions = os.listdir(SESSIONS_DIR)
        return {"sessions": sessions}
    except Exception as e:
        return {"sessions": [], "error": str(e)}

@app.post("/upload")
async def upload_session(file: UploadFile = File(...)):
    try:
        path = os.path.join(SESSIONS_DIR, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/delete")
def delete_session(name: str):
    try:
        path = os.path.join(SESSIONS_DIR, name)
        if os.path.exists(path):
            os.remove(path)
        return {"status": "deleted"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/logs")
def get_logs():
    try:
        if not os.path.exists(LOG_FILE):
            return {"logs": ""}
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return {"logs": f.read()}
    except Exception as e:
        return {"logs": str(e)}

# Railway support
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
