from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import dev_cmd
from TelegramBot import bot
from TelegramBot.loggings import logger


@Client.on_message(filters.left_chat_member)
async def exit_group(_, message: Message):
    # logger(__name__).info(f"{message.left_chat_member }")
    try:
        if message.left_chat_member.id == bot.me.id:
            await database.delete_chat(message.chat.id)
            await database.del_add_bill(message.chat.id)
            await database.del_out_bill(message.chat.id)
            # logger(__name__).info(f"bot left group {message.chat.id}")
    except AttributeError as e:
        pass






