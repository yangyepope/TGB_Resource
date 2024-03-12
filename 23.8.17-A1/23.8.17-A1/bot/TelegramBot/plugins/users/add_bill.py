import time

from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.loggings import logger
import datetime
from TelegramBot.helpers.start_constants import *
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from TelegramBot.helpers.filters import *
from TelegramBot.helpers.functions import get_time_range, overpressure
from TelegramBot import config as cf
from TelegramBot import global_var


# 过滤 + 消息
@Client.on_message(
    (filters.regex(r"^\+\d+") | filters.regex(r"^入款") | filters.regex(r"^0$")) & filters.group & op_cmd)  # ^\+\d+$
# @ratelimiter
async def add_bill(_, message: Message):
    start_time1 = time.time()
    authorized = await database.check_permissions(message.chat.id)
    # logger(__name__).info(f"{message.text}")
    # logger(__name__).info(f"授权状况为：{authorized}")
    if authorized:
        config = await database.get_config(message.chat.id)
        if config['state']:
            # operator = await database.is_operator(message.chat.id, message.from_user.id)
            # if operator:
            if message.text == "入款":
                return
            amount_str = message.text.replace("+", "").upper().replace("入款", "")
            if amount_str.find("/") != -1 and float(config['usd_rate']) == 0:
                await message.reply_text("当前未设置美元汇率\n请使用命令：<code>设置美元汇率</code>x.xx\n再以U形式入款")
                return
            if amount_str.find("U") != -1 and float(config['usd_rate']) == 0:
                await message.reply_text("当前未设置美元汇率\n请使用命令：<code>设置美元汇率</code>x.xx\n再以U形式入款")
                return




            if amount_str.find("/") != -1 and float(config['usd_rate']) > 0: # 判断设置了U汇率没有
                amount = amount_str.split("/")[0]
                usd_rate = amount_str.split("/")[1]
            elif amount_str.find("U") != -1 and float(config['usd_rate']) > 0: # 判断设置了U汇率没有
                amount = float(amount_str.replace("U", "")) * float(config['usd_rate'])
                usd_rate = float(config['usd_rate'])
            else:
                amount = amount_str
                usd_rate = float(config['usd_rate'])

            group_id = message.chat.id
            timestamp = int(message.date.timestamp())
            try:
                operator_id = message.from_user.username
            except KeyError as e:
                operator_id = message.from_user.first_name

            if not operator_id:
                operator_id = message.from_user.first_name
            print(operator_id)
            #print(message.from_user)
            rate = config['rate']
            try:
                respondent = message.reply_to_message.from_user.username
            except:
                try:
                    # respondent = message.reply_to_message.from_user.first_name
                    respondent = message.reply_to_message.from_user.first_name
                except:
                    respondent = ""
            try:
                if not respondent:
                    respondent = message.reply_to_message.from_user.first_name
            except:
                respondent = ""

            # print(group_id, amount, timestamp, operator, respondent)
            try:
                await database.add_bill(group_id, float(amount), timestamp, rate, float(usd_rate), respondent,
                                        operator_id, "add")
            except ValueError as e:
                pass

            display = config['display']
            u_display = config['u_display']
            ad = config['ad']
            ad_display = config['ad_display']
            start_time, end_time = get_time_range()

            data = await get_display(group_id, display, rate, usd_rate, u_display, ad, ad_display, start_time, end_time)
            url_jump = data[1]
            text = data[0]
            if ad_display:  # 展示广告
                if ad != "0":  # 已经设置了广告内容
                    ad_name = ad.split("+")[0]
                    ad_url = ad.split("+")[1]
                    try:
                        await message.reply_text(text=text, quote=False, reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("点击跳转完整账单", url=f"{cf.bill_url}/?group={-message.chat.id}")],
                             [InlineKeyboardButton(ad_name, url=ad_url)]]))
                    except:
                        if url_jump:
                            await message.reply_text(text=text, quote=False, reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("点击跳转完整账单",
                                                       url=f"{cf.bill_url}/?group={-message.chat.id}")]]))
                        else:
                            await message.reply_text(text=text, quote=False)
                        await message.reply_text(text=f"广告链接参数错误", quote=False)

                else:  # 没有设置广告内容
                    if url_jump:
                        await message.reply_text(text=text, quote=False, reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("点击跳转完整账单",
                                                   url=f"{cf.bill_url}/?group={-message.chat.id}")]]))
                    else:
                        await message.reply_text(text=text, quote=False)
            else:  # 不展示广告

                if url_jump:
                    await message.reply_text(text=text, quote=False, reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("点击跳转完整账单", url=f"{cf.bill_url}/?group={-message.chat.id}")]]))
                else:
                    await message.reply_text(text=text, quote=False)

                    # 超压提醒
            flag = config['overs']
            over = await overpressure(message.chat.id, config['usd_rate'], config['rate'], config['warn_u'],
                                      config['warn_rmb'])
            if over and not flag: # 第一次推送的话这里为False
                await message.reply_photo(photo='https://i.328888.xyz/2023/05/12/iqhTFy.jpeg', quote=False)
                # global_var.set_value('flag', 1)
                await database.update_over(message.chat.id, True)

        else:
            await message.reply_text("请先发送 开始 进行记账！", quote=False)

    else:
        await message.reply_text("您的授权已过期！", quote=False)

    end_time1 = time.time()
    logger(__name__).info(f"add_bill: {end_time1 - start_time1}")
