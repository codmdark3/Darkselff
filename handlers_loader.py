import os
import importlib
from telethon import events
from datetime import datetime
from asyncio import sleep

# متغیر وضعیت برای توقف تگ
tagging_active = {}

def register_all(client, config, data_path):
    if not config.get("selfbot_enabled", True):
        print("❌ سلف‌بات غیرفعاله، هیچ هندلری ثبت نمی‌شه.")
        return

    # ✅ ذخیره خودکار مدیای زمان‌دار
    @client.on(events.NewMessage(incoming=True))
    async def save_view_once_private(event):
        if not event.is_private:
            return

        if event.media and getattr(event.message, "ttl_seconds", None):
            sender = await event.get_sender()
            username = sender.username or f"user_{sender.id}"
            folder = os.path.join(data_path, "timed_media", str(username))
            os.makedirs(folder, exist_ok=True)

            try:
                file_path = await event.download_media(file=folder)
                file_name = os.path.basename(file_path)

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                info = f"🕒 زمان دریافت: {now}\n👤 فرستنده: @{username}\n📁 فایل: {file_name}"

                await client.send_file("me", file_path, caption=info)
                print(f"✅ فایل زمان‌دار ذخیره و ارسال شد: {file_path}")

            except Exception as e:
                print(f"❌ خطا در ذخیره یا ارسال فایل زمان‌دار: {e}")

    # ✅ دستور .تگ همه برای تگ روی پیام ریپلای‌شده
    @client.on(events.NewMessage(pattern=r'^\.تگ همه$'))
    async def tag_all(event):
        if not event.is_group:
            return await event.reply("این دستور فقط توی گروه کار می‌کنه.")

        if not event.is_reply:
            return await event.reply("لطفاً روی یک پیام ریپلای کن بعد دستور بده.")

        chat_id = event.chat_id
        tagging_active[chat_id] = True
        replied_msg = await event.get_reply_message()

        users = []
        async for user in client.iter_participants(chat_id):
            if not user.bot:
                mention = f"[{user.first_name}](tg://user?id={user.id})"
                users.append(mention)

        chunk_size = 5  # هر پیام ۵ نفر
        for i in range(0, len(users), chunk_size):
            if not tagging_active.get(chat_id, False):
                break  # لغو شده
            mentions = ' '.join(users[i:i + chunk_size])
            try:
                await client.send_message(chat_id, mentions, reply_to=replied_msg.id)
                await sleep(2)
            except Exception as e:
                print(f"خطا در تگ @{mentions}: {e}")
                continue

        tagging_active[chat_id] = False
        await event.reply("✅ تگ کردن تموم شد.")

    # ✅ دستور .لغو تگ برای توقف
    @client.on(events.NewMessage(pattern=r'^\.لغو تگ$'))
    async def cancel_tagging(event):
        chat_id = event.chat_id
        if tagging_active.get(chat_id, False):
            tagging_active[chat_id] = False
            await event.reply("🛑 تگ زدن متوقف شد.")
        else:
            await event.reply("❌ هیچ تگی در حال انجام نیست.")

    # 🔁 لود تمام هندلرهای پوشه my_handlers
    handlers_dir = os.path.join(os.path.dirname(__file__), "my_handlers")
    for filename in os.listdir(handlers_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            try:
                module_path = f"my_handlers.{module_name}"
                module = importlib.import_module(module_path)
                if hasattr(module, "register"):
                    module.register(client, config, data_path)
                    print(f"[LOADER] Registered: {module_path}")
                else:
                    print(f"[LOADER] Skipped (no register): {module_path}")
            except Exception as e:
                print(f"[LOADER] ❌ Error loading {module_path}: {e}")
