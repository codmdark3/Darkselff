import os
import json
from telethon import events

ACTIVE_KEY = "active"  # کلید وضعیت روشن یا خاموش بودن

def load_config(data_path):
    path = os.path.join(data_path, "config.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # اگر فایل نبود، پیش‌فرض روشن بودن و بدون امکانات
        return {ACTIVE_KEY: True}

def save_config(data_path, config):
    path = os.path.join(data_path, "config.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def register(client, config, data_path):
    @client.on(events.NewMessage(pattern=r'^(روشن|/روشن)$'))
    async def turn_on(event):
        conf = load_config(data_path)
        conf[ACTIVE_KEY] = True
        save_config(data_path, conf)
        await event.reply("✅ سلف‌بات با موفقیت روشن شد.")

    @client.on(events.NewMessage(pattern=r'^(خاموش|/خاموش)$'))
    async def turn_off(event):
        conf = load_config(data_path)
        conf[ACTIVE_KEY] = False
        save_config(data_path, conf)
        await event.reply("⛔ سلف‌بات با موفقیت خاموش شد.")

    @client.on(events.NewMessage(pattern=r'^(وضعیت|/وضعیت)$'))
    async def show_status(event):
        conf = load_config(data_path)
        status = "✅ روشن" if conf.get(ACTIVE_KEY, True) else "🔴 خاموش"
        await event.reply(f"📍 وضعیت فعلی سلف‌بات:\n{status}")
        