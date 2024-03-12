from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import dev_cmd
from TelegramBot.helpers.filters import *


@Client.on_message(filters.regex(r"^设置显示模式") & filters.group & op_cmd)
@ratelimiter
async def set_bill_display1(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        num = int(message.text.replace("设置显示模式", ""))
        if 2 <= num <= 4:
            try:
                await database.set_bill_display1(message.chat.id, num)
                await message.reply_text(f"设置成功！", quote=False)
            except ValueError as e:
                pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^设置为原始模式") & filters.group & op_cmd)
@ratelimiter
async def set_bill_display2(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        num = 1
        if num == 1:
            try:
                await database.set_bill_display1(message.chat.id, num)
                await message.reply_text(f"设置成功！", quote=False)
            except ValueError as e:
                pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^设置为计数模式") & filters.group & op_cmd)
@ratelimiter
async def set_bill_display3(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        num = 5
        if num == 5:
            try:
                await database.set_bill_display1(message.chat.id, num)
                await message.reply_text(f"设置成功！", quote=False)
            except ValueError as e:
                pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)