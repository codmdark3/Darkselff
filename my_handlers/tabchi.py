import asyncio
from telethon import events
from utils import save_config

def register_tabchi(client, config, data_path):
    tabchi = config["features"].get("tabchi", {})

    if "enabled" not in tabchi:
        tabchi["enabled"] = False
    if "groups" not in tabchi:
        tabchi["groups"] = []
    if "message" not in tabchi:
        tabchi["message"] = "پیام پیش‌فرض تبچی"
    if "delay" not in tabchi:
        tabchi["delay"] = 5  # دقیقه

    save_config(data_path, config)

    @client.on(events.NewMessage(pattern=r"^\.افزودن گروه تبچی$"))
    async def add_group(event):
        if event.is_group or event.is_channel:
            group_id = event.chat_id
            if group_id not in tabchi["groups"]:
                tabchi["groups"].append(group_id)
                save_config(data_path, config)
                await event.reply("گروه با موفقیت به لیست تبچی افزوده شد.")
            else:
                await event.reply("این گروه قبلاً اضافه شده.")
        else:
            await event.reply("فقط در گروه‌ها می‌تونی این دستور رو بزنی.")

    @client.on(events.NewMessage(pattern=r"^\.حذف گروه تبچی$"))
    async def remove_group(event):
        if event.is_group or event.is_channel:
            group_id = event.chat_id
            if group_id in tabchi["groups"]:
                tabchi["groups"].remove(group_id)
                save_config(data_path, config)
                await event.reply("گروه از لیست تبچی حذف شد.")
            else:
                await event.reply("این گروه داخل لیست نیست.")
        else:
            await event.reply("فقط در گروه‌ها می‌تونی این دستور رو بزنی.")

    @client.on(events.NewMessage(pattern=r"^\.تنظیم پیام تبچی (.+)$"))
    async def set_tabchi_msg(event):
        text = event.pattern_match.group(1)
        tabchi["message"] = text
        save_config(data_path, config)
        await event.reply("پیام تبچی تنظیم شد.")

    @client.on(events.NewMessage(pattern=r"^\.تنظیم فاصله تبچی (\d+)$"))
    async def set_delay(event):
        delay = int(event.pattern_match.group(1))
        tabchi["delay"] = delay
        save_config(data_path, config)
        await event.reply(f"فاصله زمانی تبچی تنظیم شد روی {delay} دقیقه.")

    @client.on(events.NewMessage(pattern=r"^\.فعال سازی تبچی$"))
    async def enable_tabchi(event):
        tabchi["enabled"] = True
        save_config(data_path, config)
        await event.reply("تبچی فعال شد.")

    @client.on(events.NewMessage(pattern=r"^\.غیرفعال سازی تبچی$"))
    async def disable_tabchi(event):
        tabchi["enabled"] = False
        save_config(data_path, config)
        await event.reply("تبچی غیرفعال شد.")

    async def tabchi_loop():
        await client.connect()
        print("[TABCHI] در حال اجرا...")

        while True:
            if tabchi.get("enabled", False):
                print("[TABCHI] فعال است. ارسال پیام به گروه‌ها...")
                for group_id in tabchi.get("groups", []):
                    try:
                        await client.send_message(group_id, tabchi.get("message", "پیام تبچی"))
                        print(f"[TABCHI] پیام به گروه {group_id} ارسال شد.")
                    except Exception as e:
                        print(f"[TABCHI] خطا در ارسال پیام به {group_id}: {e}")
                await asyncio.sleep(tabchi.get("delay", 5) * 60)
            else:
                print("[TABCHI] غیرفعاله. صبر می‌کنیم...")
                await asyncio.sleep(10)

    client.loop.create_task(tabchi_loop())
    