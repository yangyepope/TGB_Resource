import time
from TelegramBot.database.mysqldb import mysql as db
from TelegramBot.loggings import logger


async def save_user(user):
    """
    Save the new user id in the database if it is not already there.
    """
    try:
        name = (user.first_name or " ") + (user.last_name or "")
        username = user.username or " "
        user_id = user.id
        authorized = 0
        await db.init_pool()
        sql = f"insert into users (user_id, name,username,authorized,free,shouquan,shouquan_name,liangtian,daoqi)values({user_id}, '{name}','{username}', {authorized},TRUE,'{str(user_id)},','admin,',TRUE,TRUE)"
        await db.insert(sql)
    except Exception as e:
        logger(__name__).info(f"Error in saving user：{e}")


async def save_chat(grou_id, owner):
    """
    Save the new chat id in the database if it is not already there.
    """
    try:
        welcome = "用户名称：{name}\n用户名：{username}\n用户ID：{id}\n欢迎加入此群！"
        await db.init_pool()
        sql = f"insert into `groups` (group_id,owner,operator,rate,usd_rate,state,display,operator_name,u_display,address,ad_display,ad,rule,welcome,authorizer,authorizer_name,gear,adjust,mrate,kefu,warn_rmb,warn_u,overs,uuu)values({grou_id}, {owner}, '{owner},', -1,0,FALSE,1,'T,',TRUE,'0',TRUE,'0','0','{welcome}','{owner}','A,',1,0,0,'0',0,0,FALSE,0)"
        await db.insert(sql)
    except Exception as e:
        logger(__name__).info(f"Error in saving chat：{e}")


async def get_group_admin(group_id):
    try:
        await db.init_pool()
        sql = f"select owner from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        owner_id = data["owner"]
        return owner_id
    except Exception as e:
        logger(__name__).info(f"Error in getting group admin：{e}")


async def get_remind():
    try:
        await db.init_pool()
        sql = f"select user_id,authorized,liangtian,daoqi from users"
        data = await db.fetch_all(sql)
        return data
    except Exception as e:
        logger(__name__).info(f"Error in get_remind：{e}")


async def get_address(group_id):
    try:
        # print(group_id)
        await db.init_pool()
        sql = f"select address from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        owner_id = data["address"]
        return owner_id
    except Exception as e:
        logger(__name__).info(f"Error in get_address：{e}")


async def get_all_users():
    try:
        await db.init_pool()
        sql = f"select * from `users` "
        data = await db.fetch_all(sql)
        return data
    except Exception as e:
        logger(__name__).info(f"Error in get_all_users：{e}")


async def get_all_group():
    try:
        await db.init_pool()
        sql = f"select * from `groups` "
        data = await db.fetch_all(sql)
        return data
    except Exception as e:
        logger(__name__).info(f"Error in get_all_group：{e}")


async def get_rule(group_id):
    try:
        await db.init_pool()
        sql = f"select rule from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        owner_id = data["rule"]
        return owner_id
    except Exception as e:
        logger(__name__).info(f"Error in get_rule：{e}")


async def get_kefu(group_id):
    try:
        await db.init_pool()
        sql = f"select kefu from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        owner_id = data["kefu"]
        return owner_id
    except Exception as e:
        logger(__name__).info(f"Error in get_kefu：{e}")


async def get_expire_date(user_id):
    try:
        await db.init_pool()
        sql = f"select authorized from `users` where user_id = {user_id}"
        data = await db.fetch_one(sql)
        owner_id = data["authorized"]
        return owner_id
    except Exception as e:
        logger(__name__).info(f"Error in get_expire_date：{e}")


async def get_welcome(group_id):
    try:
        await db.init_pool()
        sql = f"select welcome from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        owner_id = data["welcome"]
        return owner_id
    except Exception as e:
        logger(__name__).info(f"Error in get_welcome：{e}")


async def check_permissions(group_id) -> bool:
    """
    Check if the user has permission to use the bot.
    """
    try:
        owner_id = await get_group_admin(group_id)
        await db.init_pool()
        sql = f"select authorized from users where user_id = {owner_id}"
        data = await db.fetch_one(sql)
        authorized = data["authorized"]
        if authorized >= int(time.time()):
            return True
        else:
            return False
    except Exception as e:
        logger(__name__).info(f"Error in checking permissions：{e}")
        return False


# 设置费率
async def set_rate(group_id, rate):
    try:
        await db.init_pool()
        sql = f"update `groups` set rate = {float(rate)} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_rate：{e}")


async def independent_rate(group_id, rate):
    try:
        await db.init_pool()
        sql = f"update `groups` set mrate = {float(rate)} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in independent_rate：{e}")


async def independent_usd_rate(group_id, rate):
    try:
        await db.init_pool()
        sql = f"update `groups` set uuu = {float(rate)} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in independent_usd_rate：{e}")


async def set_usd_rate(group_id, rate):
    try:
        await db.init_pool()
        sql = f"update `groups` set usd_rate = {float(rate)} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_usd_rate：{e}")


async def update_gear(group_id, gear):
    try:
        await db.init_pool()
        sql = f"update `groups` set gear = {gear} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in update_gear：{e}")


async def update_adjust(group_id, adjust):
    try:
        await db.init_pool()
        sql = f"update `groups` set adjust = {adjust} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in update_adjust：{e}")


async def set_address(group_id, address):
    try:
        await db.init_pool()
        sql = f"update `groups` set address = '{address}' where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_address：{e}")


async def set_rule(group_id, rule):
    try:
        await db.init_pool()
        sql = f"update `groups` set rule = '{rule}' where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_rule：{e}")


async def set_kefu(group_id, kefu):
    try:
        await db.init_pool()
        sql = f"update `groups` set kefu = '{kefu}' where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_kefu：{e}")


async def set_welcome(group_id, welcome):
    try:
        await db.init_pool()
        sql = f"update `groups` set welcome = '{welcome}' where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_welcome：{e}")


async def set_ad(group_id, ad):
    try:
        await db.init_pool()
        sql = f"update `groups` set ad = '{ad}' where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_ad：{e}")


async def del_ad(group_id):
    try:
        await db.init_pool()
        sql = f"update `groups` set ad = '0' where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in del_ad：{e}")


async def get_config(group_id):
    try:
        await db.init_pool()
        sql = f"select * from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        return data
    except Exception as e:
        logger(__name__).info(f"Error in get_config：{e}")


async def set_status(group_id, state):
    try:
        await db.init_pool()
        sql = f"update `groups` set state = {state} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_status：{e}")


async def set_daoqi(user_id, state, q):
    try:
        await db.init_pool()
        sql = f"update `users` set {state} = {q} where user_id = {user_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_daoqi：{e}")


async def set_u_display(group_id, state):
    try:
        await db.init_pool()
        sql = f"update `groups` set u_display = {state} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_u_display：{e}")


async def set_warn(group_id, types, amount):
    try:
        await db.init_pool()
        sql = f"update `groups` set {types} = {amount} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_warn_{types}：{e}")


async def set_bill_display1(group_id, state):
    try:
        await db.init_pool()
        sql = f"update `groups` set display = {state} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_bill_display1：{e}")


async def set_ad_display(group_id, state):
    try:
        await db.init_pool()
        sql = f"update `groups` set ad_display = {state} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in set_u_display：{e}")


async def update_over(group_id, state):
    try:
        await db.init_pool()
        sql = f"update `groups` set overs = {state} where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in update_over：{e}")


async def add_bill(group_id, amount, timestamp, rate, usd_rate, respondent, operator, types):
    try:
        await db.init_pool()
        sql = f"insert into `data` (group_id, amount, timestamp, rate, usd_rate, respondent, operator, type)values({group_id}, {amount}, {timestamp}, {rate}, {usd_rate}, '{respondent}', '{operator}', '{types}')"
        await db.insert(sql)
    except Exception as e:
        logger(__name__).info(f"Error in add_bill：{e}")


async def out_bill(group_id, text, rmb, usdt, timestamp, respondent, operator, types):
    try:
        await db.init_pool()
        sql = f"insert into `data2` (group_id, text, rmb, usdt, timestamp, respondent, operator, type)values({group_id}, '{text}', {rmb}, {usdt}, {timestamp}, '{respondent}', '{operator}', '{types}')"
        await db.insert(sql)
    except Exception as e:
        logger(__name__).info(f"Error in out_bill：{e}")


async def get_bill(group_id, types, start_time, end_time):
    try:
        await db.init_pool()
        sql = f"select * from `data` where group_id = {group_id} and type = '{types}' AND timestamp > {start_time} AND timestamp < {end_time} AND amount != 0"
        data = await db.fetch_all(sql)
        if data:
            return data
        else:
            return []
    except Exception as e:
        logger(__name__).info(f"Error in get_bill：{e}")
        return []


async def get_out_bill(group_id, types, start_time, end_time):
    try:
        await db.init_pool()
        sql = f"select * from `data2` where group_id = {group_id} and type = '{types}' AND timestamp > {start_time} AND timestamp < {end_time} AND rmb != 0.0"
        data = await db.fetch_all(sql)
        if data:
            return data
        else:
            return []
    except Exception as e:
        logger(__name__).info(f"Error in get_out_bill：{e}")
        return []


async def delete_chat(group_id):
    try:
        await db.init_pool()
        sql = f"delete from `groups` where group_id = {group_id}"
        await db.delete(sql)
    except Exception as e:
        logger(__name__).info(f"Error in delete_chat：{e}")


async def is_operator(group_id, user_id):
    try:
        await db.init_pool()
        sql = f"select operator from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        operator = data["operator"]
        operator_list = operator.split(",")
        for i in operator_list:
            if str(i) == str(user_id):
                return True
            else:
                return False
    except Exception as e:
        logger(__name__).info(f"Error in is_operator：{e}")
        return False


async def get_operator(group_id):
    try:
        await db.init_pool()
        sql = f"select operator from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        operator = str(data["operator"])
        operator_list = operator.split(",")
        return operator_list
    except Exception as e:
        logger(__name__).info(f"Error in get_operator：{e}")
        return []


async def get_authorizer(group_id):
    try:
        await db.init_pool()
        sql = f"select owner from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        boss = int(data["owner"])
        sql2 = f"select shouquan from `users` where user_id = {boss}"
        sq = await db.fetch_one(sql2)
        sq_list = sq["shouquan"].split(",")
        return sq_list
    except Exception as e:
        logger(__name__).info(f"Error in get_authorizer：{e}")
        return []


async def get_vip(group_id):
    try:
        await db.init_pool()
        sql = f"select owner from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        operator = str(data["owner"])
        operator_list = operator.split(",")
        return operator_list
    except Exception as e:
        logger(__name__).info(f"Error in get_authorizer：{e}")
        return []


async def is_owner(group_id, user_id):
    try:
        await db.init_pool()
        sql = f"select owner from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        owner = data["owner"]
        if str(owner) == str(user_id):
            return True
        else:
            return False
    except Exception as e:
        logger(__name__).info(f"Error in is_owner：{e}")
        return False


async def del_add_bill(group_id):
    try:
        await db.init_pool()
        sql = f"delete from `data` where group_id = {group_id}"
        await db.delete(sql)
    except Exception as e:
        logger(__name__).info(f"Error in del_add_bill：{e}")


async def del_out_bill(group_id):
    try:
        await db.init_pool()
        sql = f"delete from `data2` where group_id = {group_id}"
        await db.delete(sql)
    except Exception as e:
        logger(__name__).info(f"Error in del_out_bill：{e}")


async def del_bill_by_timestamp(group_id, start_time, end_time):
    try:
        await db.init_pool()
        sql = f"DELETE FROM `data` WHERE group_id = {group_id} AND timestamp > {start_time} AND timestamp < {end_time};"
        await db.delete(sql)
        sql2 = f"DELETE FROM `data2` WHERE group_id = {group_id} AND timestamp > {start_time} AND timestamp < {end_time};"
        await db.delete(sql2)
    except Exception as e:
        logger(__name__).info(f"Error in del_bill_by_timestamp：{e}")


async def clear_past_bills(timestamp):
    try:
        await db.init_pool()
        sql = f"DELETE FROM `data` WHERE timestamp < {timestamp};"
        await db.delete(sql)
        sql2 = f"DELETE FROM `data2` WHERE timestamp < {timestamp};"
        await db.delete(sql2)
    except Exception as e:
        logger(__name__).info(f"Error in clear_past_bills：{e}")


async def save_operator(group_id, operator_id):
    try:
        await db.init_pool()
        sql = f"select operator from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        operator = str(data["operator"])
        operator_list = operator.split(",")
        if str(operator_id) not in operator_list:
            new_operator = operator + str(operator_id) + ","
            sql = f"update `groups` set operator = '{new_operator}' where group_id = {group_id}"
            await db.update(sql)

    except Exception as e:
        logger(__name__).info(f"Error in save_operator：{e}")


async def save_authorizer(group_id, authorizer_id):
    try:
        admin_id = await get_group_admin(group_id)
        await db.init_pool()
        sql = f"select shouquan from `users` where user_id = {admin_id}"
        data = await db.fetch_one(sql)
        operator = str(data["shouquan"])
        operator_list = operator.split(",")
        logger(__name__).info(f"现在一共是{len(operator_list)}个权限人")
        if str(authorizer_id) not in operator_list and len(operator_list) <= 6:
            new_operator = operator + str(authorizer_id) + ","
            sql = f"update `users` set shouquan = '{new_operator}' where user_id = {admin_id}"
            await db.update(sql)
            logger(__name__).info(f"授权成功")
            return True
        else:
            logger(__name__).info(f"没有！！！授权成功")
            return False

    except Exception as e:
        logger(__name__).info(f"Error in save_authorizer：{e}")


async def get_authorizer_num(group_id):
    try:
        admin_id = await get_group_admin(group_id)
        await db.init_pool()
        sql = f"select shouquan from `users` where user_id = {admin_id}"
        data = await db.fetch_one(sql)
        operator = str(data["shouquan"])
        operator_list = operator.split(",")
        return len(operator_list)


    except Exception as e:
        logger(__name__).info(f"Error in save_authorizer：{e}")


async def del_operator(group_id, operator_id):
    try:
        await db.init_pool()
        sql = f"select operator from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        operator = str(data["operator"])
        operator_list = operator.split(",")
        for i in operator_list:
            if str(i) == str(operator_id):
                operator_list.remove(i)
        new_operator = ",".join(operator_list)
        sql = f"update `groups` set operator = '{new_operator}' where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in del_operator：{e}")


async def del_authorizer(group_id, authorizer_id):
    try:
        admin_id = await get_group_admin(group_id)
        await db.init_pool()
        sql = f"select shouquan from `users` where user_id = {admin_id}"
        data = await db.fetch_one(sql)
        operator = str(data["shouquan"])
        operator_list = operator.split(",")
        for i in operator_list:
            if str(i) == str(authorizer_id):
                operator_list.remove(i)
        new_operator = ",".join(operator_list)
        sql = f"update `users` set shouquan = '{new_operator}' where user_id = {admin_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in del_authorizer：{e}")


async def save_operator_name(group_id, operator_name):
    try:
        await db.init_pool()
        sql = f"select operator_name from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        operator = str(data["operator_name"])
        operator_list = operator.split(",")
        if (str(operator_name) not in operator_list) and ('@' + str(operator_name) not in operator_list):
            new_operator = operator + str(operator_name) + ","
            sql = f"update `groups` set operator_name = '{new_operator}' where group_id = {group_id}"
            await db.update(sql)

    except Exception as e:
        logger(__name__).info(f"Error in save_operator_name：{e}")


async def save_authorizer_name(group_id, authorizer_name):
    try:
        admin_id = await get_group_admin(group_id)
        await db.init_pool()
        sql = f"select shouquan_name from `users` where user_id = {admin_id}"
        data = await db.fetch_one(sql)
        operator = str(data["shouquan_name"])
        operator_list = operator.split(",")
        if (str(authorizer_name) not in operator_list) and ('@' + str(authorizer_name) not in operator_list) and len(operator_list) <= 6:
            new_operator = operator + str(authorizer_name) + ","
            sql = f"update `users` set shouquan_name = '{new_operator}' where user_id = {admin_id}"
            await db.update(sql)

    except Exception as e:
        logger(__name__).info(f"Error in save_operator_name：{e}")


async def del_operator_name(group_id, operator_name):
    try:
        sql = f"select operator_name from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        operator = str(data["operator_name"])
        operator_list = operator.split(",")
        for i in operator_list:
            if str(i) == str(operator_name):
                operator_list.remove(i)
        new_operator = ",".join(operator_list)
        sql = f"update `groups` set operator_name = '{new_operator}' where group_id = {group_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in del_operator_name：{e}")


async def del_authorizer_name(group_id, authorizer_name):
    try:
        admin_id = await get_group_admin(group_id)
        sql = f"select shouquan_name from `users` where user_id = {admin_id}"
        data = await db.fetch_one(sql)
        operator = str(data["shouquan_name"])
        operator_list = operator.split(",")
        for i in operator_list:
            if str(i) == str(authorizer_name):
                operator_list.remove(i)
        new_operator = ",".join(operator_list)
        sql = f"update `users` set shouquan_name = '{new_operator}' where user_id = {admin_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in del_authorizer_name：{e}")


async def get_operator_name(group_id):
    try:
        await db.init_pool()
        sql = f"select operator_name from `groups` where group_id = {group_id}"
        data = await db.fetch_one(sql)
        operator = str(data["operator_name"])
        operator_list = operator.split(",")
        return operator_list[1:]
    except Exception as e:
        logger(__name__).info(f"Error in get_operator_name：{e}")
        return []


async def get_authorizer_name(group_id):
    try:
        admin_id = await get_group_admin(group_id)
        await db.init_pool()
        sql = f"select shouquan_name from `users` where user_id = {admin_id}"
        data = await db.fetch_one(sql)
        operator = str(data["shouquan_name"])
        operator_list = operator.split(",")
        return operator_list[1:]
    except Exception as e:
        logger(__name__).info(f"Error in get_authorizer_name：{e}")
        return []


async def test(user_id):
    await db.init_pool()
    sql = f"select free from `users` where user_id = {user_id}"
    free = await db.fetch_one(sql)
    free = free["free"]  # false
    if free:
        timestamp = int(time.time() + 6 * 3600)
        sql = f"update users set authorized = {timestamp} where user_id = {user_id}"
        await db.update(sql)
        sql2 = f"update users set free = FALSE where user_id = {user_id}"
        await db.update(sql2)
        return timestamp
    else:
        return


async def get_warn():
    try:
        await db.init_pool()
        sql = f"select group_id,warn_u,warn_rmb,rate,usd_rate from `groups` where warn_u > 0 OR warn_rmb > 0"
        data = await db.fetch_all(sql)
        if data:
            return data
        else:
            return []
    except Exception as e:
        logger(__name__).info(f"Error in get_bill：{e}")
        return []


async def change_author_time(user_id, d):
    try:
        # sql1 = f"select authorized from `users` where user_id = {user_id}"
        # free = await db.fetch_one(sql1)
        # old = free["authorized"]
        t = d * 86400 + int(time.time())
        sql = f"update users set authorized = {t} where user_id = {user_id}"
        await db.update(sql)
    except Exception as e:
        logger(__name__).info(f"Error in change_author_time：{e}")
