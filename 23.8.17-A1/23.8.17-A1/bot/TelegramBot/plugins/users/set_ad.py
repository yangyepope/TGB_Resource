from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
from TelegramBot.loggings import logger


# 规则：设置链接+链接名称+网址
@Client.on_message(filters.regex(r"^设置链接") & filters.group & au_cmd)
@ratelimiter
async def set_ad(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        ad_url_name = str(message.text.split("+")[1])
        ad_url = str(message.text.split("+")[2])
        data = str(ad_url_name + "+" + ad_url)
        try:
            await database.set_ad(message.chat.id, data)
            await message.reply_text(f"链接设置成功！", quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


# 删除链接
@Client.on_message(filters.regex(r"^删除链接") & filters.group & au_cmd)
@ratelimiter
async def del_ad(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        # ad_url_name = str(message.text.split("删除链接")[1])
        try:
            await database.del_ad(message.chat.id)
            await message.reply_text(f"自定义广告删除成功！", quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)
