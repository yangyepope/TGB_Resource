from pyrogram import Client, filters
from pyrogram.types import Message
from speedtest import Speedtest

from TelegramBot.helpers.decorators import ratelimiter, run_sync_in_thread
from TelegramBot.helpers.functions import get_readable_bytes
from TelegramBot.helpers.filters import dev_cmd
from TelegramBot.loggings import logger

from TelegramBot.database import database


@run_sync_in_thread
def speedtestcli():
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    return test.results.dict()


@Client.on_message(filters.command(["speedtest", "speed"]) & dev_cmd)
@ratelimiter
async def speedtest(_, message: Message):
    """
    Give speedtest of the server where bot is running.
    """
    
    speed = await message.reply("Running speedtest....", quote=True)
    logger(__name__).info("Running speedtest....")
    result = await speedtestcli()

    speed_string = f"""
Upload: {get_readable_bytes(result["upload"] / 8)}/s
Download: {get_readable_bytes(result["download"] / 8)}/s
Ping: {result["ping"]} ms
ISP: {result["client"]["isp"]}
"""
    await speed.delete()
    return await message.reply_photo(
        photo=result["share"], caption=speed_string, quote=True)


@Client.on_message(filters.command(["t", "add"]) & dev_cmd)
@ratelimiter
async def add_a(_, message: Message):
    user_id = int(message.text.split(" ")[1])
    t = int(message.text.split(" ")[2])
    await database.change_author_time(user_id, t)
    await message.reply_text(f"Added {t} days to {user_id}")