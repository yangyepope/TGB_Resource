from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
from TelegramBot.loggings import logger
from TelegramBot import bot
from TelegramBot.helpers.functions import get_time_range


@Client.on_message((filters.regex(r"^清理今天数据") | filters.regex(r"^删除今天数据")) & filters.group & au_cmd)
@ratelimiter
async def clen_bill(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # owner = await database.is_owner(message.chat.id, message.from_user.id)
    # if owner:
    if authorized:
        start_time, end_time = get_time_range()
        await database.del_bill_by_timestamp(message.chat.id, start_time, end_time)
        await message.reply_text(f"清理今天数据成功！", quote=False)

    else:
        await message.reply_text("您的授权已过期！", quote=False)
