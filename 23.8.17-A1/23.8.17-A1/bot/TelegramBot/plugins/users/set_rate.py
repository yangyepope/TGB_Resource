from pyrogram import Client
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *


@Client.on_message(filters.regex(r"^设置费率\d{0,2}(\.\d+)?%?$") & filters.group & op_cmd)
@ratelimiter
async def set_rate(_, message: Message):
    await database.update_over(message.chat.id, False)
    authorized = await database.check_permissions(message.chat.id)
    config = await database.get_config(message.chat.id)
    old_rate = config["rate"]
    if authorized:
        rate = message.text.split("设置费率")[1].replace("%", "")
        rate = float(rate) / 100
        if old_rate == -1:
            try:
                await database.set_rate(message.chat.id, float(rate))
                await message.reply_text(f"设置成功！接下来发送[开始]就能使用", quote=False)
            except ValueError as e:
                pass
        else:
            try:
                await database.set_rate(message.chat.id, float(rate))
                await message.reply_text(f"更改成功！", quote=False)
            except ValueError as e:
                pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)
