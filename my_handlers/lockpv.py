from telethon import events
from utils import save_config

def register(client, config, data_path):
    if "features" not in config:
        config["features"] = {}
    if "lockpv" not in config["features"]:
        config["features"]["lockpv"] = False
        save_config(data_path, config)

    @client.on(events.NewMessage(incoming=True))
    async def delete_private_message(event):
        if config["features"].get("lockpv") and event.is_private and not event.out:
            try:
                await event.delete()
            except:
                pass

    @client.on(events.NewMessage(pattern=r'^\.فعال سازی قفل پیوی$'))
    async def enable_lockpv(event):
        config["features"]["lockpv"] = True
        save_config(data_path, config)
        await event.reply("🔒 قفل پیوی فعال شد.")

    @client.on(events.NewMessage(pattern=r'^\.غیرفعال سازی قفل پیوی$'))
    async def disable_lockpv(event):
        config["features"]["lockpv"] = False
        save_config(data_path, config)
        await event.reply("🔓 قفل پیوی غیرفعال شد.")
        