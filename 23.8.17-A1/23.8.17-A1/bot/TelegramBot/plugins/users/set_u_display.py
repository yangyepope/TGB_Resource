from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import dev_cmd
from TelegramBot.helpers.filters import *


@Client.on_message(filters.regex(r"^账单显示U开启") & filters.group & op_cmd)
@ratelimiter
async def set_u_display(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        # rate = message.text.split("设置费率")[1].split("%")[0]
        try:
            await database.set_u_display(message.chat.id, True)
            await message.reply_text(f"设置成功！U账单功能已经开启", quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^账单显示U关闭") & filters.group & op_cmd)
@ratelimiter
async def close_u_display(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        # rate = message.text.split("设置费率")[1].split("%")[0]
        try:
            await database.set_u_display(message.chat.id, False)
            await message.reply_text(f"设置成功！U账单功能已经关闭", quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)
