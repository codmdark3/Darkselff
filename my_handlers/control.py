from telethon import events
from utils import save_config

def register(client, config, data_path):
    @client.on(events.NewMessage(pattern="/خاموش", incoming=True))
    async def disable_selfbot(event):
        if not event.is_private:
            return

        config["selfbot_enabled"] = False
        save_config(data_path, config)
        await event.reply("❌ سلف‌بات خاموش شد.")

    @client.on(events.NewMessage(pattern="/روشن", incoming=True))
    async def enable_selfbot(event):
        if not event.is_private:
            return

        config["selfbot_enabled"] = True
        save_config(data_path, config)
        await event.reply("✅ سلف‌بات روشن شد.")

    @client.on(events.NewMessage(pattern="/وضعیت", incoming=True))
    async def show_status(event):
        if not event.is_private:
            return

        enabled = config.get("selfbot_enabled", True)
        features = config.get("features", {})

        msg = f"🟢 وضعیت کلی: {'فعال ✅' if enabled else 'خاموش ❌'}\n\n"
        msg += "📦 فیچرهای فعال:\n"

        for key, value in features.items():
            if isinstance(value, dict):
                status = value.get("enabled", False)
            else:
                status = value
            if status:
                msg += f"✔️ {key}\n"

        await event.reply(msg)
        