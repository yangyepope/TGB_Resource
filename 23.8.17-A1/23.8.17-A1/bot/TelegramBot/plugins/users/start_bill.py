from pyrogram import Client
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *


@Client.on_message(filters.regex(r"^开始$") & filters.group & op_cmd)
@ratelimiter
async def start_bill(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        config = await database.get_config(message.chat.id)
        if config['rate'] == -1:
            await message.reply_text("请先设置费率", quote=False)
        else:
            if config['state']:
                await message.reply_text("已经开始了，请继续记账", quote=False)
            else:
                await message.reply_text("您可以开始在群里记账啦", quote=True)
                await database.set_status(message.chat.id, True)
    else:
        await message.reply_text("您的授权已过期！", quote=False)
