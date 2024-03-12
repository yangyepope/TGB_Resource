from TelegramBot import bot
from TelegramBot.loggings import logger

logger(__name__).info("client successfully initiated....")
if __name__ == "__main__":
    #
    bot.run()
