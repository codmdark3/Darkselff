import json
import os

def save_config(data_path: str, config: dict):
    """ذخیره تنظیمات در فایل config.json داخل مسیر داده شده."""
    print(f"[DEBUG] save_config called with:")
    print(f"  data_path = {data_path} ({type(data_path)})")
    print(f"  config = {config} ({type(config)})")

    if not isinstance(data_path, str):
        raise TypeError(f"❌ data_path باید str باشه، الان هست: {type(data_path)}")

    os.makedirs(data_path, exist_ok=True)
    file_path = os.path.join(data_path, "config.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def load_config(data_path: str) -> dict:
    """بارگذاری تنظیمات از فایل config.json"""
    file_path = os.path.join(data_path, "config.json")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    return {}  # در صورتی که فایل وجود نداشته باشد، دیکشنری خالی برمی‌گرداند

def get_phone(event):
    """
    گرفتن شماره یا شناسه اکانت از روی رویداد تلگرام (Telethon event).
    در اینجا نام فایل سشن (session) بدون پسوند برگشت داده می‌شود.
    """
    # event.client.session.filename معمولاً نام فایل سشن است
    session_name = str(event.client.session.filename)
    # حذف پسوند .session
    phone = session_name.replace(".session", "")
    return phone
    