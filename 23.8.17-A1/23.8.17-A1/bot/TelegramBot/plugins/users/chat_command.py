from pyrogram import Client
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *
import numexpr as ne

ne.set_num_threads(4)


@Client.on_message(filters.regex(r"^地址") & filters.group, group=7)
@ratelimiter
async def chat_address(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        address = await database.get_address(message.chat.id)
        try:
            if address != "0":
                await message.reply_text(f"下发地址：{address}\n\n点击上方地址，👆🏻即可复制地址", quote=False)
            else:
                pass
        except ValueError as e:
            pass
    else:
        pass


@Client.on_message(filters.regex(r"^显示押金") & filters.group, group=7)
@ratelimiter
async def show_over(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        data = await database.get_config(message.chat.id)
        warn_u = data["warn_u"]
        warn_rmb = data["warn_rmb"]
        try:
            message_text = f"当前押金：{warn_u} U\n当前押金：{warn_rmb} "
            await message.reply_text(message_text, quote=False)
        except ValueError as e:
            pass
    else:
        pass


@Client.on_message(filters.regex(r"^担保规则") & filters.group, group=7)
@ratelimiter
async def chat_rule(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        rule = await database.get_rule(message.chat.id)
        try:
            if rule != "0":
                await message.reply_text(f"{rule}", quote=False)
            else:
                pass
        except ValueError as e:
            pass
    else:
        pass


@Client.on_message(filters.regex(r"^客服") & filters.group, group=7)
@ratelimiter
async def chat_service(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        service = await database.get_kefu(message.chat.id)
        try:
            if service != "0":
                await message.reply_text(f"{service}", quote=False)
            else:
                await message.reply_text(f"没有客服哦~", quote=False)
        except ValueError as e:
            pass
    else:
        pass


@Client.on_message(filters.regex(r'^(\d+(?:\.\d+)?(?:(?:[\+\-\*\/]\d+(?:\.\d+)?)+))$') & filters.group, group=6)
@ratelimiter
async def calculator(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        expression = message.text
        try:
            result = round(float(ne.evaluate(expression)), 3)
            await message.reply_text(f"计算结果：{result}", quote=True)
        except ValueError as e:
            pass
    else:
        pass


# @Client.on_message(filters.command(["m"]) & filters.private & au_cmd)
# async def markdown(_, message: Message):
#     ccc = """< b>加粗< /b>
# < i>斜体< /i>
# < u>下划线< /u>
# < s>删除线< /s>
# < spoiler>剧透效果< /spoiler>
# < a href="https://baidu.com/">文字链接< /a>  网址
# < code>可复制文本< /code>"""
#     text = "以下语法支持 欢迎语句 中使用\n\n{name}  用户名称\n{username}  用户名\n{id}  用户ID"
#     await message.reply_text(text, quote=False)
#     await message.reply_text("通用语法 使用时请把<>标签内的空格删除\n\n" + ccc, quote=False,
#                              disable_web_page_preview=True)
