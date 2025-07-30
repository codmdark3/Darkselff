from telethon import events
from datetime import datetime, timedelta
import asyncio
import re
import pytz

def register(client, config, data_path):
    @client.on(events.NewMessage(pattern=r'^\.بازشو (\d{2}:\d{2}:\d{2})(?: (https?://t\.me/[\w\d_]+/\d+))?$'))
    async def timed_star_open(event):
        try:
            time_str = event.pattern_match.group(1)
            link = event.pattern_match.group(2)

            # تنظیم منطقه زمانی ایران
            iran_tz = pytz.timezone("Asia/Tehran")
            now = datetime.now(iran_tz)

            # ساخت زمان هدف با ساعت ایران
            target_time = datetime.strptime(time_str, "%H:%M:%S").replace(
                year=now.year, month=now.month, day=now.day
            )
            target_time = iran_tz.localize(target_time)

            if target_time < now:
                target_time += timedelta(days=1)

            wait_time = (target_time - now).total_seconds()

            # دریافت پیام هدف
            if link:
                match = re.search(r't\.me/([\w\d_]+)/(\d+)', link)
                if not match:
                    return await event.reply("❌ لینک نامعتبره.")
                username = match.group(1)
                msg_id = int(match.group(2))
                target_msg = await client.get_messages(username, ids=msg_id)
            elif event.is_reply:
                target_msg = await event.get_reply_message()
            else:
                return await event.reply("❌ لطفاً لینک بده یا روی پیام قفل ریپلای کن.")

            if not target_msg:
                return await event.reply("❌ پیام مورد نظر پیدا نشد.")

            await event.reply(f"⏳ طبق ساعت ایران منتظر می‌مونم تا {time_str} باز کنم...")

            # منتظر بمون تا ساعت برسه
            await asyncio.sleep(wait_time)

            if target_msg.buttons:
                await target_msg.click(0)
                await event.respond("✅ عکس Starz با موفقیت باز شد!")
            else:
                await event.respond("❌ این پیام دکمه‌ای برای باز کردن نداره.")

        except Exception as e:
            await event.respond(f"⚠️ خطا: {str(e)}")
            