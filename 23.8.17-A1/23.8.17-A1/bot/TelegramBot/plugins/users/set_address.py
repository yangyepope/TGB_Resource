from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
from TelegramBot.loggings import logger
from TelegramBot.helpers.functions import markdown


@Client.on_message(filters.regex(r"^设置下发地址") & filters.group & au_cmd)
@ratelimiter
async def set_address(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # operator = await database.is_operator(message.chat.id, message.from_user.id)
    # if operator:
    if authorized:
        # address = str(message.text.split("设置下发地址")[1])
        address = str(markdown(message).split("设置下发地址")[1])

        copy = address.split("\n")[0]
        address = address.replace(copy, f"<code>{copy}</code>")
        logger(__name__).info(f"{address}")
        if address != "":
            try:
                await database.set_address(message.chat.id, address)
                await message.reply_text(f"设置成功！下发地址已设置为{address}", quote=False)
            except ValueError as e:
                pass
        else:
            await message.reply_text(f"下发地址已删除！", quote=False)

    else:
        await message.reply_text("您的授权已过期！", quote=False)
