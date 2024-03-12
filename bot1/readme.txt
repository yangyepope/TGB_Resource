1，配置環境
 安裝python 版本>=3.6
 安裝依賴 pip install -r r.txt
 安裝mysql 運行以下命令 (若您不想更改原文件 請將root密碼設爲123456 否則您需要前往sql_user.py修改數據庫配置)
	create database du;
	use du;
	CREATE TABLE  `user`(telegramid bigint,score float,invite int,usertype int);
2，修改bot配置
 打開config.json
 {
    "token":填寫機器人token,
    "apitoken":填寫duupay的token 若沒有請前往 http://t.me/duupaybot 點擊🛠商戶合作&開發者接入獲取,
    "price":填寫單價,
    "channel":["@sharesgk"] 填寫頻道用戶名 可以多個,
    "admin":[5515722973] 填寫admin的telegramid,
    "shenhe":審核群的群id,
    "tablename":填寫用戶數據儲存表（若您完全依照步驟1 請直接填寫user）,
    "keyboard":""不用填！
 
 設置按鈕：打開main.py 翻到最底下
 修改    mainkeyboard=InlineKeyboardMarkup([[InlineKeyboardButton("✅担保交易",url='https://t.me/'),InlineKeyboardButton("🔰自助发布",url='https://t.me/')],
                                       [InlineKeyboardButton("🔰公群频道",url='https://t.me/'),InlineKeyboardButton("💁人工客服",url='https://')]])

3 運行bot python -m main.py 後臺運行（linux） nohup python -m main.py &