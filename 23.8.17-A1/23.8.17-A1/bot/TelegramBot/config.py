import json
import os
from dotenv import load_dotenv
from TelegramBot.loggings import logger

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
config_path = os.path.join(parent_dir, 'config.env')
print(config_path)

load_dotenv('config.env')

api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")
bill_url = os.getenv("bill_url")

owner_userid = json.loads(os.getenv("owner_userid"))
sudo_userid = owner_userid
try:
    sudo_userid += json.loads(os.getenv("sudo_userid"))
except json.decoder.JSONDecodeError as e:
    pass
    # logger(__name__).info(f"sudo_userid is not filled")

sudo_userid = list(set(sudo_userid))

mysql_host = os.getenv("host")
mysql_user = os.getenv("user")
mysql_password = os.getenv("password")
mysql_database = os.getenv("database")
mysql_port = int(os.getenv("port"))



