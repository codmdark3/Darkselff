import json
import os
from telethon import events

def get_config_path(data_path):
    return os.path.join(data_path, 'config.json')

def load_config(data_path):
    path = get_config_path(data_path)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(data_path, config):
    path = get_config_path(data_path)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def register(client, config, data_path):
    @client.on(events.NewMessage(pattern=r'^/روشن$'))
    async def turn_on(event):
        cfg = load_config(data_path)
        cfg["active"] = True
        save_config(data_path, cfg)
        await event.reply("✅ سلف‌بات با موفقیت روشن شد.")

    @client.on(events.NewMessage(pattern=r'^/خاموش$'))
    async def turn_off(event):
        cfg = load_config(data_path)
        cfg["active"] = False
        save_config(data_path, cfg)
        await event.reply("⛔ سلف‌بات با موفقیت خاموش شد.")

    @client.on(events.NewMessage(pattern=r'^/وضعیت$'))
    async def show_status(event):
        cfg = load_config(data_path)
        is_active = cfg.get("active", False)
        features = cfg.get("features", {})

        status = "🟢 روشن است." if is_active else "🔴 خاموش است."
        mapped = {
            "تبچی تبلیغاتی": features.get("ads", False),
            "حالت روح": features.get("ghost", False),
            "ری‌اکشن خودکار": features.get("reaction", False),
            "ساعت در بیو": features.get("bio", False),
            "سیو عکس زمان‌دار": features.get("watch", False),
            "ضد سین": features.get("lockpv", False),
            "هشدار حذف پیام": False,  # اگر اینا رو نداری دستی False بزن
            "هشدار ویرایش پیام": False,
            "نقل قول خودکار": features.get("quote", False),
            "چرخش اسم": False,
            "چرخش عکس پروفایل": features.get("rotate_photo", False)
        }

        feature_text = "\n".join([f"{'✅' if val else '❌'} {key}" for key, val in mapped.items()])
        msg = f"سلف‌بات {status}\n📊 وضعیت امکانات فعال:\n{feature_text}"
        await event.reply(msg)
        