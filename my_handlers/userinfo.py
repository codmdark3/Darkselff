from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_display_name
from datetime import datetime
import pytz

def format_last_seen(status):
    if status is None:
        return "نامشخص یا مخفی"
    elif hasattr(status, 'was_online'):
        dt = status.was_online.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Tehran"))
        return dt.strftime("%Y-%m-%d %H:%M")
    elif hasattr(status, 'expires'):
        return "آنلاین"
    elif hasattr(status, 'until'):
        return "آفلاین تا " + str(status.until)
    else:
        return str(status)

def register(client, config, data_path):
    @client.on(events.NewMessage(pattern=r'^\.(اطلاعات|این کیه)$'))
    async def get_user_info(event):
        if not event.is_reply:
            await event.reply("🔻 لطفاً روی پیام کاربر ریپلای کن.")
            return

        replied_msg = await event.get_reply_message()
        sender = await replied_msg.get_sender()

        try:
            full = await client(GetFullUserRequest(sender.id))
            user = full.users[0]  # 🔧 اصلاح این خط
            about = full.full_user.about if hasattr(full.full_user, "about") else "ندارد"

            name = get_display_name(user)
            username = f"@{user.username}" if user.username else "ندارد"
            user_id = user.id
            phone = user.phone if user.phone else "نامشخص"
            premium = "✅" if getattr(user, "premium", False) else "❌"
            is_bot = "✅" if user.bot else "❌"
            lang = getattr(user, "lang_code", "نامشخص")
            link = f"<a href='tg://user?id={user_id}'>کلیک</a>"
            last_seen = format_last_seen(user.status)

            # تست بلاک بودن
            try:
                await client.send_message(user_id, "✅ تست بلاک (به‌زودی حذف می‌شود)")
                blocked = "❌"
            except Exception:
                blocked = "✅"

            text = f"""
👤 <b>نام:</b> {name}
🔗 <b>یوزرنیم:</b> {username}
🆔 <b>آیدی عددی:</b> <code>{user_id}</code>
📞 <b>شماره:</b> <code>{phone}</code>
⭐ <b>Premium:</b> {premium}
🗣 <b>زبان:</b> {lang}
🤖 <b>ربات:</b> {is_bot}
📜 <b>بیو:</b> {about}
🕐 <b>آخرین بازدید:</b> {last_seen}
⛔ <b>آیا بلاکت کرده؟</b> {blocked}
🔗 <b>لینک:</b> {link}
"""
            await event.reply(text, parse_mode="html")

        except Exception as e:
            await event.reply(f"⛔ خطا در دریافت اطلاعات:\n<code>{str(e)}</code>", parse_mode="html")
            