import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")

os.makedirs(SESSIONS_DIR, exist_ok=True)

@app.get("/sessions")
def get_sessions():
    try:
        return {"sessions": os.listdir(SESSIONS_DIR)}
    except Exception as e:
        return {"sessions": [], "error": str(e)}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        path = os.path.join(SESSIONS_DIR, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/delete")
def delete(name: str):
    try:
        path = os.path.join(SESSIONS_DIR, name)
        if os.path.exists(path):
            os.remove(path)
        return {"status": "deleted"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/logs")
def logs():
    try:
        if not os.path.exists(LOG_FILE):
            return {"logs": ""}
        return {"logs": open(LOG_FILE, encoding="utf-8").read()}
    except Exception as e:
        return {"logs": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
