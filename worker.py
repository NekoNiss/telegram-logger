import os
import asyncio
from datetime import datetime
import requests
from telethon import TelegramClient, events

# 🔑 ВСТАВЬ СВОЁ
api_id = 30074866
api_hash = "eea91e3c3b0381b36d455383fe5b9989
BOT_TOKEN = "7649175732:AAEiyZNWIgEdgx3i4f4Bsik_9p9JgEZayS4"

SESSIONS_DIR = "server/sessions"

# 💥 фикс: создаём папку если нет
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

messages = {}
clients = {}

# 📤 отправка текста
def send_text(user_id, text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": user_id, "text": text}
        )
    except Exception as e:
        print("send_text error:", e)

# 📤 отправка файла
def send_file(user_id, file_path, caption):
    try:
        with open(file_path, "rb") as f:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                data={"chat_id": user_id, "caption": caption},
                files={"document": f}
            )
    except Exception as e:
        print("send_file error:", e)

# 🚀 запуск клиента (АНТИ-КРАШ)
async def start_client(session_path):
    while True:
        try:
            client = TelegramClient(session_path, api_id, api_hash)
            await client.start()

            me = await client.get_me()
            user_id = me.id

            print(f"🔥 Запущен: {me.first_name}")

            # 📩 сохранение сообщений
            @client.on(events.NewMessage)
            async def save(event):
                try:
                    sender = await event.get_sender()
                    chat = await event.get_chat()

                    file_path = None
                    if event.media:
                        file_path = await event.download_media()

                    messages[(session_path, event.id)] = {
                        "text": event.text,
                        "sender": sender.first_name if sender else "Unknown",
                        "sender_id": sender.id if sender else 0,
                        "chat": getattr(chat, "title", sender.first_name if sender else "Unknown"),
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "file": file_path,
                        "user_id": user_id
                    }

                    print("📩", event.text)

                except Exception as e:
                    print("save error:", e)

            # 🗑 удаление сообщений
            @client.on(events.MessageDeleted)
            async def delete(event):
                try:
                    print("🗑", event.deleted_ids)

                    for msg_id in event.deleted_ids:
                        data = messages.get((session_path, msg_id))

                        if not data:
                            continue

                        profile = f"tg://user?id={data['sender_id']}"

                        text = f"""
🗑 УДАЛЕНО
👤 {data['sender']}
🔗 {profile}
💬 {data['chat']}
🕒 {data['time']}
━━━━━━━━━━━━━━━
{data['text'] if data['text'] else "📎 Медиа"}
"""

                        if data["file"] and os.path.exists(data["file"]):
                            send_file(data["user_id"], data["file"], text)
                        else:
                            send_text(data["user_id"], text)

                except Exception as e:
                    print("delete error:", e)

            # 🔄 держим соединение
            await client.run_until_disconnected()

        except Exception as e:
            print("💥 Краш клиента:", e)
            await asyncio.sleep(5)

# 👀 авто-подхват новых session
async def watch_sessions():
    while True:
        try:
            for file in os.listdir(SESSIONS_DIR):
                if file.endswith(".session"):
                    name = file.replace(".session", "")

                    if name in clients:
                        continue

                    print("🆕 Новая сессия:", name)

                    task = asyncio.create_task(
                        start_client(os.path.join(SESSIONS_DIR, name))
                    )
                    clients[name] = task

        except Exception as e:
            print("watch error:", e)

        await asyncio.sleep(10)

# 🚀 запуск
async def main():
    print("🚀 Worker запущен")
    await watch_sessions()

asyncio.run(main())
