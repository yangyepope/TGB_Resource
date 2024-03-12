import sys
import time
from asyncio import get_event_loop, new_event_loop, set_event_loop
# import uvloop
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client
from TelegramBot import config
from TelegramBot.database.mysqldb import check_mysql_uri
from TelegramBot.loggings import logger
from TelegramBot.helpers.task import warn, over, clear_past_due_bills, due_reminder, group_status_restart
from TelegramBot import global_var

# uvloop.install()
logger(__name__).info("Starting TelegramBot....")
BotStartTime = time.time()

if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    logger(__name__).critical("""
=============================================================
You MUST need to be on python 3.7 or above, shutting down the bot...
=============================================================
""")
    sys.exit(1)

logger(__name__).info("setting up event loop....")
try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

logger(__name__).info("initiating the client....")
logger(__name__).info("checking MySQL URI....")

loop.run_until_complete(check_mysql_uri())

plugins = dict(root="TelegramBot/plugins")
bot = Client(
    "TelegramBot",
    api_id=config.api_id,
    api_hash=config.api_hash,
    bot_token=config.bot_token,
    plugins=plugins,
    workers=8)

scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
scheduler.add_job(group_status_restart, 'cron', hour=4, minute=0, second=0, args=(bot,))
scheduler.add_job(clear_past_due_bills, 'cron', hour=4, minute=5, second=0)
scheduler.add_job(warn, 'cron', minute='0,3,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57', second='0', args=(bot,))
scheduler.add_job(over, "interval", seconds=1, args=(bot,))
scheduler.add_job(due_reminder, "interval", seconds=60*3, args=(bot,))
scheduler.start()
