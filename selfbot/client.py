import json
import os
from telethon import TelegramClient

def load_accounts():
    with open("accounts.json", "r", encoding="utf-8") as f:
        return json.load(f)

def create_all_clients():
    accounts = load_accounts()
    clients = {}

    for acc in accounts:
        phone = acc["phone"]
        session_name = acc["session"]
        client = TelegramClient(session_name, acc["api_id"], acc["api_hash"])
        
        clients[phone] = {
            "client": client,
            "config": acc,
            "data_path": f"data/{phone.replace('+', '')}"
        }

        os.makedirs(clients[phone]["data_path"], exist_ok=True)

    return clients
    