import os
import asyncio
from telethon import events, functions
from utils import save_config

def register(client, config, data_path):
    if "avatar_rotate" not in config:
        config["avatar_rotate"] = {
            "enabled": False,
            "delay": 180,  # ثانیه
        }

    avatar = config["avatar_rotate"]
    photo_folder = "profile_photos"

    if not os.path.exists(photo_folder):
        os.makedirs(photo_folder)

    @client.on(events.NewMessage(pattern=r"^\.فعال سازی چرخش عکس$", chats="me"))
    async def enable_avatar(event):
        avatar["enabled"] = True
        save_config(data_path, config)
        await event.reply("✅ چرخش عکس پروفایل فعال شد.")

    @client.on(events.NewMessage(pattern=r"^\.غیرفعال سازی چرخش عکس$", chats="me"))
    async def disable_avatar(event):
        avatar["enabled"] = False
        save_config(data_path, config)
        await event.reply("⛔️ چرخش عکس پروفایل غیرفعال شد.")

    @client.on(events.NewMessage(pattern=r"^\.تنظیم تاخیر چرخش عکس (\d+)$", chats="me"))
    async def set_delay(event):
        delay = int(event.pattern_match.group(1))
        avatar["delay"] = delay
        save_config(data_path, config)
        await event.reply(f"⏱️ فاصله چرخش تنظیم شد روی {delay} ثانیه.")

    async def avatar_loop():
        while True:
            await asyncio.sleep(avatar["delay"])
            if not avatar["enabled"]:
                continue

            photos = [os.path.join(photo_folder, f) for f in os.listdir(photo_folder) if f.lower().endswith((".jpg", ".png"))]
            if not photos:
                continue

            for photo in photos:
                if not avatar["enabled"]:
                    break
                try:
                    await client(functions.photos.UploadProfilePhotoRequest(file=await client.upload_file(photo)))
                    await asyncio.sleep(avatar["delay"])
                except Exception as e:
                    print(f"[AVATAR ERROR] {e}")

    client.loop.create_task(avatar_loop())
    
    