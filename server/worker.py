from telethon import TelegramClient, events
import os
import asyncio
from datetime import datetime
import requests

api_id = 30074866
api_hash = "eea91e3c3b0381b36d455383fe5b9989"
BOT_TOKEN = "7649175732:AAEiyZNWIgEdgx3i4f4Bsik_9p9JgEZayS4"

SESSIONS_DIR = "sessions"

messages = {}


def send(user_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": user_id, "text": text}
    )


async def start_client(session_path):
    client = TelegramClient(session_path, api_id, api_hash)
    await client.start()

    me = await client.get_me()
    user_id = me.id

    print(f"🔥 Запущен: {me.first_name}")

    @client.on(events.NewMessage)
    async def save(event):
        if not event.is_private:
            return

        messages[(session_path, event.id)] = event.text

    @client.on(events.MessageDeleted)
    async def delete(event):
        for msg_id in event.deleted_ids:
            text = messages.get((session_path, msg_id))
            if not text:
                continue

            send(user_id, f"🗑 Удалено:\n{text}")

    await client.run_until_disconnected()


async def main():
    tasks = []

    for file in os.listdir(SESSIONS_DIR):
        if file.endswith(".session"):
            path = os.path.join(SESSIONS_DIR, file.replace(".session", ""))
            tasks.append(start_client(path))

    await asyncio.gather(*tasks)


asyncio.run(main())