from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
from TelegramBot.loggings import logger
from TelegramBot.helpers.functions import markdown


@Client.on_message(filters.regex(r"^设置担保规则") & filters.group & au_cmd)
@ratelimiter
async def set_rule(_, message: Message):
    # logger(__name__).info(f"{message}")
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        rule = str(markdown(message).split("设置担保规则")[1])
        if rule != "":
            try:
                await database.set_rule(message.chat.id, rule)
                await message.reply_text(f"担保规则设置成功！", quote=False)
            except ValueError as e:
                pass
        else:
            await message.reply_text(f"担保规则已删除！", quote=False)
    else:
        await message.reply_text("您的授权已过期！", quote=False)
