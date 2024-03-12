from pyrogram import Client, filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from TelegramBot import bot
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.filters import op_cmd, op_cmd_query
from TelegramBot.helpers.functions import get_okex_price
from TelegramBot.database import database
from TelegramBot.loggings import logger


@Client.on_message(filters.regex(r"^lk$") & filters.group)
# @ratelimiter
async def lk(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        data = await get_okex_price("bank")
        try:
            path = ""
            n = 0
            for i in data[0:10]:
                n += 1
                nick_name = f"买入{n}"
                price = i["price"]
                path += f"{nick_name}：{price}\n"
            text = f"今日欧意**银行卡**实时价格：\n{path}\n命令：\nlk 列出银行卡价格\nlz列出支付宝价格\nlw 列出微信价格"
            await message.reply_text(text, quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^lz$") & filters.group)
# @ratelimiter
async def lz(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        data = await get_okex_price("aliPay")
        try:
            path = ""
            n = 0
            for i in data[0:10]:
                n += 1
                nick_name = f"买入{n}"
                price = i["price"]
                path += f"{nick_name}：{price}\n"
            text = f"今日欧意**支付宝**实时价格：\n{path}\n命令：\nlk 列出银行卡价格\nlz列出支付宝价格\nlw 列出微信价格"
            await message.reply_text(text, quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^lw$") & filters.group)
# @ratelimiter
async def lw(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        data = await get_okex_price("wxPay")
        try:
            path = ""
            n = 0
            for i in data[0:10]:
                n += 1
                nick_name = f"买入{n}"
                price = i["price"]
                path += f"{nick_name}：{price}\n"
            text = f"今日欧意**微信**实时价格：\n{path}\n命令：\nlk 列出银行卡价格\nlz列出支付宝价格\nlw 列出微信价格"
            await message.reply_text(text, quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^[Ww][0-9]\d*(\.\d+)?$") & filters.group)
# @ratelimiter
async def wx_number(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        data = await get_okex_price("wxPay")
        config = await database.get_config(message.chat.id)
        amount = float(message.text.replace("w", "").replace("W", ""))
        gear = int(config['gear'])
        adjust = float(config['adjust'])
        usd_rate = float(config['uuu'])
        try:
            path = ""
            n = 0
            for i in data[0:10]:
                n += 1
                nick_name = f"买入{n}"
                price = i["price"]
                path += f"{nick_name}：{price}\n"
            if usd_rate == 0:
                price1 = round(float(data[gear - 1]["price"]) + adjust, 3)
                setting = f"**{int(config['gear'])}** 档 | 微调 {config['adjust']}"
                if config['mrate'] == 0:
                    fee = 0
                else:
                    fee = round(amount * config['mrate'] / price1, 2)
            else:
                price1 = usd_rate
                setting = f"**固定汇率：{price1}**"
                if config['mrate'] == 0:
                    fee = 0
                else:
                    fee = round(amount * config['mrate'] / price1, 2)
            coins = round((amount / price1) - fee, 2)
            text = f"今日欧意**微信**实时价格：\n{path}\n命令：\nlk 列出银行卡价格\nlz列出支付宝价格\nlw 列出微信价格\n\n当前设置：{setting} | 费率 {config['mrate'] * 100}%\n设置：/usdt \n\n币数：({amount}÷{round(price1,3)}）- {config['mrate'] * 100}%={coins}USDT\n手续费：{config['mrate'] * 100}% = {round(amount * config['mrate'], 2)}RMB = {fee}USDT"
            await message.reply_text(text, quote=False)
        except ValueError as e:
            pass
            # logger(__name__).info(f"Error ：{e}")
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^[zZ][0-9]\d*(\.\d+)?$") & filters.group)
# @ratelimiter
async def zfb_number(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        data = await get_okex_price("aliPay")
        config = await database.get_config(message.chat.id)
        amount = float(message.text.replace("z", "").replace("Z", ""))
        gear = int(config['gear'])
        adjust = float(config['adjust'])
        usd_rate = float(config['uuu'])
        try:
            path = ""
            n = 0
            for i in data[0:10]:
                n += 1
                nick_name = f"买入{n}"
                price = i["price"]
                path += f"{nick_name}：{price}\n"

            if usd_rate == 0:
                price1 = round(float(data[gear - 1]["price"]) + adjust, 3)
                setting = f"**{int(config['gear'])}** 档 | 微调 {config['adjust']}"
                if config['mrate'] == 0:
                    fee = 0
                else:
                    fee = round(amount * config['mrate'] / price1, 2)
            else:
                price1 = usd_rate
                setting = f"**固定汇率：{price1}**"
                if config['mrate'] == 0:
                    fee = 0
                else:
                    fee = round(amount * config['mrate'] / price1, 2)
            coins = round((amount / price1) - fee, 2)
            text = f"今日欧意**支付宝**实时价格：\n{path}\n命令：\nlk 列出银行卡价格\nlz列出支付宝价格\nlw 列出微信价格\n\n当前设置：{setting} | 费率 {config['mrate'] * 100}%\n设置：/usdt \n\n币数：({amount}÷{round(price1,3)}）- {config['mrate'] * 100}%={coins}USDT\n手续费：{config['mrate'] * 100}% = {round(amount * config['mrate'], 2)}RMB = {fee}USDT"
            await message.reply_text(text, quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.regex(r"^[kK][0-9]\d*(\.\d+)?$") & filters.group)
# @ratelimiter
async def k_number(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        data = await get_okex_price("bank")
        config = await database.get_config(message.chat.id)
        amount = float(message.text.replace("k", "").replace("K", ""))
        gear = int(config['gear'])
        adjust = float(config['adjust'])
        usd_rate = float(config['uuu'])
        try:
            path = ""
            n = 0
            for i in data[0:10]:
                n += 1
                nick_name = f"买入{n}"
                price = i["price"]
                path += f"{nick_name}：{price}\n"

            if usd_rate == 0:
                price1 = round(float(data[gear - 1]["price"]) + adjust, 3)
                setting = f"**{int(config['gear'])}** 档 | 微调 {config['adjust']}"
                if config['mrate'] == 0:
                    fee = 0
                else:
                    fee = round(amount * config['mrate'] / price1, 2)
            else:
                price1 = usd_rate
                setting = f"**固定汇率：{price1}**"
                if config['mrate'] == 0:
                    fee = 0
                else:
                    fee = round(amount * config['mrate'] / price1, 2)
            coins = round((amount / price1) - fee, 2)
            text = f"今日欧意**银行卡**实时价格：\n{path}\n命令：\nlk 列出银行卡价格\nlz列出支付宝价格\nlw 列出微信价格\n\n当前设置：{setting} | 费率 {config['mrate'] * 100}%\n设置：/usdt \n\n币数：({amount}÷{round(price1,3)}）- {config['mrate'] * 100}%={coins}USDT\n手续费：{config['mrate'] * 100}% = {round(amount * config['mrate'], 2)}RMB = {fee}USDT"
            await message.reply_text(text, quote=False)
        except ValueError as e:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


def keybords():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "上一挡",
                    callback_data="top"
                ),
                InlineKeyboardButton(
                    "下一档",
                    callback_data="down"
                ),
            ],
            [
                InlineKeyboardButton(
                    "+0.05",
                    callback_data="add_005"
                ),
                InlineKeyboardButton(
                    "-0.05",
                    callback_data="sub_005"
                ),
                InlineKeyboardButton(
                    "+0.01",
                    callback_data="add_001"
                ),
                InlineKeyboardButton(
                    "-0.01",
                    callback_data="sub_001"
                ),
            ],
            [
                InlineKeyboardButton(
                    "USDT功能设置方法",
                    callback_data="usdt_method"
                ),
                InlineKeyboardButton(
                    "关闭设置",
                    callback_data="close"
                ),
            ]
        ]
    )


@Client.on_message(filters.command(commands="usdt") & filters.group & op_cmd)
# @ratelimiter
async def usdt(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        config = await database.get_config(message.chat.id)
        gear = int(config['gear'])
        adjust = config['adjust']
        await message.reply_text(f"当前设置：欧易 {gear} 档 {adjust}", quote=False)
        await message.reply_text("点击设置", quote=False, reply_markup=keybords())
    else:
        await message.reply_text("您的授权已过期！", quote=False)


# 回调函数 top
@Client.on_callback_query(filters.regex(r"^top$"))
# @ratelimiter
async def top(_, callback_query: CallbackQuery):
    authorized = await database.check_permissions(callback_query.message.chat.id)
    if authorized:
        config = await database.get_config(callback_query.message.chat.id)
        gear = int(config['gear'])
        adjust = config['adjust']
        if gear == 1:
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
        else:
            gear -= 1
            await database.update_gear(callback_query.message.chat.id, gear=gear)
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
    else:
        await callback_query.answer("您的授权已过期！", show_alert=True)


@Client.on_callback_query(filters.regex(r"^down$"))
# @ratelimiter
async def down(_, callback_query: CallbackQuery):
    authorized = await database.check_permissions(callback_query.message.chat.id)
    if authorized:
        config = await database.get_config(callback_query.message.chat.id)
        gear = int(config['gear'])
        adjust = config['adjust']
        if gear == 10:
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
        else:
            gear += 1
            await database.update_gear(callback_query.message.chat.id, gear=gear)
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
    else:
        await callback_query.answer("您的授权已过期！", show_alert=True)


@Client.on_callback_query(filters.regex(r"^add_005$"))
# @ratelimiter
async def add_005(_, callback_query: CallbackQuery):
    authorized = await database.check_permissions(callback_query.message.chat.id)
    if authorized:
        config = await database.get_config(callback_query.message.chat.id)
        gear = int(config['gear'])
        adjust = float(config['adjust'])
        if adjust + 0.05 > 100:
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
        else:
            adjust += 0.05
            await database.update_adjust(callback_query.message.chat.id, adjust=adjust)
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
    else:
        await callback_query.answer("您的授权已过期！", show_alert=True)


@Client.on_callback_query(filters.regex(r"^add_001$"))
# @ratelimiter
async def add_001(_, callback_query: CallbackQuery):
    authorized = await database.check_permissions(callback_query.message.chat.id)
    if authorized:
        config = await database.get_config(callback_query.message.chat.id)
        gear = int(config['gear'])
        adjust = float(config['adjust'])
        if adjust + 0.01 > 100:
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
        else:
            adjust += 0.01
            await database.update_adjust(callback_query.message.chat.id, adjust=adjust)
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
    else:
        await callback_query.answer("您的授权已过期！", show_alert=True)


@Client.on_callback_query(filters.regex(r"^sub_005$"))
# @ratelimiter
async def sub_005(_, callback_query: CallbackQuery):
    authorized = await database.check_permissions(callback_query.message.chat.id)
    if authorized:
        config = await database.get_config(callback_query.message.chat.id)
        gear = int(config['gear'])
        adjust = float(config['adjust'])
        if adjust - 0.05 < 0:
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
        else:
            adjust -= 0.05
            await database.update_adjust(callback_query.message.chat.id, adjust=adjust)
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
    else:
        await callback_query.answer("您的授权已过期！", show_alert=True)


@Client.on_callback_query(filters.regex(r"^sub_001$"))
# @ratelimiter
async def sub_001(_, callback_query: CallbackQuery):
    authorized = await database.check_permissions(callback_query.message.chat.id)
    if authorized:
        config = await database.get_config(callback_query.message.chat.id)
        gear = int(config['gear'])
        adjust = float(config['adjust'])
        if adjust - 0.01 < 0:
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
        else:
            adjust -= 0.01
            await database.update_adjust(callback_query.message.chat.id, adjust=adjust)
            try:
                await callback_query.edit_message_text(f"**当前设置：欧易 {gear} 档 {round(adjust, 2)}**",
                                                       reply_markup=keybords())
            except:
                pass
    else:
        await callback_query.answer("您的授权已过期！", show_alert=True)


@Client.on_callback_query(filters.regex(r"^usdt_method$"))
# @ratelimiter
async def usdt_method(_, callback_query: CallbackQuery):
    authorized = await database.check_permissions(callback_query.message.chat.id)
    if authorized:
        text = """【USDT独立功能设置】
/usdt 币价调整
/set 5 设置查U价费率5%
/gd 6.6 固定汇率6.6
lk   列出火币实时价银行卡价格
lz   列出支付宝价格
lw   列出微信价格
k100   实时卡价计算100元换算usdt
z100   实时支价计算100元换算usdt
w100   实时微价计算100元换算usdt"""
        await bot.send_message(callback_query.message.chat.id, text=text)
    else:
        await callback_query.answer("您的授权已过期！", show_alert=True)


@Client.on_callback_query(filters.regex(r"^close$"))
# @ratelimiter
async def close(_, callback_query: CallbackQuery):
    # logger(__name__).info(f"Error ：{callback_query}")
    authorized = await database.check_permissions(callback_query.message.chat.id)
    if authorized:
        await callback_query.message.delete()
    else:
        await callback_query.answer("您的授权已过期！", show_alert=True)


@Client.on_message(filters.command(["set"]) & filters.group & op_cmd)
# @ratelimiter
async def independent_rate(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        try:
            rate = float(message.text.split(" ")[1].replace("%", "")) / 100
            await database.independent_rate(message.chat.id, rate=rate)
            await message.reply_text("设置成功！", quote=False)
        except:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)


@Client.on_message(filters.command(["gd"]) & filters.group & op_cmd)
# @ratelimiter
async def independent_usd_rate(_, message: Message):
    authorized = await database.check_permissions(message.chat.id)
    if authorized:
        try:
            rate = float(message.text.split(" ")[1])
            await database.independent_usd_rate(message.chat.id, rate=rate)
            await message.reply_text("设置成功！", quote=False)
        except:
            pass
    else:
        await message.reply_text("您的授权已过期！", quote=False)
