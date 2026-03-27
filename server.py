import os
import asyncio
from fastapi import FastAPI, UploadFile, File
from telethon import TelegramClient, events

API_ID = 30074866
API_HASH = "eea91e3c3b0381b36d455383fe5b9989"

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

app = FastAPI()

clients = []

# ===== ЗАПУСК КЛИЕНТА =====
async def start_client(session_path):
    name = os.path.splitext(os.path.basename(session_path))[0]

    client = TelegramClient(session_path, API_ID, API_HASH)

    await client.start()

    print(f"✅ Запущен: {name}")

    # ===== ЛОГ СООБЩЕНИЙ =====
    @client.on(events.NewMessage)
    async def handler(event):
        try:
            print(f"[{name}] {event.chat_id}: {event.text}")
        except:
            pass

    clients.append(client)

# ===== ЗАГРУЗКА СЕССИИ =====
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = os.path.join(SESSIONS_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    asyncio.create_task(start_client(path))

    return {"status": "ok"}

# ===== СТАРТ ВСЕХ СЕССИЙ =====
@app.on_event("startup")
async def startup():
    for file in os.listdir(SESSIONS_DIR):
        if file.endswith(".session"):
            path = os.path.join(SESSIONS_DIR, file)
            asyncio.create_task(start_client(path))
