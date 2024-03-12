import pymysql
import json
class user:
    db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
    cursor = db.cursor() 
    def invite(table,tgid,invite):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
        cursor = db.cursor() 
        sql = "UPDATE {} SET invite = invite + {} WHERE telegramid = {}".format(table,invite,tgid)
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    def add(table,tgid):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
        cursor = db.cursor() 
        sql = "INSERT INTO `{}`(telegramid,score, invite, usertype)VALUES ({}, 0.0,  0,  1)".format(table,tgid)

        cursor.execute(sql)
        db.commit()
           #db.rollback()
    def score(table,tgid,score):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
        cursor = db.cursor() 
        sql = "UPDATE {} SET score = score + {} WHERE telegramid = {}".format(table,float(score),tgid)
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    def get(table,tgid):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
        cursor = db.cursor() 
        sql="SELECT * FROM {} WHERE telegramid = {}".format(table,tgid)
        atype=["尊贵的VIP","普通用户"]
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
              tgid = row[0]
              score = row[1]
              invite = row[2]
              usertype = row[3]
            msg={
                "id":tgid,
                "score":score,
                "invite":invite,
                "usertype":atype[int(usertype)]
            }
            return msg
        except:
            print('fail')
            db.rollback()
    def all(table):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
        cursor = db.cursor() 
        sql = " SELECT COUNT(*) FROM {} limit 1;".format(table)
        try:
            cursor.execute(sql)
            db.commit()
            all_user=cursor.fetchall()
        except:
           db.rollback()
        db.commit()
        return all_user
    def issign(table,tgid):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
        cursor = db.cursor() 
        sql = "SELECT telegramid FROM {} WHERE telegramid={} LIMIT 1".format(table,tgid)
        try:
            cursor.execute(sql)
            db.commit()
            is_user_sign_in=cursor.fetchall()
            print(is_user_sign_in)
        except:
            db.rollback()
            return False

        if len(is_user_sign_in) >0:
            if tgid == is_user_sign_in[0][0]:
                return True
            else:
                return False
        else:
            return False
    def set(table,user,id):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
        cursor = db.cursor() 
        sql = "UPDATE {} SET usertype = {} WHERE telegramid = {}".format(table,user,id)
        try:
            cursor.execute(sql)
            db.commit()
            return True
        except:
            print("失败")
            db.rollback()
    def all_list(table):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='du')
        cursor = db.cursor() 
        sql = "select distinct telegramid from {};".format(table)
        cursor.execute(sql)
        db.commit()
        userlist=cursor.fetchall()
        userlist=list(userlist)
        return userlist
    def new_table(name):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='epusdt')
        cursor = db.cursor() 
        sql="CREATE TABLE  `{}`(telegramid bigint,score float,invite int,usertype int);".format(str(name))
        cursor.execute(sql)
        db.commit()
    def get_order(trade_id):
        db = pymysql.connect(host='127.0.0.1',
        port=3306,user='root', password='123456', database='epusdt')
        cursor = db.cursor() 
        sql="SELECT * FROM orders WHERE trade_id = {}".format(trade_id)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            trade_id = row[1]
            order_id=row[2]
            block_transaction_id = row[3]
            actual_amount = row[4]
            amount=row[5]
            token=row[6]
            staus=row[7]
            notify_url=row[8]
            callback_num=row[9]
            created_at=row[10]
            updated_at=row[11]
            deleted_at=row[12]
        if staus == 3 :
            return False
        elif staus == 2:
            return True
    def send(tgid):
        with open("user.json",'r') as load_f:
            user_dict = json.load(load_f)
        if str(tgid) in user_dict:
            user_dict[str(tgid)]+=1
        else:
            user_dict[str(tgid)]=1
        with open("user.json","w") as dump_f:
            json.dump(user_dict,dump_f)
            dump_f.close()
        return user_dict[str(tgid)]
