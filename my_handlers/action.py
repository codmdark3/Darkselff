import asyncio
import os
import json
from telethon import events, functions, types

def register(client, config, data_path):
    settings_file = os.path.join(data_path, "action_settings.json")

    if not os.path.exists(settings_file):
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump({
                "enabled": False,
                "type": "تایپ",
                "scope": "همه"
            }, f, ensure_ascii=False)

    def load_settings():
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_settings(data):
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    @client.on(events.NewMessage(pattern=r"^\.فعال سازی اکشن$"))
    async def enable_action(event):
        data = load_settings()
        data["enabled"] = True
        save_settings(data)
        await event.reply("✅ اکشن فعال شد.")

    @client.on(events.NewMessage(pattern=r"^\.غیرفعال سازی اکشن$"))
    async def disable_action(event):
        data = load_settings()
        data["enabled"] = False
        save_settings(data)
        await event.reply("🛑 اکشن غیرفعال شد.")

    @client.on(events.NewMessage(pattern=r"^\.اکشن (تایپ|صدا|ویدیو|بازی|لغو)$"))
    async def set_type(event):
        action_type = event.pattern_match.group(1)
        data = load_settings()
        data["type"] = action_type
        save_settings(data)
        await event.reply(f"🔧 نوع اکشن روی «{action_type}» تنظیم شد.")

    @client.on(events.NewMessage(pattern=r"^\.اکشن (فقط پیوی|فقط گروه|همه جا)$"))
    async def set_scope(event):
        scope = event.pattern_match.group(1)
        data = load_settings()
        if scope == "فقط پیوی":
            data["scope"] = "pv"
        elif scope == "فقط گروه":
            data["scope"] = "group"
        else:
            data["scope"] = "all"
        save_settings(data)
        await event.reply(f"🌐 محل اجرا روی «{scope}» تنظیم شد.")

    @client.on(events.NewMessage())
    async def perform_action(event):
        data = load_settings()
        if not data.get("enabled", False):
            return

        if event.sender_id == (await client.get_me()).id:
            return

        scope = data.get("scope", "all")
        if scope == "pv" and not event.is_private:
            return
        if scope == "group" and event.is_private:
            return

        action_map = {
            "تایپ": types.SendMessageTypingAction(),
            "صدا": types.SendMessageRecordAudioAction(),
            "ویدیو": types.SendMessageRecordVideoAction(),
            "بازی": types.SendMessageGamePlayAction(),
            "لغو": types.SendMessageCancelAction(),
        }

        action_type = data.get("type", "تایپ")
        action = action_map.get(action_type)
        if action:
            try:
                await client(functions.messages.SetTypingRequest(
                    peer=event.chat_id,
                    action=action
                ))
            except:
                pass
                