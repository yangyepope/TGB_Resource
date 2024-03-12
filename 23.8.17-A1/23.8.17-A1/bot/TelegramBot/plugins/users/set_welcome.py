from pyrogram import Client
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
from TelegramBot.helpers.functions import markdown


@Client.on_message(filters.regex(r"^设置欢迎信息") & filters.group & au_cmd)
@ratelimiter
async def set_welcome(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        t = '''用户名称：{name}  
用户名：{username}
用户ID：{id} 
欢迎加入此群！\n\n'''
        welcome = t + str(markdown(message).split("设置欢迎信息")[1])
        try:
            await database.set_welcome(message.chat.id, welcome)
            await message.reply_text(f"欢迎信息设置成功！", quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)
