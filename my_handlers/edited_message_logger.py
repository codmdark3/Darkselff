from telethon import events
from datetime import datetime
import jdatetime

# دیکشنری کش برای نگهداری نسخه اولیه پیام‌ها
original_messages = {}

def register(client, config, data_path):
    # ذخیره پیام اولیه برای مقایسه بعدی
    @client.on(events.NewMessage(incoming=True))
    async def store_original(event):
        if event.is_private and event.text:
            original_messages[event.id] = event.text

    # هندلر ویرایش پیام
    @client.on(events.MessageEdited(incoming=True))
    async def handle_edit(event):
        if not event.is_private or not event.text:
            return

        try:
            sender = await event.get_sender()
            username = f"@{sender.username}" if sender.username else "بدون_یوزرنیم"
            user_id = sender.id

            old_text = original_messages.get(event.id, "❌ ذخیره نشده")
            new_text = event.text

            # ساعت و تاریخ به وقت ایران
            now_iran = datetime.utcnow().timestamp() + (3.5 * 3600)
            dt = datetime.fromtimestamp(now_iran)
            time_str = dt.strftime("%H:%M:%S")
            date_shamsi = jdatetime.datetime.fromgregorian(datetime=dt).strftime("%Y/%m/%d")

            message = (
                f"✏️ پیام ویرایش‌شده در پیوی:\n"
                f"👤 فرستنده: {username}\n"
                f"🆔 آیدی عددی: {user_id}\n"
                f"📅 تاریخ: {date_shamsi}\n"
                f"🕒 ساعت: {time_str}\n\n"
                f"📝 قبل:\n{old_text}\n\n"
                f"📝 بعد:\n{new_text}"
            )

            await client.send_message("me", message)
            print(f"✏️ پیام ویرایش‌شده ذخیره شد از {username}")

            # آپدیت کش
            original_messages[event.id] = new_text

        except Exception as e:
            print(f"❌ خطا در ذخیره پیام ویرایش‌شده: {e}")
