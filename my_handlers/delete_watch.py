from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage

deleted_messages = {}

def register(client, config, data_path):
    @client.on(events.NewMessage(incoming=True))
    async def store_messages(event):
        if event.is_private:
            sender = await event.get_sender()
            deleted_messages[event.id] = {
                "message": event.message,
                "sender": sender
            }

    @client.on(events.MessageDeleted())
    async def on_delete(event):
        for msg_id in event.deleted_ids:
            data = deleted_messages.get(msg_id)
            if not data:
                continue

            message = data["message"]
            sender = data["sender"]
            username = sender.username or f"ID:{sender.id}"
            caption = message.text or message.raw_text or ""

            header = f"🗑 پیام حذف شده در پیوی\n👤 فرستنده: {username}\n"

            # اگر پیام متنی هست
            if message.message:
                await client.send_message("me", header + "💬 متن پیام:\n" + message.message)
            
            # اگر پیام شامل عکس هست
            elif message.photo:
                await client.send_file("me", message.photo, caption=header + "📷 عکس حذف شده\n" + (caption or ""))
            
            # اگر پیام شامل ویدیو هست
            elif message.video:
                await client.send_file("me", message.video, caption=header + "🎥 ویدیو حذف شده\n" + (caption or ""))
            
            # اگر پیام شامل فایل هست
            elif message.document:
                await client.send_file("me", message.document, caption=header + "📎 فایل حذف شده\n" + (caption or ""))
            
            # اگر پیام شامل ویس هست
            elif message.voice:
                await client.send_file("me", message.voice, caption=header + "🎙 ویس حذف شده\n" + (caption or ""))
            
            else:
                # اگر پیام نوع خاص دیگه‌ای داشت، فقط متن یا اطلاع کلی بفرست
                await client.send_message("me", header + "⚠️ پیام حذف شده نوع ناشناخته داشت.")
                