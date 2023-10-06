from pyrogram import Client, filters
import shutil
bot = Client('yedek_bot', bot_token='6204154676:AAGx_cTAaJ6Uw90FGZu45_7w3gzOTiv_GmI', api_hash="78dcc9a9d25d1386b508d37774b93f47", api_id=27924368)
import os
@bot.on_message(filters.command('yedek'))
async def yedekal(bot:Client, message):
    try:
        chat_id = message.chat.id
        await bot.send_message(chat_id, 'yedek alınıyor...')
        shutil.make_archive('yedek', 'zip', './')
        await bot.send_message(chat_id, "gönderiliyor...")
        await bot.send_document(chat_id, 'yedek.zip')
        os.remove("yedek.zip")
    except Exception as e:
        await bot.send_message(chat_id, str(e))

bot.run()