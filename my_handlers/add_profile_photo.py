import os
from telethon import events

# اگر utils.py کنار main.py هست و مسیر اجرا هم ریشه پروژه است، این درست کار می‌کند
from utils import save_config

def register(client, config, data_path):
    rotate_config = config.setdefault("features", {}).setdefault("avatar_rotate", {})
    rotate_config.setdefault("photos", [])

    avatars_path = os.path.join(data_path, "avatars")
    os.makedirs(avatars_path, exist_ok=True)

    @client.on(events.NewMessage(pattern=r"^\.افزودن عکس پروفایل$"))
    async def handle_invalid(event):
        await event.reply("❗ لطفاً عکس رو با کپشن `.افزودن عکس پروفایل` ارسال کن.")

    @client.on(events.NewMessage())
    async def add_photo(event):
        if not event.message.file:
            return

        caption = getattr(event.message, "caption", None)
        if not caption:
            return

        if caption.strip() != ".افزودن عکس پروفایل":
            return

        try:
            file_path = await event.download_media(file=avatars_path)
            rotate_config["photos"].append(file_path)
            save_config(data_path, config)
            await event.reply("✅ عکس با موفقیت به لیست چرخش اضافه شد.")
        except Exception as e:
            await event.reply(f"⚠️ خطا در افزودن عکس: {e}")
            