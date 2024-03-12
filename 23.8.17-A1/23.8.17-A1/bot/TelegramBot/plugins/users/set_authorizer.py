from pyrogram import Client
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
from TelegramBot import bot
from TelegramBot.loggings import logger


@Client.on_message((filters.regex(r"^设置权限人") | filters.regex(r"^添加权限人")) & filters.group & vip_cmd)
@ratelimiter
async def set_operator(_, message: Message):
    # global c_a
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        operators = message.text.replace("设置权限人", "").replace("添加权限人", "").split(" ")[1:]
        if len(operators) > 5:
            await message.reply_text(f"设置失败，最多能设置5个权限人", quote=False)
            return
        authorizer_num = await database.get_authorizer_num(message.chat.id)
        if authorizer_num >= 7:
            await message.reply_text(f"设置失败，最多能设置5个权限人", quote=False)
            return
        # c_a = True
        if operators:
            n = 0
            for user in operators:
                if user != "":
                    n += 1
                    for i in message.entities:
                        try:
                            user_name = (i.user.first_name or " ") + (i.user.last_name or "")
                            user_id = i.user.id
                            await database.save_authorizer(message.chat.id, user_id)
                            await database.save_authorizer_name(message.chat.id, user_name)
                        except:
                            if user.find("@") != -1:
                                user = user.replace("@", "")
                                operator = await bot.get_users(user)
                                operator_username = f"@{operator.username}"
                                operator_id = operator.id
                                await database.save_authorizer(message.chat.id, operator_id)
                                await database.save_authorizer_name(message.chat.id, operator_username)
            # if c_a:
            if n <= 5:
                await message.reply_text(f"设置权限人完成， 共增加{n}位权限人", quote=False)
            else:
                await message.reply_text(f"已设置前5名用户为权限人！", quote=False)
            # else:
            #     await message.reply_text(f"设置失败，已经超出5个了哦~", quote=False)
        else:
            try:
                #  c = True
                operator_id = message.reply_to_message.from_user.id
                name = message.reply_to_message.from_user.username
                if not name:
                    name = message.reply_to_message.from_user.first_name or " " + message.reply_to_message.from_user.last_name or " "
                c = await database.save_authorizer(message.chat.id, operator_id)
                await database.save_authorizer_name(message.chat.id, name)
                # logger(__name__).info(f"{c} 前面是c 的值")
                # if c:
                await message.reply_text(f"设置权限人完成， 共增加 {1} 位权限人", quote=False)
                # else:
                #     await message.reply_text(f"设置失败，已经超出5个了哦~", quote=False)
            except Exception as e:
                await message.reply_text(f"设置权限人需要**@用户**、或者**回复消息**哦", quote=False)

    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^删除权限人") & filters.group & vip_cmd)
@ratelimiter
async def del_operator(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        operators = message.text.replace("删除权限人", "").split(" ")[1:]
        if operators:
            n = 0
            for user in operators:
                if user != "":
                    n += 1
                    for i in message.entities:
                        try:
                            user_name = (i.user.first_name or " ") + (i.user.last_name or "")
                            user_id = i.user.id
                            await database.del_authorizer(message.chat.id, user_id)
                            await database.del_authorizer_name(message.chat.id, user_name)
                        except:
                            if user.find("@") != -1:
                                user = user.replace("@", "")
                                operator = await bot.get_users(user)
                                operator_username = f"@{operator.username}"
                                operator_id = operator.id
                                await database.del_authorizer(message.chat.id, operator_id)
                                await database.del_authorizer_name(message.chat.id, operator_username)
            await message.reply_text(f"删除权限人完成， 共删除 {n} 位权限人", quote=False)
        else:
            try:
                operator_id = message.reply_to_message.from_user.id
                name = message.reply_to_message.from_user.username
                if not name:
                    name = message.reply_to_message.from_user.first_name or " " + message.reply_to_message.from_user.last_name or " "
                await database.del_authorizer(message.chat.id, operator_id)
                await database.del_authorizer_name(message.chat.id, name)
                await message.reply_text(f"删除权限人完成， 共删除 {1} 位权限人", quote=False)
            except Exception as e:
                await message.reply_text(f"删除权限人需要**@用户**、或者**回复消息**哦", quote=False)

    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^显示权限人") & filters.group & vip_cmd)
@ratelimiter
async def show_operator(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        operators = await database.get_authorizer_name(message.chat.id)
        path = ''
        if operators:
            for user in operators:
                path += f"{user} "
            await message.reply_text(f"当前权限人为：{path}", quote=False)
        else:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)
