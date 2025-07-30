from telethon import events
from datetime import datetime
import jdatetime  # برای تاریخ شمسی

def register(client, config, data_path):
    @client.on(events.NewMessage(incoming=True))
    async def handle_timed_media(event):
        if not event.is_private:
            return

        # بررسی اینکه مدیا زمان‌دار (View Once) هست یا نه
        if event.media and getattr(event.media, 'ttl_seconds', None):
            try:
                sender = await event.get_sender()
                username = f"@{sender.username}" if sender.username else "بدون_یوزرنیم"
                user_id = sender.id

                # گرفتن زمان به وقت ایران
                now_iran = datetime.utcnow().timestamp() + (3.5 * 3600)  # UTC +3:30
                dt = datetime.fromtimestamp(now_iran)
                time_str = dt.strftime("%H:%M:%S")
                date_shamsi = jdatetime.datetime.fromgregorian(datetime=dt).strftime("%Y/%m/%d")

                caption = (
                    f"👤 فرستنده: {username}\n"
                    f"🆔 آیدی عددی: {user_id}\n"
                    f"🕒 ساعت: {time_str}\n"
                    f"📅 تاریخ: {date_shamsi}"
                )

                await client.send_file("me", event.media, caption=caption)
                print(f"✅ مدیای زمان‌دار ذخیره شد از {username}")

            except Exception as e:
                print(f"❌ خطا در ذخیره مدیای زمان‌دار: {e}")
                