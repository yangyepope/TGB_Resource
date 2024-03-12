from pyrogram import Client
from TelegramBot import bot
from TelegramBot.helpers.filters import *
from pyrogram.types import BotCommand
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
import time
from TelegramBot.config import sudo_userid, owner_userid


@Client.on_message(filters.command(["start"]) & filters.private)
async def start(_, message: Message):
    await database.save_user(message.from_user)
    await bot.set_bot_commands([BotCommand("start", "开始服务")])
    await message.reply_text("您好，请选择服务:", quote=False,
                             reply_markup=ReplyKeyboardMarkup(
                                 [
                                     ["申请试用", "开始服务", "群操作人"],
                                     ["使用说明", "开通权限", "自助续费"],
                                     ["到期时间", "AiGPT客服", "推广奖励"]
                                 ],
                                 resize_keyboard=True
                             )
                             )


# filters.regex(r"^0$")
@Client.on_message(filters.regex(r"^申请试用$") & filters.private)
async def start_service(_, message: Message):
    await database.save_user(message.from_user)
    free = await database.test(message.from_user.id)
    if free:
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(free))
        await message.reply_text(f"申请成功，有效时间为 {time_str}", )
    else:
        await message.reply_text("您好，您已经试用过了，请联系客服购买正式授权！", )
    for i in owner_userid:
        userid = message.from_user.id
        username = message.from_user.username or " "
        name = (message.from_user.first_name or " ") + (message.from_user.last_name or "")
        await bot.send_message(i, f"**申请试用**\n\n用户ID：`{userid}`\n用户名：`{username}`\n用户名称：`{name}`")


@Client.on_message(filters.regex(r"^开始服务$") & filters.private)
async def b1(_, message: Message):
    await database.save_user(message.from_user)
    await message.reply_text("请加我进群", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "点我进群",
                    url="https://t.me/Ai118_bot?startgroup"
                )
            ]
        ]
    )
                             )


@Client.on_message(filters.regex(r"^群操作人$") & filters.private)
async def b2(_, message: Message):
    await database.save_user(message.from_user)
    await message.reply_text(
        "✔️群内发：设置操作人 @ xxxxx 先打空格再打 @，会弹出选择更方便。\n✔️群内发：删除操作人 @ xxxxx 先打空格再打 @，会弹出选择更方便。", )


@Client.on_message(filters.regex(r"^使用说明$") & filters.private)
async def b3(_, message: Message):
    await database.save_user(message.from_user)

    text = """【全新升级多功能自动统计机器人】🤖
✔️功能简介：
1记账 2设置操作人 3设置权限人 4设置下发地址 5设置担保规则 6设置欢迎信息 7设置客服 8设置押金 9欧意实时价格 10+-x÷计算 11自定义广告链接🔗

以下【】中的内容，均表示机器人的口令，在群内直接发送即可

✔️使用说明：
1私聊机器人点击申请试用
2私聊机器人点击开始服务把机器人添加到你群内
3机器人进入群内后,输入【设置费率X.X%】
比如【设置费率0】【设置费率8%】【设置费率8.5%】
4输入【设置美元汇率6.5】USDT下发汇率  可以自定义美元汇率
5输入【设置押金】比如100U 或者 100   带U是USDT押金 不带U是人民币押金 设置押金0U或0 就是关闭押金提示
6输入【开始】每天必须先输入此命令，机器人才会开始记录。默认是每天4点至第二天4点

✔️其它命令 例如：
入款【+100】或【+100u】或【+100/6.5】

入款修正 例如：
【入款-100】
【入款-100u】

下发 例如：
【下发100】【下发100u】

下发修正 例如：
【下发-100】
【下发-100U】

✔️以下这三个口令中的任何一个，都可以轻松查看当日账单
【0】【+0】【-0】显示账单   显示最近5条数据

✔️
【设置为计数模式】  只显示入款简洁模式
【设置显示模式2】  账单显示3条
【设置显示模式3】  账单显示1条
【设置显示模式4】  只显示总入款
【设置为原始模式】

✔️【设置/添加操作人 @xxxxx @xxxx】  设置群成员使用。先打空格再打@，会弹出选择更方便。注：再次设置的话就是新增。
 -或群内回复某人消息发：设置为操作人

✔️【显示操作人】

✔️【删除操作人 @xxxxx】 先输入“删除操作人” 然后空格，再打@，就出来了选择，这样更方便
例如 【删除操作人 @xxxxx @xxxx】

✔️【设置美元汇率6.5】  如需显示美元，可设置这个，汇率可改变，隐藏的话再次设置为0。
【设置美元汇率0】   则清空美元汇率。
【设置美元实时汇率】USDT下发汇率 与 欧意交易所C2C买盘一的价格实时同步

✔️【清理/删除今天数据】  慎用，必须由权限人发送命令 

✔️USDT独立功能命令：
【lk】  列出实时银行卡价格
【lz】  列出实时支付宝价格
【lw】  列出实时微信价格

【k100】  实时卡价计算100元换算usdt
【z100】  实时支价计算100元换算usdt
【w100】  实时微价计算100元换算usdt

【/set 5%】 设置费率5%
【/gd 6.8】 汇率固定
【/usdt】   设置币价功能

✔️【账单显示U开启】  发送该命令后，账单入款和下发都会显示 USD
  【账单显示U关闭】  发送该命令后，账单入款和下发都不会再显示 USD
  
✔【设置押金】比如 设置押金1000U 入金到了百分之70时候机器人会开始提示 3分钟一次 直到下发低于押金的百分之70
   1000U 代表USDT  1000 代表人民币  有区分的。【显示押金】就弹出你设定的押金  【设置押金0u/0】关闭功能

✔️【设置下发地址】 这个可以给群里增加地址一个下发地址，一个群仅能增加一个
例如：【设置下发地址0x12345678】  （注意下发地址后面没有冒号或空格）
群内任何人发送【地址】都会显示权限人设置的下发地址

自定义广告链接🔗(机器人每一次发账单的时候，会展示你的广告链接)
规则：设置链接+链接名称+网址
注意：网站必须为http或者https开头,否则不生效
例如：【设置链接+统计机器人+https://t.me/AI118_bot】
【链接显示关闭】  机器人每一次发账单的时候，会展示你的广告链接
【链接显示开启】  机器人每一次发账单的时候，则不会展示你的广告链接

✔️【设置担保规则】  这个可以给群里增加地址一个担保规则，一个群仅能增加一个
例如：【设置担保信息玉皇大帝担保】  （注意担保信息后面没有冒号）
群内任何人发送  【担保规则】  都会显示权限人设置的相关担保信息

✔️【设置欢迎信息】  这个可以给群里增加地址一个欢迎信息，一个群仅能增加一个
例如：【设置欢迎信息Hi兄弟你来了，欢迎加入】  （注意欢迎信息后面没有冒号）
任何新人进群机器人都会发送欢迎信息 "Hi兄弟你来了，欢迎加入"

✔️【设置客服】这个是添加客服信息功能
例如：【设置客服 小学 @xuezhang 】内容自己填写 任何人输入 客服就会弹出相应内容。

✔️【设置权限人】 这个功能是 比如你付费买了机器人你想给你团队其它人授权权限人
你只需要叫他在群里任意发一个信息你在群内点击回复他的信息【设置权限人】，他即可成为权限人
或者群内输入 【设置/添加权限人 @xxxxx @xxxx】  设置成员使用。先打空格再打@，会弹出选择更方便。注：再次设置的话就是新增。

你也可以点击他发的信息回复【删除权限人】,就删除了他的权限 
或者或者群内输入 【删除权限人 @xxxxx @xxxx】  删除成员权限。先打空格再打@，会弹出选择更方便。

【显示权限人】可以查看你给谁授权了权限人，权限人和你功能一样，除了不可以给别人授权权限人以外。 
可以授权的权限人上限是5人

✔️最后需注意：
1：计算器  群里所有人都可以使用
2：加减分  开关U显示 设置美元汇率  设置费率  （权限人和操作人都可以使用）
3：【设置下发地址】,【设置担保规则】,【设置欢迎信息】,【清理今天数据】 只有授权人和权限人可以操作 
4：客服联系 @Ai118 @Ai008"""
    await message.reply_text(text)


@Client.on_message(filters.regex(r"^开通权限$") & filters.private)
async def b4(_, message: Message):
    await database.save_user(message.from_user)
    text = '''🔰以下三个口令🔰
        ✔️设置权限人
        想设置谁为权限人，就可以在群内回复谁的消息，回复内容为 【设置权限人】，则就授权该用户为权限人
        或者群内输入 【设置/添加权限人 @xxxxx @xxxx】  设置成员使用。先打空格再打@，会弹出选择更方便。注：再次设置的话就是新增 
        ✔️删除权限人
        想删除之前设置的权限人，就可以在群内回复他的消息，回复内容为【删除权限人】，则就删除该用户的权限人授权
        ✔️显示权限人
        在群内直接 输入【显示权限人】，就可以显示您之前设置过的权限人'''
    await message.reply_photo(photo="https://img.tg.sb/file/2201e0b6998d62b934bcf.jpg", caption=text)


@Client.on_message(filters.regex(r"^自助续费$") & filters.private)
async def b5(_, message: Message):
    for i in owner_userid:
        userid = message.from_user.id
        username = message.from_user.username or " "
        name = (message.from_user.first_name or " ") + (message.from_user.last_name or "")
        await bot.send_message(i, f"**自助续费**\n\n用户ID：`{userid}`\n用户名：`{username}`\n用户名称：`{name}`")
    await database.save_user(message.from_user)
    text = '''自助续费暂只支持USDT的trc通道'''
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "15天（30U）",
                    callback_data="renew"
                )
            ],
            [
                InlineKeyboardButton(
                    "一个月（55U）",
                    callback_data="renew"
                )
            ],
            [
                InlineKeyboardButton(
                    "三个月（148U/9折）",
                    callback_data="renew"
                )
            ]
        ]
    ))


@Client.on_message(filters.regex(r"^到期时间$") & filters.private)
async def b6(_, message: Message):
    await database.save_user(message.from_user)
    timestamp = await database.get_expire_date(message.from_user.id)
    # 格式化为本地时间
    time_local = time.localtime(timestamp)
    # 转换为新的时间格式(2016-05-05 20:28:54)
    expire_date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    text = f'''您的到期时间为：{expire_date}'''
    await message.reply_text(text)


@Client.on_message(filters.regex(r"^AiGPT客服$") & filters.private)
async def b7(_, message: Message):
    await database.save_user(message.from_user)
    text = '''如有疑问，可以直接联系客服人员 @Ai118'''
    await message.reply_text(text)


@Client.on_message(filters.regex(r"^推广奖励$") & filters.private)
async def b8(_, message: Message):
    await database.save_user(message.from_user)
    text = '''推广奖励，你推广一个人申请试用然后告诉我们申请试用的飞机ID是什么,我们后台核对后给你发放奖励,奖励【统计机器人】使用时间加3天，1个3天 2个6天 以此类推@Ai118'''
    await message.reply_text(text)


# renew回调
@Client.on_callback_query(filters.regex(r"^renew$"))
async def renew_callback(_, c: CallbackQuery):
    text = '''订单已创建！
TRC-20地址：TUU5DG5nV52eiRZcxUbK8Ao97Td1888888

 - 注：地址为1888888结尾
 - 充值成功后，3分钟后再次查看时间。
 - 如充值有问题，请联系客服@Ai118'''
    await c.edit_message_text(text)
    for i in owner_userid:
        await bot.send_message(int(i), f"用户<code>{c.from_user.id}</code>({c.from_user.first_name})发起了续费请求")
