import os
import json
from telethon import events
from utils import get_phone

ALL_FEATURES = {
    "auto_reply": "پاسخ‌ خودکار",
    "ghost_mode": "حالت روح",
    "no_seen": "ضد سین",
    "clock_bio": "ساعت در بیو",
    "auto_react": "ری‌اکشن خودکار",
    "delete_alert": "هشدار حذف پیام",
    "edit_alert": "هشدار ویرایش پیام",
    "auto_clean": "پاکسازی چت",
    "rotate_name": "چرخش اسم",
    "rotate_profile": "چرخش عکس پروفایل",
    "forward_saver": "سیو عکس زمان‌دار",
    "ads_sender": "تبچی تبلیغاتی",
}

def register(client, config, data_path):
    @client.on(events.NewMessage(pattern=r'^(وضعیت|/وضعیت)$'))
    async def status_handler(event):
        print(f"[STATUS HANDLER] درخواست وضعیت از کاربر {event.sender_id} دریافت شد.")

        # data_path اینجا باید پوشه مخصوص اکانت باشه مثل data/989033674402
        config_path = os.path.join(data_path, "config.json")

        if not os.path.exists(config_path):
            await event.reply("⚠️ تنظیماتی برای این حساب یافت نشد.")
            print(f"[STATUS HANDLER] فایل تنظیمات برای {data_path} پیدا نشد: {config_path}")
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except Exception as e:
            await event.reply(f"⚠️ خطا در بارگذاری تنظیمات: {e}")
            print(f"[STATUS HANDLER] خطا در خواندن فایل تنظیمات {config_path}: {e}")
            return

        lines = ["📊 وضعیت امکانات فعال:"]
        features = settings.get("features", {})  # دیکشنری امکانات فعال

        for key, title in sorted(ALL_FEATURES.items(), key=lambda x: x[1]):
            status = features.get(key, False)
            emoji = "✅" if status else "❌"
            lines.append(f"{emoji} {title}")

        # وضعیت کلی روشن/خاموش سلف‌بات
        active = settings.get("active", False)
        lines.insert(0, f"سلف‌بات {'✅ روشن' if active else '🔴 خاموش'} است.")

        await event.reply("\n".join(lines))
        print(f"[STATUS HANDLER] وضعیت برای {data_path} ارسال شد.")
        