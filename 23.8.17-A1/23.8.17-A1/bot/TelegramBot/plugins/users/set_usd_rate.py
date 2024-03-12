from pyrogram import Client
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *


@Client.on_message(filters.regex(r"设置美元汇率") & filters.group & op_cmd)
@ratelimiter
async def set_usd_rate(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    config = await database.get_config(message.chat.id)
    if authorized:
        rate = message.text.split("设置美元汇率")[1]
        await database.set_warn(message.chat.id, 'warn_u', 0)
        await database.set_warn(message.chat.id, 'warn_rmb', 0)
        if rate != "":
            if config["usd_rate"] == 0:
                try:
                    await database.set_usd_rate(message.chat.id, float(rate))
                    await message.reply_text(f"设置成功，请<code>设置押金</code>！", quote=False)
                except ValueError as e:
                    pass
            else:
                await database.set_usd_rate(message.chat.id, float(rate))
                await message.reply_text(f"更改成功，美元汇率：{rate}，请重新<code>设置押金</code>！", quote=False)
        else:
            await database.set_usd_rate(message.chat.id, 0)
            await message.reply_text(f"汇率已删除！，请重新<code>设置押金</code>！", quote=False)

    else:
        await message.reply_text("您的授权已过期！", quote=False)
