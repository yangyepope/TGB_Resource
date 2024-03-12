from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot import bot
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.loggings import logger


@Client.on_message(filters.new_chat_members, group=9)
@ratelimiter
async def new_chat(_, message: Message):
    """
    Get notified when someone add bot in the group, then saves that group chat_id
    in the database.
    """
    chat_id = message.chat.id

    for new_user in message.new_chat_members:
        if new_user.id == bot.me.id:  # 新进来的人是不是自己？
            # 增加一个判断，拉进来的这个人是不是被授权的人
            # 如果是被授权的，该怎么办？就把这主人设置为这个群的owner
            all_users = await database.get_all_users()
            # n = 0
            zhu_id = 0
            for i in all_users:
                sq_list = str(i['shouquan']).split(',')
                logger(__name__).info(f"{sq_list}")
                logger(__name__).info(f"{message.from_user.id}")
                for z in sq_list:
                    if str(message.from_user.id) == z:
                        zhu_id = sq_list[0]
                        break
            logger(__name__).info(f"主权{zhu_id}")
            await database.save_chat(chat_id, zhu_id)
            authorized = await database.check_permissions(message.chat.id)
            if authorized:  # 检查这个群有权限使用不？
                await message.reply_text("感谢您把我添加到贵群!\n下一步设置费率，请发：设置费率x%", quote=False)
            else:
                await message.reply_text("您没有权限使用本机器人！", quote=False)
            logger(__name__).info(f"bot added to group {chat_id} from {message.from_user.id}")

        else:  # 新用户进群
            try:
                welcome = await database.get_welcome(chat_id)
                # {name}
                # {uername}
                # {id}
                if welcome != "0":
                    try:
                        welcome = welcome.replace("{name}", new_user.first_name)
                    except:
                        welcome = welcome.replace("{name}", "")
                    try:
                        welcome = welcome.replace("{username}", new_user.username)
                    except:
                        welcome = welcome.replace("{username}", "")
                    try:
                        welcome = welcome.replace("{id}", str(new_user.id))
                    except:
                        welcome = welcome.replace("{id}", "")
                    await message.reply_text(welcome, quote=False)
            except Exception as e:
                # logger(__name__).error(e)
                pass
