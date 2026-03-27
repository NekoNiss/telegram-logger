import asyncio
import requests
from telethon import TelegramClient, events

API_ID = 30074866  # ← вставь свой
API_HASH = "eea91e3c3b0381b36d455383fe5b9989"  # ← вставь свой

BOT_TOKEN = "8695827916:AAENIQTjiIaorme2RJwdppGLn1_85rjXzkY"
CHAT_ID = "7649175732"

SERVER_URL = "gleaming-truth-production-ed48.up.railway.app"

clients = {}

def send(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text}
        )
    except:
        pass


async def start_client(name, session):
    client = TelegramClient(session, API_ID, API_HASH)
    await client.start()

    print("✅", name)

    @client.on(events.MessageDeleted)
    async def deleted(event):
        send(f"🗑 Удалено | {name} | chat {event.chat_id}")

    @client.on(events.MessageEdited)
    async def edited(event):
        send(f"✏️ Изменено | {name} | {event.text}")

    await client.run_until_disconnected()


async def main():
    print("🚀 START")

    while True:
        try:
            data = requests.get(f"{SERVER_URL}/sessions").json()

            for acc in data:
                if acc["name"] in clients:
                    continue

                clients[acc["name"]] = asyncio.create_task(
                    start_client(acc["name"], acc["session"])
                )

        except Exception as e:
            print("ERR:", e)

        await asyncio.sleep(10)


asyncio.run(main())
