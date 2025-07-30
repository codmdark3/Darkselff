from telethon.sync import TelegramClient

api_id = 18904273
api_hash = 'c4c73c3f8cb89f6a7672efa8ab065f95'

client = TelegramClient('session_2', api_id, api_hash)
client.start()
print("Session saved as session_2.session")
