from telethon import events
import random
import json
import os

friends = set()
enemies = set()
friend_messages = ["سلام رفیق!"]
enemy_messages = ["خفه شو 😡"]

DATA_FILE = "data/friends_enemies.json"

def save_data():
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "friends": list(friends),
            "enemies": list(enemies),
            "friend_messages": friend_messages,
            "enemy_messages": enemy_messages
        }, f, ensure_ascii=False)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            friends.update(data.get("friends", []))
            enemies.update(data.get("enemies", []))
            friend_messages[:] = data.get("friend_messages", [])
            enemy_messages[:] = data.get("enemy_messages", [])

def register(client, config, data_path):
    load_data()

    @client.on(events.NewMessage(pattern=r"\.دوست$", func=lambda e: e.is_reply))
    async def add_friend(event):
        reply = await event.get_reply_message()
        if reply:
            friends.add(reply.sender_id)
            save_data()
            await event.reply("✅ طرف به لیست دوستان اضافه شد.")

    @client.on(events.NewMessage(pattern=r"\.دشمن$", func=lambda e: e.is_reply))
    async def add_enemy(event):
        reply = await event.get_reply_message()
        if reply:
            enemies.add(reply.sender_id)
            save_data()
            await event.reply("❌ طرف به لیست دشمنان اضافه شد.")

    @client.on(events.NewMessage(pattern=r"\.حذف دوست$", func=lambda e: e.is_reply))
    async def remove_friend(event):
        reply = await event.get_reply_message()
        if reply and reply.sender_id in friends:
            friends.remove(reply.sender_id)
            save_data()
            await event.reply("🗑 از لیست دوستان حذف شد.")

    @client.on(events.NewMessage(pattern=r"\.حذف دشمن$", func=lambda e: e.is_reply))
    async def remove_enemy(event):
        reply = await event.get_reply_message()
        if reply and reply.sender_id in enemies:
            enemies.remove(reply.sender_id)
            save_data()
            await event.reply("🗑 از لیست دشمنان حذف شد.")

    @client.on(events.NewMessage(pattern=r"\.افزودن پیام دوست (.+)"))
    async def add_friend_msg(event):
        msg = event.pattern_match.group(1).strip()
        if msg:
            friend_messages.append(msg)
            save_data()
            await event.reply("✅ پیام جدید برای دوستان اضافه شد.")

    @client.on(events.NewMessage(pattern=r"\.افزودن پیام فش (.+)"))
    async def add_enemy_msg(event):
        msg = event.pattern_match.group(1).strip()
        if msg:
            enemy_messages.append(msg)
            save_data()
            await event.reply("✅ پیام فحش برای دشمنان اضافه شد.")

    @client.on(events.NewMessage(pattern=r"\.لیست پیام دوست"))
    async def list_friend_msgs(event):
        if not friend_messages:
            await event.reply("📭 هیچ پیام دوستی ثبت نشده.")
        else:
            text = "📋 لیست پیام‌های دوستان:\n\n"
            text += "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(friend_messages)])
            await event.reply(text)

    @client.on(events.NewMessage(pattern=r"\.لیست پیام فش"))
    async def list_enemy_msgs(event):
        if not enemy_messages:
            await event.reply("📭 هیچ پیام فحش ثبت نشده.")
        else:
            text = "📋 لیست پیام‌های فحش:\n\n"
            text += "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(enemy_messages)])
            await event.reply(text)

    @client.on(events.NewMessage(pattern=r"\.لیست دوست ها"))
    async def list_friends(event):
        if not friends:
            await event.reply("📭 هیچ دوستی ثبت نشده.")
        else:
            text = "📋 لیست دوستان:\n\n"
            text += "\n".join([f"`{uid}`" for uid in friends])
            await event.reply(text)

    @client.on(events.NewMessage(pattern=r"\.لیست دشمن ها"))
    async def list_enemies(event):
        if not enemies:
            await event.reply("📭 هیچ دشمنی ثبت نشده.")
        else:
            text = "📋 لیست دشمنان:\n\n"
            text += "\n".join([f"`{uid}`" for uid in enemies])
            await event.reply(text)

    # حذف پیام دوست از لیست
    @client.on(events.NewMessage(pattern=r"\.حذف پیام دوست (\d+)"))
    async def delete_friend_msg(event):
        index = int(event.pattern_match.group(1)) - 1
        if 0 <= index < len(friend_messages):
            removed = friend_messages.pop(index)
            save_data()
            await event.reply(f"🗑 پیام دوست حذف شد:\n{removed}")
        else:
            await event.reply("❌ شماره پیام معتبر نیست.")

    # حذف پیام فش از لیست
    @client.on(events.NewMessage(pattern=r"\.حذف پیام فش (\d+)"))
    async def delete_enemy_msg(event):
        index = int(event.pattern_match.group(1)) - 1
        if 0 <= index < len(enemy_messages):
            removed = enemy_messages.pop(index)
            save_data()
            await event.reply(f"🗑 پیام فحش حذف شد:\n{removed}")
        else:
            await event.reply("❌ شماره پیام معتبر نیست.")

# پاسخ خودکار
    @client.on(events.NewMessage(incoming=True))
    async def auto_reply(event):
        sender = await event.get_sender()
        if not sender:
            return  # اگر فرستنده None بود، بی‌خیال شو

        if sender.bot or event.out:
            return

        if sender.id in friends and friend_messages:
            await event.reply(random.choice(friend_messages))
        elif sender.id in enemies and enemy_messages:
            await event.reply(random.choice(enemy_messages))
            