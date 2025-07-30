from telethon import events, functions

def register(client, config, data_path):
    client.ghost_mode = config["features"].get("ghost", False)

    @client.on(events.NewMessage(pattern="^.فعال سازی حالت روح$"))
    async def enable_ghost(event):
        config["features"]["ghost"] = True
        client.ghost_mode = True
        await client(functions.account.UpdateStatusRequest(offline=True))
        await event.reply("🕴️ حالت روح + آفلاین فعال شد.")

    @client.on(events.NewMessage(pattern="^.غیرفعال سازی حالت روح$"))
    async def disable_ghost(event):
        config["features"]["ghost"] = False
        client.ghost_mode = False
        await client(functions.account.UpdateStatusRequest(offline=False))
        await event.reply("🙈 حالت روح غیرفعال شد.")
        