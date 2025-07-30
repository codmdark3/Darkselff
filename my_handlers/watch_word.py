from telethon import events
import os

def register(client, config, data_path):
    watch_file = os.path.join(data_path, "watch_word.txt")
    status_file = os.path.join(data_path, "watch_status.txt")

    # اطمینان از وجود فایل‌ها
    if not os.path.exists(watch_file):
        with open(watch_file, "w", encoding="utf-8") as f:
            f.write("")
    if not os.path.exists(status_file):
        with open(status_file, "w", encoding="utf-8") as f:
            f.write("off")

    # تنظیم کلمه
    @client.on(events.NewMessage(pattern="(?i)^.تنظیم کلمه (.+)"))
    async def set_word(event):
        word = event.pattern_match.group(1).strip()
        with open(watch_file, "w", encoding="utf-8") as f:
            f.write(word)
        await event.reply(f"🔍 کلمه‌ی مورد نظر تنظیم شد به: «{word}»")

    # فعال سازی
    @client.on(events.NewMessage(pattern="^.فعال سازی هشدار کلمه"))
    async def activate(event):
        with open(watch_file, "r", encoding="utf-8") as f:
            word = f.read().strip()
        if not word:
            return await event.reply("⚠️ اول با دستور `.تنظیم کلمه ...` یه کلمه وارد کن!")
        with open(status_file, "w", encoding="utf-8") as f:
            f.write("on")
        await event.reply("✅ هشدار کلمه فعال شد.")

    # غیرفعال سازی
    @client.on(events.NewMessage(pattern="^.غیرفعال سازی هشدار کلمه"))
    async def deactivate(event):
        with open(status_file, "w", encoding="utf-8") as f:
            f.write("off")
        await event.reply("❌ هشدار کلمه غیرفعال شد.")

    # بررسی پیام‌ها
    @client.on(events.NewMessage())
    async def watch_message(event):
        if event.is_private:
            return  # فقط گروه‌ها

        # بررسی وضعیت
        with open(status_file, "r", encoding="utf-8") as f:
            if f.read().strip() != "on":
                return

        # دریافت کلمه
        with open(watch_file, "r", encoding="utf-8") as f:
            word = f.read().strip()

        if not word or word.lower() not in event.message.message.lower():
            return

        sender = await event.get_sender()
        sender_id = sender.username or sender.id
        msg_link = None
        try:
            msg_link = await client.get_message_link(event.message)
        except:
            pass

        text = f"🚨 کلمه‌ی خاص تشخیص داده شد!\n\n👤 فرستنده: {sender_id}\n🗨️ پیام: {event.message.message}"
        if msg_link:
            text += f"\n🔗 لینک پیام: {msg_link}"

        await client.send_message("me", text)
        