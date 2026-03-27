import asyncio
import aiohttp
from telethon import TelegramClient, events

API_ID = 30074866
API_HASH = "eea91e3c3b0381b36d455383fe5b9989"

SERVER_URL = "https://gleaming-truth-production-ed48.up.railway.app"

clients = []

async def get_sessions():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{SERVER_URL}/sessions") as resp:
            data = await resp.json()

            if "sessions" not in data:
                print("❌ Invalid response:", data)
                return []

            return data["sessions"]
            
async def send_log(data):
    async with aiohttp.ClientSession() as session:
        await session.post(f"{SERVER_URL}/log", json=data)

async def start_client(session_name):
    client = TelegramClient(f"sessions/{session_name}", API_ID, API_HASH)
    await client.start()

    print(f"✅ Запущен: {session_name}")

    # удалённые сообщения
    @client.on(events.MessageDeleted)
    async def deleted_handler(event):
        await send_log({
            "type": "deleted",
            "ids": event.deleted_ids,
            "chat": str(event.chat_id)
        })

    # изменённые сообщения
    @client.on(events.MessageEdited)
    async def edited_handler(event):
        await send_log({
            "type": "edited",
            "text": event.raw_text,
            "chat": str(event.chat_id)
        })

    await client.run_until_disconnected()

async def main():
    print("🚀 WORKER START")

    sessions = await get_sessions()
    print("📂 sessions:", sessions)

    if not sessions:
        print("❌ Нет сессий")
        return

    tasks = []

    for s in sessions:
        tasks.append(start_client(s))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
