# -- coding: utf-8 --**
from telegram import ParseMode
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import create_deep_linked_url
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.ext.updater import Updater
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import re
import os
import json
import asyncio
import random
from telegram.ext import Filters,MessageHandler,CallbackQueryHandler,PreCheckoutQueryHandler,ShippingQueryHandler
from telegram import LabeledPrice, ShippingOption, Update
from telegram import InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo
import time
import random,string
from sql_user import *
import duupay
#from elasticsearch import Elasticsearch
user_send={}
user_time={}
global price
class main:
    user_t={}
    def __init__(self,token,tablename,mainkeyboard,channelid,admin,aprice,shenhe,apitoken):
        global price
        price=aprice
        def aexec(func):
            def wrapper(update: Update, context: CallbackContext):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(func(update, context))
                loop.close()
            return wrapper
        @aexec
        async def play(update: Update, context: CallbackContext):
            query = update.callback_query
            if 'send' in query.data:
                if user.get(table=tablename,tgid=query.from_user.id)['score'] >= price:
                    user.score(table=tablename,tgid=query.from_user.id,score=price*-1)
                    times=query.data.split('-')[1]
                    print(times)
                    keyboard=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text='通過',callback_data='pass'),InlineKeyboardButton(text='不通過',callback_data='unpass')]
                    ])
                    msg=str(user_send[query.from_user.id]+'\n【累计发布{}次】\n{}\n{}'.format(user.send(tgid=query.from_user.id),str(times),query.from_user.id))
                    print(msg)
                    context.bot.send_message(
                        chat_id=shenhe,
                        #parse_mode='markdown',
                        disable_web_page_preview=True,
                        text=msg,
                        reply_markup=keyboard
                    )
                    query.edit_message_text('已发送至管理員 請等待審核結果！')
                else:
                    query.edit_message_text('您的余额不足 请先充值')
                pass
            elif query.data=='pass':
                sendtext=query.message.text
                times=int(sendtext.split('\n')[-2])
                tgid=int(sendtext.split('\n')[-1])

                if times > 1:
                    moretext='\n感谢老板在本供需的{}连发！！！'.format(times)
                else:
                    moretext=''
                while times > 0:
                    context.bot.send_message(
                        chat_id=channelid[0],
                        #parse_mode='markdown',
                        disable_web_page_preview=True,
                        text=str(sendtext[:-13])+moretext,
                        reply_markup=mainkeyboard
                    )
                    times -=1
                context.bot.send_message(chat_id=tgid,text="您的供需信息已成功发送！")
                query.edit_message_text('訊息已成功發送')
            elif query.data=='unpass':
                sendtext=query.message.text
                tgid=int(sendtext.split('\n')[-1])
                query.edit_message_text('success')
                context.bot.send_message(chat_id=tgid,text="您的供需未通过审核！")
            elif query.data=='cancel':
                query.edit_message_text('操作已取消')
            elif query.data=='gongying':
                keyboard=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text='供应模板',callback_data='gongying'),InlineKeyboardButton(text='需求模板',callback_data='xuqiu')]]
                )
                query.edit_message_text('''<pre>⭕️需求信息✅
供应商品：
供应内容：
价格接受：
是否支持担保：
联系用户： @
联系频道:（没有可不填写）</pre>''',parse_mode='html',reply_markup=keyboard)
            elif query.data=='xuqiu':
                keyboard=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text='供应模板',callback_data='gongying'),InlineKeyboardButton(text='需求模板',callback_data='xuqiu')]]
                )
                query.edit_message_text('''<pre>⭕️需求信息✅
需求商品：
需求内容：
价格接受：
是否支持担保：
联系用户： @
联系频道:（没有可不填写）</pre>''',parse_mode='html',reply_markup=keyboard)
            else:
                amount=int(float(query.data))
                data=duupay.create(seller=admin[0],buyer=query.from_user.id,amount=amount,commodity='供需bot充值 {}u'.format(amount),token=apitoken)
                keyboard=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text='點我支付',url=data['paylink'])]]
                )
                query.edit_message_text("*已為您創建訂單！*\n請點擊下方按鈕前往支付！",parse_mode='markdown',reply_markup=keyboard)
                t=0
                while True:
                    if duupay.query(orderid=data['orderid'],token=apitoken)['status']==1:
                        user.score(table=tablename,tgid=query.from_user.id,score=amount)
                        query.edit_message_text('充值成功！')
                        break
                    elif t >= 1200:
                        query.edit_message_text('充值失败！')
                    else:
                        time.sleep(0.9)
                        t+=1
                    
                    
                
        
        @aexec
        async def start(update: Update, context: CallbackContext):
            import telegram
            _= re.findall(r"(?:/start )(.+)", update.message.text)
            print(_)
            keyboard=[
                    ['💻 发布广告','💡 发布规则'],
                    ['💰 我要充值','👤 个人中心']
                ]
            if not user.issign(table=tablename,tgid=update.message.from_user.id):
                    user.add(table=tablename,tgid=update.message.from_user.id)
            update.message.reply_text("""付费广告 {}USDT
——————————————
发布付费广告严格要求如下
1：禁止附加任何表情【审批百分百不通过】
2：行数限制15行内，【超过百分百不通过】
3：禁止发布虚假内容，禁止诈骗欺骗用户🆘
4：无需备注累计广告次数，机器人会自动统计
——————————————
请编写好广告词，点击下方【💻 发布广告】""".format(price)
                                      ,reply_markup=telegram.ReplyKeyboardMarkup(keyboard,resize_keyboard=True))
            
       
        @aexec
        async def me(update: Update, context: CallbackContext):
            if user.issign(table=tablename, tgid=update.message.from_user.id):
                info=user.get(table=tablename, tgid=update.message.from_user.id)
                update.message.reply_text(
                    parse_mode='MarkdownV2',
                    reply_markup=mainkeyboard,
                    text="*🎉🎉欢迎使用个人信息面板*\n*🎉您的用户ID：`{}`*\n*🎉您的余额：*`{}`\n*🎉您的用户状态：*{}".format(info['id'],info['score'],info['usertype']))
            else:
                update.message.reply_text(
                    text='您还没有注册请发送 /start 进行注册',
                    reply_markup=mainkeyboard)
        @aexec
        async def create(update: Update, context: CallbackContext):
            if update.message.chat_id in admin:
                password= ''.join(random.sample(string.ascii_letters, 10))
                num = update.message.text[8:].replace('\n', ' ')
                with open ("{}.txt".format(password) , 'w') as d:
                    d.write(num)
                    d.close
                update.message.reply_text("生成1张卡密，价值{}\n`{}`".format(num,password),parse_mode='MarkdownV2')
        @aexec
        async def km(update: Update, context: CallbackContext):
            def file_name(file_dir):
                File_Name=[]
                for files in os.listdir(file_dir):
                    if os.path.splitext(files)[1] == '.txt':
                        File_Name.append(files)
                return File_Name
            txt_file_name=file_name(".")
            kmlist=txt_file_name
            km=update.message.text[4:].replace('\n', ' ')
            if "{}.txt".format(km) in kmlist:
                with open("{}.txt".format(km)) as d:
                    num=d.read()
                    user.score(table=tablename, tgid=update.message.from_user.id, score=int(num))
                    d.close()
                os.remove("{}.txt".format(km))
                update.message.reply_text("已使用卡密，增加了{}积分".format(num))
            else:
                update.message.reply_text("卡密无效或已被使用")

        @aexec
        async def echo(update: Update, context: CallbackContext):
            if update.message.text=='👤 个人中心':
                
                if user.issign(table=tablename, tgid=update.message.from_user.id):
                    info=user.get(table=tablename, tgid=update.message.from_user.id)
                    update.message.reply_text(
                    parse_mode='MarkdownV2',
                    text="*🎉🎉欢迎使用个人信息面板*\n*🎉您的用户ID：`{}`*\n*🎉您的余额：*`{}`\n*🎉您的用户状态：*{}".format(info['id'],info['score'],info['usertype']))
                else:
                    update.message.reply_text(
                    text='您还没有注册请发送 /start 进行注册')
            elif update.message.text=='💡 发布规则':
                update.message.reply_text(
                    text='''👇为了不让广告满天飞👇
1️⃣.供需信息实施收费制💰
2⃣️.一条信息只能发布一个商品📳
3⃣️.押金商家会有标识提高商品成交

''')
            elif update.message.text=='💰 我要充值':
                keyboard=[
    [InlineKeyboardButton("20",callback_data="20"),InlineKeyboardButton("50",callback_data="50"),InlineKeyboardButton("100",callback_data="100"),InlineKeyboardButton("200",callback_data="200")],
    [InlineKeyboardButton('人工充值&发布客服',url='https://t.me/wz222')]
    ]
                update.message.reply_text(
                    text='请选择需要充值的金额',reply_markup=InlineKeyboardMarkup(keyboard))
            elif update.message.text=='💻 发布广告':
                keyboard=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text='供应模板',callback_data='gongying'),InlineKeyboardButton(text='需求模板',callback_data='xuqiu')]]
                )
                update.message.reply_text(
                    text='''付费广告发布规则如下
———————————————
1：机器人发布时 一定注意小数点以及在规定时间完成付款！
2: 不得发布虚假诈骗广告，发现马上下架。
3: 广告行数不能超过15行,否则不予审核通过。
4: 如付错款或没在规定时间及时付款，都不会退还给您的USDT！
5：禁止携带其他供需平台上压字体，百分百不通过。

——————————————
感谢您认真的阅读！
下方是广告格式，点击文字即可复制
供应请选择供应模板，需求请选择需求模板''',parse_mode='html')
                update.message.reply_text(text=str('''```⭕️需求信息✅
需求商品：
需求内容：
价格接受：
是否支持担保：
联系用户： @
联系频道:（没有可不填写）```'''),parse_mode='markdown',reply_markup=keyboard)
            elif str(update.message.chat_id)==shenhe:
                if ' ' in update.message.text:
                        user.score(table=tablename,tgid=update.message.text.split(' ')[0],score=update.message.text.split(' ')[1])
                        update.message.reply_text('success')
                        context.bot.send_message(chat_id=update.message.text.split(' ')[0],
                                                 message='您获得了{}u'.format(update.message.text.split(' ')[1]))
                elif '-' in update.message.text:
                    user.score(table=tablename,tgid=update.message.text.split('-')[0],score=float(update.message.text.split('-')[1])*-1)
                    update.message.reply_text('success')
                    context.bot.send_message(chat_id=update.message.text.split(' ')[0],
                                                 message='您被扣除了{}u'.format(update.message.text.split(' ')[1]))
            else:
                info=user.get(table=tablename,tgid=update.message.from_user.id)
                score=float(info['score'])
                print(price)
                if  score>= float(price):
                    keyboard=InlineKeyboardMarkup([
    [InlineKeyboardButton("单发",callback_data='send-1'),InlineKeyboardButton("三连发",callback_data='send-3'),],
    [InlineKeyboardButton("五连发",callback_data='send-5'),InlineKeyboardButton("十连发",callback_data='send-10')],
    [InlineKeyboardButton("取消发送",callback_data='cancel')]
   ]
    )
                    user_send[update.message.from_user.id]=update.message.text
                    update.message.reply_text(
                    text='您确定要发布吗？\n本次发布将消耗{}usdt'.format(price),reply_markup=keyboard)
                else:
                    update.message.reply_text(
                    text='您的余额不足 请先充值')
        @aexec
        async def send(update: Update, context: CallbackContext):
            if update.message.from_user.id in admin:
                text=update.message.text_html[6:]
            ul=user.all_list(table=tablename)
            success=0
            while len(ul) > 0:
                try:
                    context.bot.send_message(
                    chat_id=ul[0][0],
                    text=text,
                    parse_mode='HTML'
                    )
                    success+=1
                except:
                    pass
                ul.remove(ul[0])
            update.message.reply_text(
                    text='发送完成 共有{}发送成功'.format(success))
        @aexec
        async def setp(update: Update, context: CallbackContext):
            if update.message.from_user.id in admin:
                global price
                price=float(update.message.text[6:])
                update.message.reply_text(
                    text='成功')
                
        token = token
        time.sleep(0.1)
        updater = Updater(token=token,use_context=True)
        #updater = Updater(token=token,use_context=True,request_kwargs={'proxy_url':'socks5h://127.0.0.1:7890'})
        dispatch = updater.dispatcher
        updater.dispatcher.add_handler(CallbackQueryHandler(play, run_async=True))
        updater.dispatcher.add_handler(CommandHandler('start', start, run_async=True))
        updater.dispatcher.add_handler(CommandHandler('send', send, run_async=True))
        updater.dispatcher.add_handler(CommandHandler('me', me, run_async=True))
        updater.dispatcher.add_handler(CommandHandler('km', km, run_async=True))
        updater.dispatcher.add_handler(CommandHandler('setp', setp, run_async=True))
        updater.dispatcher.add_handler(CommandHandler('create', create, run_async=True))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo, run_async=True))
        updater.start_polling()
        updater.idle()

with open("config.json",'r',encoding='utf-8') as load_f:
    data = json.load(load_f)
main(token=data['token'],
     channelid=data['channel'],
    tablename=data['tablename'],
    aprice=data['price'],
    mainkeyboard=InlineKeyboardMarkup([[InlineKeyboardButton("✅担保交易",url='https://t.me/'),InlineKeyboardButton("🔰自助发布",url='https://t.me/')],
                                       [InlineKeyboardButton("🔰公群频道",url='https://t.me/'),InlineKeyboardButton("💁人工客服",url='https://')]]),
    admin=data['admin'],
    apitoken=data['apitoken'],
    shenhe=data['shenhe']
    )    
