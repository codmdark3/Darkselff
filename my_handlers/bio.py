from telethon import events, functions
import asyncio
from datetime import datetime
import pytz
import random

# وضعیت فعال یا غیرفعال بودن ساعت بیو
bio_status = {"enabled": False}

# فونت‌های ساعت
fonts = [
    "⓿➊➋➌➍➎➏➐➑➒",
    "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟯𝟴𝟵",
    "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫",
    "⓪①②③④⑤⑥⑦⑧⑨",
]

# تبدیل اعداد به فونت خاص
def stylize(text, style):
    normal = "0123456789"
    return ''.join(style[normal.index(c)] if c in normal else c for c in text)

# بروزرسانی بیو هر 60 ثانیه
async def update_bio_loop(client):
    while True:
        if bio_status["enabled"]:
            now = datetime.now(pytz.timezone("Asia/Tehran"))
            font = random.choice(fonts)
            hour = stylize(now.strftime("%H"), font)
            minute = stylize(now.strftime("%M"), font)
            bio = f"{hour}:{minute}"
            try:
                await client(functions.account.UpdateProfileRequest(about=bio))
            except:
                pass
        await asyncio.sleep(60)

def register(client, config, data_path):
    @client.on(events.NewMessage(pattern=r"\.فعال سازی ساعت بیو"))
    async def enable_bio_clock(event):
        bio_status["enabled"] = True
        await event.respond("✅ ساعت بیو فعال شد.")

    @client.on(events.NewMessage(pattern=r"\.غیرفعال سازی ساعت بیو"))
    async def disable_bio_clock(event):
        bio_status["enabled"] = False
        await event.respond("⛔ ساعت بیو غیرفعال شد.")

    client.loop.create_task(update_bio_loop(client))
    