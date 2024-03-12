import datetime
import time

from TelegramBot.database import database
from TelegramBot.helpers.functions import get_time_range
from TelegramBot.helpers.start_constants import format_number
from TelegramBot.loggings import logger


async def warn(bot):
    data = await database.get_warn()
    # logger(__name__).info(f"{data}")
    start_time, end_time = get_time_range()
    for z in data:
        if z['warn_u'] > 0 or z['warn_rmb'] > 0:
            add_data = await database.get_bill(z['group_id'], "add", start_time, end_time)
            out_data = await database.get_out_bill(z['group_id'], "out", start_time, end_time)
            ying_xiafa = format_number(round(sum([i['amount'] * (1 - z['rate']) / (i['usd_rate'] if i['usd_rate'] != 0 else 1) for i in add_data]), 2))
            zong_xiafa = format_number(round(sum([i['usdt'] for i in out_data]), 2))
            wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))  # USD
            no_usdt = float(wei_xiafa)
            no_rmb = float(wei_xiafa) * (z['usd_rate'] if z['usd_rate'] != 0 else 1)
            if z['usd_rate'] > 0:
                if no_usdt >= z['warn_u'] * 0.7 and z['warn_u'] != 0:
                    await bot.send_photo(z['group_id'], photo='https://i.328888.xyz/2023/05/12/iqhTFy.jpeg')
            else:
                if no_rmb >= z['warn_rmb'] * 0.7 and z['warn_rmb'] != 0:
                    await bot.send_photo(z['group_id'], photo='https://i.328888.xyz/2023/05/12/iqhTFy.jpeg')


async def over(bot):
    data = await database.get_warn()
    start_time, end_time = get_time_range()
    for z in data:
        if z['warn_u'] > 0 or z['warn_rmb'] > 0:
            add_data = await database.get_bill(z['group_id'], "add", start_time, end_time)
            out_data = await database.get_out_bill(z['group_id'], "out", start_time, end_time)
            ying_xiafa = format_number(round(sum([i['amount'] * (1 - z['rate']) / (i['usd_rate'] if i['usd_rate'] != 0 else 1) for i in add_data]), 2))
            zong_xiafa = format_number(round(sum([i['usdt'] for i in out_data]), 2))
            wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))  # USD
            no_usdt = float(wei_xiafa)
            no_rmb = float(wei_xiafa) * (z['usd_rate'] if z['usd_rate'] != 0 else 1)
            if z['usd_rate'] > 0:
                if no_usdt >= z['warn_u'] * 0.7 and z['warn_u'] != 0:
                    pass
                else:
                    await database.update_over(z['group_id'], False)
            else:
                if no_rmb >= z['warn_rmb'] * 0.7 and z['warn_rmb'] != 0:
                    pass
                else:
                    await database.update_over(z['group_id'], False)


async def clear_past_due_bills():
    now = datetime.datetime.now()
    month_ago = now - datetime.timedelta(days=30)
    timestamp = int(month_ago.timestamp())  # 30 days ago
    await database.clear_past_bills(timestamp)


async def due_reminder(bot):
    data = await database.get_remind()
    for i in data:
        userid = i['user_id']
        authorized = i['authorized']
        liangtian = i['liangtian']
        daoqi = i['daoqi']
        print(authorized, liangtian, daoqi)
        timestamp = int(time.time())
        if authorized - timestamp >= 86400 * 2:
            await database.set_daoqi(userid, 'liangtian', False)
            await database.set_daoqi(userid, 'daoqi', False)

        if 86400 * 2 >= authorized - timestamp > 0 and liangtian == 1:
            await bot.send_message(userid, "您的授权还有两天到期，请及时续费")
            await database.set_daoqi(userid, 'liangtian', False)

        if authorized - timestamp <= 0 and daoqi == 1:
            await bot.send_message(userid, "您的授权已到期，请及时续费")
            await database.set_daoqi(userid, 'daoqi', False)


async def group_status_restart(bot):
    data = await database.get_all_group()
    for i in data:
        await database.set_status(i['group_id'], False)
        # await bot.send_message(i['group_id'], "今日记账已经结束，请重启发送 开始 进行记账！")
