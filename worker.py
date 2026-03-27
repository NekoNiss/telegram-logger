import os
import asyncio
from telethon import TelegramClient

API_ID = 30074866  # ← вставь свой
API_HASH = "eea91e3c3b0381b36d455383fe5b9989"  # ← вставь свой

clients = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")

# 💥 ГАРАНТИЯ СОЗДАНИЯ ПАПКИ
os.makedirs(SESSIONS_DIR, exist_ok=True)


async def start_client(session_path):
    name = os.path.basename(session_path)

    try:
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.start()

        print(f"✅ Запущен: {name}")

        await client.run_until_disconnected()

    except Exception as e:
        print(f"💥 Ошибка клиента {name}:", e)


async def watch_sessions():
    while True:
        try:
            os.makedirs(SESSIONS_DIR, exist_ok=True)

            for file in os.listdir(SESSIONS_DIR):
                if file.endswith(".session"):
                    name = file.replace(".session", "")

                    if name in clients:
                        continue

                    print("🆕 Найдена сессия:", name)

                    task = asyncio.create_task(
                        start_client(os.path.join(SESSIONS_DIR, name))
                    )
                    clients[name] = task

        except Exception as e:
            print("💥 watch error:", e)

        await asyncio.sleep(10)


async def main():
    print("🚀 Worker запущен")
    await watch_sessions()


if __name__ == "__main__":
    asyncio.run(main())
