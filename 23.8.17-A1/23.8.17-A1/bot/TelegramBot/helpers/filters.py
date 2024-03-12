from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from TelegramBot.config import sudo_userid, owner_userid
from TelegramBot.database import database


def dev_users(_, __, message: Message) -> bool:
    return message.from_user.id in owner_userid if message.from_user else False


def sudo_users(_, __, message: Message) -> bool:
    return message.from_user.id in sudo_userid if message.from_user else False


async def operator_users(_, __, message: Message) -> bool:
    operator_userid = await database.get_operator(message.chat.id)
    authorizer_userid = await database.get_authorizer(message.chat.id)
    vip_userid = await database.get_vip(message.chat.id)
    new_userid = list(set(operator_userid + authorizer_userid + vip_userid))
    return str(message.from_user.id) in new_userid if message.from_user else False


async def authorizer_users(_, __, message: Message) -> bool:
    authorizer_userid = await database.get_authorizer(message.chat.id)
    vip_userid = await database.get_vip(message.chat.id)
    new_userid = list(set(authorizer_userid + vip_userid))
    return str(message.from_user.id) in new_userid if message.from_user else False


async def operator_users_query(_, __, callback_query: CallbackQuery) -> bool:
    authorizer_userid = await database.get_authorizer(callback_query.message.chat.id)
    vip_userid = await database.get_vip(callback_query.message.chat.id)
    new_userid = list(set(authorizer_userid + vip_userid))
    return str(callback_query.message.from_user.id) in new_userid if callback_query.message.from_user else False


async def vip_users(_, __, message: Message) -> bool:
    vip_userid = await database.get_vip(message.chat.id)
    return str(message.from_user.id) in vip_userid if message.from_user else False


dev_cmd = filters.create(dev_users)
sudo_cmd = filters.create(sudo_users)
op_cmd = filters.create(operator_users)
op_cmd_query = filters.create(operator_users_query)
au_cmd = filters.create(authorizer_users)
vip_cmd = filters.create(vip_users)
