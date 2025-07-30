from telethon import events, functions, types
import asyncio
from utils import save_config

def register(client, config, data_path):
    if "always_online" not in config["features"]:
        config["features"]["always_online"] = False
        save_config(data_path, config)

    async def keep_online():
        while True:
            try:
                if config["features"].get("always_online", False):
                    # تنظیم به حالت آنلاین
                    await client(functions.account.UpdateStatusRequest(offline=False))

                    # اکشن تایپ کردن در Saved Messages
                    me = await client.get_me()
                    await client(functions.messages.SetTypingRequest(
                        peer=me.username if me.username else "me",
                        action=types.SendMessageTypingAction()
                    ))

                    print("[همیشه آنلاین] تایپ فعال شد")
                await asyncio.sleep(60)
            except Exception as e:
                print(f"[همیشه آنلاین] خطا: {e}")
                await asyncio.sleep(60)

    client.loop.create_task(keep_online())

    @client.on(events.NewMessage(pattern=r"^\.فعال سازی آنلاین$"))
    async def enable(event):
        config["features"]["always_online"] = True
        save_config(data_path, config)
        await event.reply("✅ همیشه آنلاین فعال شد.")

    @client.on(events.NewMessage(pattern=r"^\.غیرفعال سازی آنلاین$"))
    async def disable(event):
        config["features"]["always_online"] = False
        save_config(data_path, config)
        await event.reply("🛑 همیشه آنلاین غیرفعال شد.")
        