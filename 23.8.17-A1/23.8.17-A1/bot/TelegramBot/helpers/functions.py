import aiohttp
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import Message
from TelegramBot.config import sudo_userid
from TelegramBot.database import database
import time


async def isAdmin(message: Message) -> bool:
    """
    Return True if the message is from owner or admin of the group or sudo of the bot.
    """
    if not message.from_user:
        return
    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return
    user_id = message.from_user.id
    if user_id in sudo_userid:
        return True
    check_status = await message.chat.get_member(user_id)
    return check_status.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]


def get_readable_time(seconds: int) -> str:
    """
    Return a human-readable time format
    """
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d "
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h "
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m "
    seconds = int(seconds)
    result += f"{seconds}s "
    return result


def get_readable_bytes(size: str) -> str:
    """
    Return a human readable file size from bytes.
    """
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}B"


def get_time_range():
    now = time.time()
    hour = int(time.strftime('%H', time.localtime(now)))
    if hour < 4:
        yesterday = time.localtime(now - 86400)
        yesterday_4am = time.mktime(time.struct_time((yesterday.tm_year, yesterday.tm_mon, yesterday.tm_mday, 4, 0, 0, 0, 0, -1)))
        today_4am = time.mktime(time.struct_time((time.localtime(now).tm_year, time.localtime(now).tm_mon, time.localtime(now).tm_mday, 4, 0, 0, 0, 0, -1)))
        return yesterday_4am, today_4am
    else:
        tomorrow = time.localtime(now + 86400)
        today_4am = time.mktime(time.struct_time((time.localtime(now).tm_year, time.localtime(now).tm_mon, time.localtime(now).tm_mday, 4, 0, 0, 0, 0, -1)))
        tomorrow_4am = time.mktime(time.struct_time((tomorrow.tm_year, tomorrow.tm_mon, tomorrow.tm_mday, 4, 0, 0, 0, 0, -1)))
        return today_4am, tomorrow_4am


async def aio_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def get_okex_price(paymentmethod):
    """
    wxPay: 微信  &urlId=10
    aliPay: 支付宝  urlId=2
    bank: 银行卡  urlId=9
    """
    urlId = {"wxPay": 10, "aliPay": 2, "bank": 9}
    t = int(time.time() * 1000)
    url = f"https://www.okx.com/v3/c2c/tradingOrders/books?t={t}&quoteCurrency=cny&baseCurrency=usdt&side=sell&paymentMethod={paymentmethod}&userType=all&receivingAds=false&urlId={urlId[paymentmethod]}"
    data = await aio_get(url)
    return data["data"]["sell"]


def markdown(message):
    m = message.text
    try:
        for i in message.entities:
            if str(i.type) == "MessageEntityType.SPOILER":
                SPOILER = message.text[i.offset:i.offset + i.length]
                m = m.replace(SPOILER, f"<spoiler>{SPOILER}</spoiler>")
            elif str(i.type) == "MessageEntityType.BOLD":
                BOLD = message.text[i.offset:i.offset + i.length]
                m = m.replace(BOLD, f"<b>{BOLD}</b>")
            elif str(i.type) == "MessageEntityType.PRE" or str(i.type) == "MessageEntityType.CODE":
                CODE = message.text[i.offset:i.offset + i.length]
                m = m.replace(CODE, f"<code>{CODE}</code>")
            elif str(i.type) == "MessageEntityType.ITALIC":
                ITALIC = message.text[i.offset:i.offset + i.length]
                m = m.replace(ITALIC, f"<i>{ITALIC}</i>")
            elif str(i.type) == "MessageEntityType.UNDERLINE":
                UNDERLINE = message.text[i.offset:i.offset + i.length]
                m = m.replace(UNDERLINE, f"<u>{UNDERLINE}</u>")
            elif str(i.type) == "MessageEntityType.STRIKETHROUGH":
                UNDERLINE = message.text[i.offset:i.offset + i.length]
                m = m.replace(UNDERLINE, f"<s>{UNDERLINE}</s>")
            elif str(i.type) == "MessageEntityType.TEXT_LINK":
                TEXT_LINK = message.text[i.offset:i.offset + i.length]
                m = m.replace(TEXT_LINK, f"<a href={i.url}>{TEXT_LINK}</a>")
    except:
        pass
    return m


def format_number(num):
    try:
        if num.is_integer():
            return str(int(num))
        else:
            return str(num)
    except AttributeError:
        return str(num)


async def overpressure(group_id, usd_rate, rate, warn_u, warn_rmb):
    start_time, end_time = get_time_range()
    add_data = await database.get_bill(group_id, "add", start_time, end_time)
    out_data = await database.get_out_bill(group_id, "out", start_time, end_time)
    ying_xiafa = format_number(round(sum([i['amount'] * (1 - rate) / (i['usd_rate'] if i['usd_rate'] != 0 else 1) for i in add_data]), 2))
    zong_xiafa = format_number(round(sum([i['usdt'] for i in out_data]), 2))
    wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))
    no_usdt = float(wei_xiafa)
    no_rmb = float(wei_xiafa) * (usd_rate if usd_rate != 0 else 1)
    if usd_rate > 0:
        if no_usdt >= warn_u * 0.7 and warn_u != 0:
            return True
    else:
        if no_rmb >= warn_rmb * 0.7 and warn_rmb != 0:
            return True

