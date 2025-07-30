from telethon import events, functions, types
import os
import json
import random

def register(client, config, data_path):
    settings_file = os.path.join(data_path, "reaction_settings.json")

    if not os.path.exists(settings_file):
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump({
                "enabled": False,
                "random": False,
                "emojis": ["❤️"],
                "scope": "both"  # options: "pv", "group", "both"
            }, f, ensure_ascii=False)

    def load_settings():
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_settings(data):
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    @client.on(events.NewMessage(from_users="me", pattern="^\.فعال سازی ری اکشن خودکار$"))
    async def enable_reaction(event):
        data = load_settings()
        data["enabled"] = True
        save_settings(data)
        await event.reply("✅ ری‌اکشن خودکار فعال شد.")

    @client.on(events.NewMessage(from_users="me", pattern="^\.غیرفعال سازی ری اکشن خودکار$"))
    async def disable_reaction(event):
        data = load_settings()
        data["enabled"] = False
        save_settings(data)
        await event.reply("❌ ری‌اکشن خودکار غیرفعال شد.")

    @client.on(events.NewMessage(from_users="me", pattern="^\.ری اکشن خودکار تصادفی روشن$"))
    async def enable_random(event):
        data = load_settings()
        data["random"] = True
        save_settings(data)
        await event.reply("🎲 حالت تصادفی فعال شد.")

    @client.on(events.NewMessage(from_users="me", pattern="^\.ری اکشن خودکار تصادفی خاموش$"))
    async def disable_random(event):
        data = load_settings()
        data["random"] = False
        save_settings(data)
        await event.reply("🛑 حالت تصادفی غیرفعال شد.")

    @client.on(events.NewMessage(from_users="me", pattern=r"^\.تنظیم ایموجی های ری اکشن خودکار (.+)$"))
    async def set_emojis(event):
        emojis = event.pattern_match.group(1).strip().split()
        data = load_settings()
        data["emojis"] = emojis
        save_settings(data)
        await event.reply(f"✅ ایموجی‌ها تنظیم شد: {' '.join(emojis)}")

    @client.on(events.NewMessage(from_users="me", pattern=r"^\.محدوده ری اکشن (پیوی|گروه|همه)$"))
    async def set_scope(event):
        scope_map = {"پیوی": "pv", "گروه": "group", "همه": "both"}
        selected = scope_map.get(event.pattern_match.group(1))
        data = load_settings()
        data["scope"] = selected
        save_settings(data)
        await event.reply(f"📍 محدوده ری‌اکشن روی «{event.pattern_match.group(1)}» تنظیم شد.")

    @client.on(events.NewMessage())
    async def auto_react(event):
        if event.out: return  # پیام خودت نباشه

        data = load_settings()
        if not data.get("enabled", False):
            return

        scope = data.get("scope", "both")
        if scope == "pv" and not event.is_private:
            return
        if scope == "group" and not (event.is_group or event.is_channel):
            return

        emoji = random.choice(data["emojis"]) if data.get("random", False) else data["emojis"][0]
        try:
            await client(functions.messages.SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.id,
                reaction=[types.ReactionEmoji(emoticon=emoji)],
                big=True
            ))
        except:
            pass
            