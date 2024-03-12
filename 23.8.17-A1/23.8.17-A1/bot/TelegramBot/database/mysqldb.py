import time
from TelegramBot.loggings import logger
from sys import exit as exiter
import aiomysql.cursors
import asyncio
import aiomysql
from TelegramBot import config


class AioMysqlClient:
    def __init__(self, host, port, username, password, db_name, **kwargs):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.kwargs = kwargs  # 其他参数
        self.conn_pool = None  # 连接池
        self.is_connected = False  # 是否处于连接状态
        self.lock = asyncio.Lock()  # 异步锁

    async def init_pool(self):
        try:
            self.conn_pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                db=self.db_name,
                **self.kwargs
            )
            self.is_connected = True
        except:
            # print(traceback.format_exc())
            self.is_connected = False

        return self

    async def insert(self, sql, args=None):
        conn = await self.conn_pool.acquire()
        cur = await self.execute(conn, sql, args)
        await conn.commit()
        conn.close()  # 不是关闭连接，而是还到连接池中
        return cur

    async def fetch_one(self, sql, args=None):
        conn = await self.conn_pool.acquire()
        cur = await self.execute(conn, sql, args)
        if cur.rowcount == 0:
            return None
        return await cur.fetchone()

    async def fetch_all(self, sql, args=None):
        conn = await self.conn_pool.acquire()
        cur = await self.execute(conn, sql, args)
        if cur.rowcount == 0:
            return None

        return await cur.fetchall()

    async def execute(self, conn, sql, args=None):
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql, args)  # 执行sql
            return cur

    # 更新数据
    async def update(self, sql, args=None):
        conn = await self.conn_pool.acquire()
        cur = await self.execute(conn, sql, args)
        await conn.commit()
        conn.close()

    # 删除数据
    async def delete(self, sql, args=None):
        conn = await self.conn_pool.acquire()
        cur = await self.execute(conn, sql, args)
        await conn.commit()
        conn.close()


async def test_insert():
    start = time.time()
    mysql_client = AioMysqlClient("127.0.0.1", 3306, 'root', '123456', 'bill')
    await mysql_client.init_pool()
    sql = "insert into users(user_id, name,username,authorized)values(5732433547, 'SychO','sychoc', 0)"
    print("执行sql")
    cur = await mysql_client.insert(sql)
    print(cur.lastrowid)
    end_time = time.time()
    print(end_time - start)


async def test_select():
    start = time.time()
    mysql_client = AioMysqlClient("127.0.0.1", 3306, 'root', '123456', 'bill')
    await mysql_client.init_pool()
    sql = "select * from users"
    # data = await mysql_client.fetch_one(sql)
    # print(data)

    datas = await mysql_client.fetch_all(sql)
    print(datas)
    end_time = time.time()
    print(end_time - start)


async def check_mysql_uri() -> None:
    try:
        conn = await aiomysql.connect(user=config.mysql_user,
                                      password=config.mysql_password,
                                      host=config.mysql_host,
                                      db=config.mysql_database,
                                      port=config.mysql_port)
        await conn.ping(reconnect=True)
        logger(__name__).info("MySQL connection succeeded!")
    except aiomysql.Error as e:
        logger(__name__).error("MySQL URL error, please check the configuration in config.env")
        exiter(1)


mysql = AioMysqlClient(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_password,
                       config.mysql_database)


async def create_users():
    try:
        mysql_client = mysql
        await mysql_client.init_pool()
        sql = f"CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, name TEXT, username TEXT, authorized BIGINT)"
        await mysql_client.insert(sql)
    except Exception as e:
        logger(__name__).info(f"Error in creating table: {e}")


if __name__ == "__main__":
    asyncio.run(test_insert())
    # pass
