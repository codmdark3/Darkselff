from telethon import events
import json
import os
import re

# مسیر ذخیره تنظیمات برای هر اکانت
def get_format_path(data_path):
    return os.path.join(data_path, "format_mode.json")

# ذخیره حالت فرمت
def save_format(data_path, fmt):
    with open(get_format_path(data_path), "w", encoding="utf-8") as f:
        json.dump({"format": fmt}, f)

# بارگذاری حالت فرمت
def load_format(data_path):
    try:
        with open(get_format_path(data_path), "r", encoding="utf-8") as f:
            return json.load(f).get("format", "عادی")
    except:
        return "عادی"

# فرار دادن کاراکترهای خاص برای MarkdownV2
def escape_md(text):
    escape_chars = r"_*~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

# ثبت هندلر
def register(client, config, data_path):
    @client.on(events.NewMessage(pattern=r"^\.فرمت (.+)$"))
    async def set_format(event):
        fmt = event.pattern_match.group(1).strip()
        valid_formats = [
            "عادی", "بولد", "کج", "خط خورده", "زیر خط", "کد", "پری", "نقل قول", "اسپویلر"
        ]
        if fmt not in valid_formats:
            await event.reply("❌ فرمت نامعتبره. فرمت‌های مجاز:\n" + "، ".join(valid_formats))
            return

        save_format(data_path, fmt)
        await event.reply(f"✅ حالت فرمت روی «{fmt}» تنظیم شد.")

    @client.on(events.NewMessage(outgoing=True))
    async def auto_format(event):
        fmt = load_format(data_path)
        if not fmt or fmt == "عادی":
            return

        try:
            text = event.message.message
            if not text:
                return

            if fmt == "بولد":
                await event.edit(f"<b>{text}</b>", parse_mode="html")
            elif fmt == "کج":
                await event.edit(f"<i>{text}</i>", parse_mode="html")
            elif fmt == "خط خورده":
                await event.edit(f"<s>{text}</s>", parse_mode="html")
            elif fmt == "زیر خط":
                await event.edit(f"<u>{text}</u>", parse_mode="html")
            elif fmt == "کد":
                await event.edit(f"<code>{text}</code>", parse_mode="html")
            elif fmt == "پری":
                await event.edit(f"<pre>{text}</pre>", parse_mode="html")
            elif fmt == "نقل قول":
                await event.edit(f"❝ {text} ❞")
            elif fmt == "اسپویلر":
                safe_text = escape_md(text)
                await event.edit(f"||{safe_text}||", parse_mode="MarkdownV2")
        except Exception as e:
            print(f"[format_text_auto] خطا: {e}")
            