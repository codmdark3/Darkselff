from telethon import events

def register(client, config, data_path):
    @client.on(events.NewMessage(pattern=r"^\.حساب (.+)"))
    async def calc_handler(event):
        if event.is_private or event.chat_id == "me":
            expression = event.pattern_match.group(1)
            try:
                # فقط اعداد و عملگرهای ساده
                allowed = "0123456789+-*/(). "
                if any(c not in allowed for c in expression):
                    return await event.reply("🚫 فقط عدد و عملگر مجاز است.")

                result = eval(expression)
                await event.reply(f"📊 نتیجه: `{result}`")
            except Exception as e:
                await event.reply(f"❌ خطا در محاسبه: {e}")
                