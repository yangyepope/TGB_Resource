import logging
import os
from logging.handlers import RotatingFileHandler

# removing old logs file if they exist.
try:
    os.remove("logs.txt")
except:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", mode="w+", maxBytes=5000000, backupCount=10),
        logging.StreamHandler()])

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiomysql").setLevel(logging.ERROR)
logging.getLogger("numexpr").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)


def logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
