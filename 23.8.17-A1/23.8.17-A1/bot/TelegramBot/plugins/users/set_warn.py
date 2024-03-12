from pyrogram import Client
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import *


@Client.on_message(filters.regex(r"^设置押金") & filters.group & au_cmd)
@ratelimiter
async def set_warn_m(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        text = str(message.text.split("设置押金")[1]).upper()
        await database.update_over(message.chat.id, False)
        if text != "":
            if text.find("U") != -1:
                warn_u = float(text.split("U")[0])
                await database.set_warn(message.chat.id, 'warn_u', warn_u)
                await message.reply_text(f"押金已设置为 {warn_u} USD", quote=False)
            else:
                warn_rmb = float(text)
                await database.set_warn(message.chat.id, 'warn_rmb', warn_rmb)
                await message.reply_text(f"押金已设置为 {warn_rmb} ", quote=False)

        else:
            await message.reply_text(f"押金已删除！", quote=False)
            await database.set_warn(message.chat.id, 'warn_u', 0)
            await database.set_warn(message.chat.id, 'warn_rmb', 0)
    else:
        await message.reply_text("您的授权已过期！", quote=False)


