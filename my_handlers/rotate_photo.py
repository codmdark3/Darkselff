import asyncio
import os
from telethon import events, functions, types
from utils import save_config

def register(client, config, data_path):
    rotate_config = config["features"].get("avatar_rotate", {})
    if "enabled" not in rotate_config:
        rotate_config["enabled"] = False
    if "delay" not in rotate_config:
        rotate_config["delay"] = 3
    if "photos" not in rotate_config:
        rotate_config["photos"] = []

    save_config(data_path, config)

    async def rotate_task():
        while True:
            try:
                if not rotate_config.get("enabled", False):
                    await asyncio.sleep(10)
                    continue

                photos = rotate_config.get("photos", [])
                delay = rotate_config.get("delay", 3)

                for photo in photos:
                    if not rotate_config.get("enabled", False):
                        break
                    if not os.path.exists(photo):
                        continue

                    # حذف عکس فعلی پروفایل
                    await client(functions.photos.UpdateProfilePhotoRequest(
                        id=types.InputPhotoEmpty()
                    ))

                    # افزودن عکس جدید
                    await client(functions.photos.UploadProfilePhotoRequest(
                        file=await client.upload_file(photo)
                    ))

                    await asyncio.sleep(delay * 60)

            except Exception as e:
                print(f"[چرخش پروفایل] خطا: {e}")
                await asyncio.sleep(60)

    client.loop.create_task(rotate_task())

    @client.on(events.NewMessage(pattern=r'^\.افزودن عکس پروفایل$'))
    async def add_profile_photo(event):
        if not event.reply_to_msg_id:
            await event.reply("❗ لطفاً عکس را با ریپلای روی پیام عکس ارسال کن.")
            return

        reply = await event.get_reply_message()
        if not reply.photo:
            await event.reply("❗ پیام ریپلای شده عکس ندارد.")
            return

        path = f"data/{config['phone']}_avatar_{len(rotate_config['photos']) + 1}.jpg"
        await client.download_media(reply.photo, file=path)
        rotate_config["photos"].append(path)
        save_config(data_path, config)
        await event.reply("✅ عکس پروفایل جدید اضافه شد.")

    @client.on(events.NewMessage(pattern=r'^\.حذف عکس پروفایل$'))
    async def delete_photos(event):
        for path in rotate_config["photos"]:
            if os.path.exists(path):
                os.remove(path)
        rotate_config["photos"] = []
        save_config(data_path, config)
        await event.reply("🗑️ تمام عکس‌های پروفایل حذف شدند.")

    @client.on(events.NewMessage(pattern=r'^\.تنظیم فاصله چرخش عکس (\d+)$'))
    async def set_delay(event):
        new_delay = int(event.pattern_match.group(1))
        rotate_config["delay"] = new_delay
        save_config(data_path, config)
        await event.reply(f"⏱️ فاصله چرخش روی {new_delay} دقیقه تنظیم شد.")

    @client.on(events.NewMessage(pattern=r'^\.فعال سازی چرخش عکس$'))
    async def enable_rotate(event):
        rotate_config["enabled"] = True
        save_config(data_path, config)
        await event.reply("✅ چرخش عکس پروفایل فعال شد.")

    @client.on(events.NewMessage(pattern=r'^\.غیرفعال سازی چرخش عکس$'))
    async def disable_rotate(event):
        rotate_config["enabled"] = False
        save_config(data_path, config)
        await event.reply("🛑 چرخش عکس پروفایل غیرفعال شد.")
        