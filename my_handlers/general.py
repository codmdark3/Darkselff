from telethon import events
import json
import os

def load_status(data_path):
    status_file = os.path.join(data_path, "status.json")
    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            return json.load(f)
    return {"enabled": True}

def save_status(data_path, status):
    status_file = os.path.join(data_path, "status.json")
    with open(status_file, "w") as f:
        json.dump(status, f)

def register_all(client, config, data_path):
    status = load_status(data_path)

    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^وضعیت$"))
    async def status_handler(event):
        if status.get("enabled", True):
            await event.reply("✅ سلف فعال است.")
        else:
            await event.reply("❌ سلف غیرفعال است.")

    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^خاموش$"))
    async def disable_handler(event):
        status["enabled"] = False
        save_status(data_path, status)
        await event.reply("❌ سلف خاموش شد.")

    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^روشن$"))
    async def enable_handler(event):
        status["enabled"] = True
        save_status(data_path, status)
        await event.reply("✅ سلف روشن شد.")
        