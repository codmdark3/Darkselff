from telethon import events
import random

def register(client, config, data_path):
    fortunes = [
        "✨ امروز روز خوبی برات خواهد بود.",
        "💡 یک فکر جدید در ذهنته، عملی‌ش کن.",
        "🔥 منتظر یه خبر خوب باش.",
        "🍀 شاید یه شانس ناگهانی بیاد سراغت.",
        "💔 مراقب دل خودت باش.",
        "🧠 امروز زمان خوبیه برای یاد گرفتن یه چیز جدید.",
        "😎 موفقیت نزدیکه فقط ادامه بده."
    ]

    @client.on(events.NewMessage(pattern=r'^\.فال$'))
    async def fortune(event):
        if event.is_private or event.chat_id == "me":
            msg = random.choice(fortunes)
            await event.reply(msg)
            