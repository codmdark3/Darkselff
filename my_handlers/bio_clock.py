import asyncio
from telethon import events, functions
from datetime import datetime
import pytz
import random
import re

def register(client, config=None, data_path=None):
    status = {"bio_clock": False}
    original_bio = {"about": None}

    font_styles = [
        "0123456789",
        "⓿①②③④⑤⑥⑦⑧⑨",
        "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
        "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
        "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
        "０１２３４５６７８９",
        "①②③④⑤⑥⑦⑧⑨⓪",
        "➉➈➇➆➅➄➃➂➁➀"
    ]

    def apply_font(text, font_digits):
        normal_digits = "0123456789"
        return "".join(font_digits[normal_digits.index(ch)] if ch in normal_digits else ch for ch in text)

    async def update_bio_loop():
        while status["bio_clock"]:
            tehran_tz = pytz.timezone("Asia/Tehran")
            now = datetime.now(tehran_tz)
            hour_minute = now.strftime("%H:%M")

            font_digits = random.choice(font_styles)
            styled_time = apply_font(hour_minute, font_digits)

            try:
                full = await client(functions.account.GetFullUserRequest("me"))
                current_bio = full.about or ""

                if original_bio["about"] is None:
                    original_bio["about"] = current_bio

                base_bio = re.sub(r"\s*\|\s*[0-9𝟶-𝟿⓪-⑨➊-➒０-９:٫]+$", "", original_bio["about"]).strip()

                new_bio = f"{base_bio} | {styled_time}"

                await client(functions.account.UpdateProfileRequest(about=new_bio))
            except Exception as e:
                print(f"خطا در آپدیت ساعت بیو: {e}")

            now = datetime.now(tehran_tz)
            seconds_to_next_minute = 60 - now.second - now.microsecond / 1_000_000
            await asyncio.sleep(seconds_to_next_minute)

    @client.on(events.NewMessage(pattern=r"^\.فعال سازی ساعت بیو$", outgoing=True))
    async def enable_bio_clock(event):
        if status["bio_clock"]:
            await event.reply("⚠️ ساعت بیو قبلاً فعال شده.")
            return
        status["bio_clock"] = True
        await event.reply("✅ ساعت کنار بیو فعال شد.")
        client.loop.create_task(update_bio_loop())

    @client.on(events.NewMessage(pattern=r"^\.غیرفعال سازی ساعت بیو$", outgoing=True))
    async def disable_bio_clock(event):
        if not status["bio_clock"]:
            await event.reply("⚠️ ساعت بیو قبلاً غیرفعال است.")
            return
        status["bio_clock"] = False
        await asyncio.sleep(1)
        try:
            full = await client(functions.account.GetFullUserRequest("me"))
            await client(functions.account.UpdateProfileRequest(
                about=original_bio["about"] or full.about or ""
            ))
            await event.reply("❌ ساعت بیو خاموش و متن بیو اصلی برگشت.")
        except Exception as e:
            await event.reply(f"❌ خطا در بازگرداندن بیو: {e}")
            