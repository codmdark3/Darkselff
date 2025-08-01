import asyncio
import logging
from selfbot.client import create_all_clients
import handlers_loader
from my_handlers import star_opener  # ✅ اضافه شد

from flask import Flask  # ✅ اضافه شد
from threading import Thread  # ✅ اضافه شد

# 🔹 تنظیمات لاگ برای دیباگ
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

# 🔸 فونت زیباتر برای کلمه DARK
DARK_LOGO = "𝐃𝐀𝐑𝐊"

# ✅ وب سرور برای زنده نگه‌داشتن پروژه
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def start_all():
    clients = create_all_clients()
    if not clients:
        logging.error("❌ هیچ اکانتی پیدا نشد! فایل‌های سشن یا config ناقص هستند.")
        return

    for phone, info in clients.items():
        client = info["client"]
        config = info["config"]
        data_path = info["data_path"]

        try:
            await client.start(phone=config["phone"])
            logging.info(f"📱 اکانت {phone} وصل شد.")

            # 🛠️ ثبت تمام هندلرها
            handlers_loader.register_all(client, config, data_path)
            star_opener.register(client, config, data_path)  # ✅ بازشو

            # ✅ ارسال پیام خوش‌آمد به Saved Messages
            me = await client.get_me()
            first_name = me.first_name or "کاربر"

            welcome_msg = f"""
💀 خوش اومدی <b>{first_name}</b>

سلف‌بات <b>{DARK_LOGO}</b> فعاله. با دستور <code>.منو</code> کنترلش کن.
""".strip()

            await client.send_message("me", welcome_msg, parse_mode='html')

        except Exception as e:
            logging.exception(f"❗ خطا در اتصال اکانت {phone}: {e}")

    logging.info("🚀 همه اکانت‌ها فعال شدن!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        keep_alive()  # ✅ اجرای وب‌سرور برای جلوگیری از خاموشی
        asyncio.run(start_all())
    except KeyboardInterrupt:
        logging.info("🛑 برنامه متوقف شد توسط کاربر.")
        