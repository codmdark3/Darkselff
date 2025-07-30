from telethon import events
import asyncio

tagging_tasks = {}

def register(client, config, data_path):

    @client.on(events.NewMessage(pattern=r"\.تگ همه", outgoing=True))
    async def tag_all_handler(event):
        me = await client.get_me()
        if event.sender_id != me.id:
            return  # فقط خود صاحب اکانت اجازه داره

        if not event.is_group:
            await event.reply("این دستور فقط در گروه کار می‌کند.")
            return

        if not event.is_reply:
            await event.reply("لطفاً روی پیامی ریپلای کن و بعد این دستور رو بزن.")
            return

        reply = await event.get_reply_message()
        chat = await event.get_chat()
        users = []
        async for user in client.iter_participants(chat):
            if not user.bot and not user.deleted:
                users.append(user)

        if not users:
            await event.reply("هیچ کاربر فعالی برای تگ کردن پیدا نشد.")
            return

        task = asyncio.create_task(tag_users(client, event, reply, users))
        tagging_tasks[event.chat_id] = task


    async def tag_users(client, event, reply, users):
        total_tagged = 0
        group_size = 6
        for i in range(0, len(users), group_size):
            chunk = users[i:i+group_size]
            if event.chat_id not in tagging_tasks:
                await event.reply("⛔ تگ کردن لغو شد.")
                return

            tags = " ".join([f"[‌](tg://user?id={u.id})" for u in chunk])
            try:
                await client.send_message(event.chat_id, tags, reply_to=reply.id, link_preview=False)
            except:
                pass

            total_tagged += len(chunk)
            await asyncio.sleep(2.5)

        del tagging_tasks[event.chat_id]
        await event.reply(f"✅ تگ کردن تمام شد. مجموعاً {total_tagged} نفر تگ شدند.")

    @client.on(events.NewMessage(pattern=r"\.لغو تگ", outgoing=True))
    async def cancel_tag(event):
        me = await client.get_me()
        if event.sender_id != me.id:
            return  # فقط صاحب اکانت اجازه لغو داره

        task = tagging_tasks.pop(event.chat_id, None)
        if task:
            task.cancel()
            await event.reply("⛔ عملیات تگ کردن لغو شد.")
        else:
            await event.reply("❌ هیچ عملیات تگی در حال اجرا نیست.")
            