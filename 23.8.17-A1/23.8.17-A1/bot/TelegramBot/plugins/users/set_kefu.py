from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
from TelegramBot.helpers.functions import markdown
from TelegramBot.loggings import logger


@Client.on_message(filters.regex(r"^设置客服") & filters.group & au_cmd)
@ratelimiter
async def set_kefu(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        # rule = str(markdown(message).split("设置担保规则")[1])
        kefu = str(markdown(message).split("设置客服")[1])
        logger(__name__).info(f"{kefu}")
        if kefu != "":
            try:
                await database.set_kefu(message.chat.id, kefu)
                await message.reply_text(f"客服设置成功！", quote=False)
            except ValueError as e:
                pass
        else:
            await message.reply_text(f"客服已删除！", quote=False)
    else:
        await message.reply_text("您的授权已过期！", quote=False)