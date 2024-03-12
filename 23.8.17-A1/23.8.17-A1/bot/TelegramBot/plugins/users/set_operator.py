from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
from TelegramBot.loggings import logger
from TelegramBot import bot


@Client.on_message((filters.regex(r"^设置操作人") | filters.regex(r"^添加操作人")) & filters.group & au_cmd)
@ratelimiter
async def set_operator(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # owner = await database.is_owner(message.chat.id, message.from_user.id)
    # if owner:
    if authorized:
        operators = message.text.replace("设置操作人", "").replace("添加操作人", "").split(" ")[1:]
        logger(__name__).info(f"{operators}")
        if operators:
            n = 0
            for user in operators:
                if user != "":
                    n += 1
                    for i in message.entities:
                        try:  # 如果不报错，就是匿名用户
                            user_name = (i.user.first_name or " ") + (i.user.last_name or "")
                            user_id = i.user.id
                            await database.save_operator(message.chat.id, user_id)
                            await database.save_operator_name(message.chat.id, user_name)
                        except: # 报错
                            if user.find("@") != -1:
                                user = user.replace("@", "")
                                operator = await bot.get_users(user)
                                operator_username = f"@{operator.username}"
                                operator_id = operator.id
                                await database.save_operator(message.chat.id, operator_id)
                                await database.save_operator_name(message.chat.id, operator_username)
            await message.reply_text(f"设置操作人完成， 共增加 {n} 位操作人", quote=False)
        else:
            try:
                logger(__name__).info(f"执行的是回复消息添加操作人")
                operator_id = message.reply_to_message.from_user.id
                name = message.reply_to_message.from_user.username
                if not name:
                    name = message.reply_to_message.from_user.first_name or " " + message.reply_to_message.from_user.last_name or " "
                logger(__name__).info(f"{operator_id} {name}")
                await database.save_operator(message.chat.id, operator_id)
                await database.save_operator_name(message.chat.id, name)
                logger(__name__).info(f"管理员设置了 {operator_id} 为操作人")
                await message.reply_text(f"设置操作人完成， 共增加 {1} 位操作人", quote=False)
            except Exception as e:
                await message.reply_text(f"设置操作人需要**@用户**、或者**回复消息**哦", quote=False)

    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^删除操作人") & filters.group & au_cmd)
@ratelimiter
async def del_operator(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # owner = await database.is_owner(message.chat.id, message.from_user.id)
    # if owner:
    if authorized:
        operators = message.text.replace("删除操作人", "").split(" ")[1:]
        logger(__name__).info(f"{operators}")
        if operators:
            n = 0
            for user in operators:
                if user != "":
                    n += 1
                    for i in message.entities:
                        try:  # 如果不报错，就是匿名用户
                            user_name = (i.user.first_name or " ") + (i.user.last_name or "")
                            user_id = i.user.id
                            await database.del_operator(message.chat.id, user_id)
                            await database.del_operator_name(message.chat.id, user_name)
                        except: # 报错
                            if user.find("@") != -1:
                                user = user.replace("@", "")
                                operator = await bot.get_users(user)
                                operator_username = f"@{operator.username}"
                                operator_id = operator.id
                                await database.del_operator(message.chat.id, operator_id)
                                await database.del_operator_name(message.chat.id, operator_username)
            await message.reply_text(f"删除操作人完成， 共删除 {n} 位操作人", quote=False)
        else:
            try:
                logger(__name__).info(f"执行的是回复消息添加操作人")
                operator_id = message.reply_to_message.from_user.id
                name = message.reply_to_message.from_user.username
                if not name:
                    name = message.reply_to_message.from_user.first_name or " " + message.reply_to_message.from_user.last_name or " "
                logger(__name__).info(f"{operator_id} {name}")
                await database.del_operator(message.chat.id, operator_id)
                await database.del_operator_name(message.chat.id, name)
                logger(__name__).info(f"管理员删除了 {operator_id} 为操作人")
                await message.reply_text(f"删除操作人完成， 共删除 {1} 位操作人", quote=False)
            except Exception as e:
                await message.reply_text(f"删除操作人需要**@用户**、或者**回复消息**哦", quote=False)

    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^显示操作人") & filters.group & au_cmd)
@ratelimiter
async def show_operator(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    # owner = await database.is_owner(message.chat.id, message.from_user.id)
    # if owner:
    if authorized:
        operators = await database.get_operator_name(message.chat.id)
        path = ''
        if operators:
            for user in operators:
                path += f"{user} "
            await message.reply_text(f"当前操作人为：{path}", quote=False)
        else:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)
