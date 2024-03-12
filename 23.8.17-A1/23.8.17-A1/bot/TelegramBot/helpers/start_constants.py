import datetime

# from TelegramBot.version import (__python_version__, __version__, __pyro_version__, __license__)
from TelegramBot.database import database


def unix_to_datetime(unix_timestamp):
    dt = datetime.datetime.fromtimestamp(unix_timestamp)
    return dt.strftime('%H:%M:%S')


def format_number(num):
    try:
        if num.is_integer():
            return str(int(num))
        else:
            return str(num)
    except AttributeError:
        return str(num)


async def get_display(group_id, display_id, rate, usd_rate, u_display, ad, ad_display, start_time, end_time):
    add_data = await database.get_bill(group_id, "add", start_time, end_time)
    out_data = await database.get_out_bill(group_id, "out", start_time, end_time)
    usd_rate = float(usd_rate)
    if display_id == 1:  # 默认显示模式
        if u_display and usd_rate > 0:
            add_count = len(add_data)
            out_count = len(out_data)
            add_part = ""
            out_part = ""
            total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
            ying_xiafa = format_number(round(sum([i['amount'] * (1 - rate) / (i['usd_rate'] if i['usd_rate'] != 0 else 1) for i in add_data]), 2))
            zong_xiafa = format_number(round(sum([i['usdt'] for i in out_data]), 2))
            wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))
            if float(zong_xiafa) == 0:
                zongxiafa_text = f"\n总下发：{zong_xiafa} USD"
            else:
                zongxiafa_text = f"\n总下发：{zong_xiafa} USD"
            for i in add_data[-5:]:
                add_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>   **{format_number(i['amount'])}** / {format_number(i['usd_rate'])} ={format_number(round(i['amount'] / (i['usd_rate'] if i['usd_rate'] != 0 else 1), 2))}U\n"
            for i in out_data[-5:]:
                if i['text'].find("U") != -1:
                    part = f"{format_number(round(i['usdt'], 2))}U 「{format_number(round(i['rmb'], 2))}」"
                else:
                    part = f"{format_number(round(i['usdt'], 2))}U 「{format_number(round(i['rmb'], 2))}」"
                out_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>    {part}\n"
            text = f"入款（{add_count}笔）：\n{add_part}\n下发（{out_count}笔）：\n{out_part}\n总入款：{total_add}\n费率：{format_number(rate * 100)}%\nUSD汇率：{usd_rate}\n\n应下发：{ying_xiafa} USD{zongxiafa_text}\n未下发：{wei_xiafa} USD"
            url_jump = True if add_count >= 5 else False
            return text, url_jump
        else:
            add_count = len(add_data)
            out_count = len(out_data)
            add_part = ""
            out_part = ""
            total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
            ying_xiafa = format_number(round(sum([i['amount'] / 1 for i in add_data]) * (1 - rate), 2))
            zong_xiafa = format_number(round(sum([i['rmb'] for i in out_data]), 2))
            wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))
            if float(zong_xiafa) == 0:
                zongxiafa_text = ""
            else:
                zongxiafa_text = f"\n总下发：{zong_xiafa}"
            for i in add_data[-5:]:
                add_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>   **{format_number(i['amount'])}**\n"
            for i in out_data[-5:]:
                if i['text'].find("U") != -1:
                    part = f"{format_number(i['rmb'])}"
                else:
                    part = f"{format_number(i['rmb'])}"
                out_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>    {part}\n"
            text = f"入款（{add_count}笔）：\n{add_part}\n下发（{out_count}笔）：\n{out_part}\n总入款：{total_add}\n费率：{format_number(rate * 100)}%\n\n应下发：{ying_xiafa}{zongxiafa_text}\n未下发：{wei_xiafa}"
            url_jump = True if add_count >= 5 else False
            return text, url_jump
    elif display_id == 4:  # 只显示总入款
        add_count = len(add_data)
        total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
        text = f"总入款：{total_add}"
        url_jump = True if add_count >= 5 else False
        return text, url_jump
    elif display_id == 3:  # 账单显示1条
        if u_display and usd_rate > 0:
            add_count = len(add_data)
            out_count = len(out_data)
            add_part = ""
            out_part = ""
            total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
            ying_xiafa = format_number(round(sum([i['amount'] * (1 - rate) / (i['usd_rate'] if i['usd_rate'] != 0 else 1) for i in add_data]), 2))
            zong_xiafa = format_number(round(sum([i['usdt'] for i in out_data]), 2))
            wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))
            if float(zong_xiafa) == 0:
                zongxiafa_text = f"\n总下发：{zong_xiafa} USD"
            else:
                zongxiafa_text = f"\n总下发：{zong_xiafa} USD"
            for i in add_data[-1:]:
                add_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>   **{format_number(i['amount'])}** / {format_number(i['usd_rate'])} ={format_number(round(i['amount'] / (i['usd_rate'] if i['usd_rate'] != 0 else 1), 2))}U\n"
            for i in out_data[-1:]:
                if i['text'].find("U") != -1:
                    part = f"{format_number(round(i['usdt'], 2))}U 「{format_number(round(i['rmb'], 2))}」"
                else:
                    part = f"{format_number(round(i['usdt'], 2))}U 「{format_number(round(i['rmb'], 2))}」"
                out_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>    {part}\n"
            text = f"入款（{add_count}笔）：\n{add_part}\n下发（{out_count}笔）：\n{out_part}\n总入款：{total_add}\n费率：{format_number(rate * 100)}%\nUSD汇率：{usd_rate}\n\n应下发：{ying_xiafa} USD{zongxiafa_text}\n未下发：{wei_xiafa} USD"
            url_jump = True if add_count >= 5 else False
            return text, url_jump
        else:
            add_count = len(add_data)
            out_count = len(out_data)
            add_part = ""
            out_part = ""
            total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
            ying_xiafa = format_number(round(sum([i['amount'] / 1 for i in add_data]) * (1 - rate), 2))
            zong_xiafa = format_number(round(sum([i['rmb'] for i in out_data]), 2))
            wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))
            if float(zong_xiafa) == 0:
                zongxiafa_text = ""
            else:
                zongxiafa_text = f"\n总下发：{zong_xiafa}"
            for i in add_data[-1:]:
                add_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>   **{format_number(i['amount'])}**\n"
            for i in out_data[-1:]:
                if i['text'].find("U") != -1:
                    part = f"{format_number(i['rmb'])}"
                else:
                    part = f"{format_number(i['rmb'])}"
                out_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>    {part}\n"
            text = f"入款（{add_count}笔）：\n{add_part}\n下发（{out_count}笔）：\n{out_part}\n总入款：{total_add}\n费率：{format_number(rate * 100)}%\n\n应下发：{ying_xiafa}{zongxiafa_text}\n未下发：{wei_xiafa}"
            url_jump = True if add_count >= 5 else False
            return text, url_jump
    elif display_id == 2:  # 账单显示3条
        if u_display and usd_rate > 0:
            add_count = len(add_data)
            out_count = len(out_data)
            add_part = ""
            out_part = ""
            total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
            ying_xiafa = format_number(round(sum([i['amount'] * (1 - rate) / (i['usd_rate'] if i['usd_rate'] != 0 else 1) for i in add_data]), 2))
            zong_xiafa = format_number(round(sum([i['usdt'] for i in out_data]), 2))
            wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))
            if float(zong_xiafa) == 0:
                zongxiafa_text = f"\n总下发：{zong_xiafa} USD"
            else:
                zongxiafa_text = f"\n总下发：{zong_xiafa} USD"
            for i in add_data[-3:]:
                add_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>   **{format_number(i['amount'])}** / {format_number(i['usd_rate'])} ={format_number(round(i['amount'] / (i['usd_rate'] if i['usd_rate'] != 0 else 1), 2))}U\n"
            for i in out_data[-3:]:
                if i['text'].find("U") != -1:
                    part = f"{format_number(round(i['usdt'], 2))}U 「{format_number(round(i['rmb'], 2))}」"
                else:
                    part = f"{format_number(round(i['usdt'], 2))}U 「{format_number(round(i['rmb'], 2))}」"
                out_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>    {part}\n"
            text = f"入款（{add_count}笔）：\n{add_part}\n下发（{out_count}笔）：\n{out_part}\n总入款：{total_add}\n费率：{format_number(rate)}%\nUSD汇率：{usd_rate}\n\n应下发：{ying_xiafa} USD{zongxiafa_text}\n未下发：{wei_xiafa} USD"
            url_jump = True if add_count >= 5 else False
            return text, url_jump
        else:
            add_count = len(add_data)
            out_count = len(out_data)
            add_part = ""
            out_part = ""
            total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
            ying_xiafa = format_number(round(sum([i['amount'] / 1 for i in add_data]) * (1 - rate / 100), 2))
            zong_xiafa = format_number(round(sum([i['rmb'] for i in out_data]), 2))
            wei_xiafa = format_number(round(float(ying_xiafa) - float(zong_xiafa), 2))
            if float(zong_xiafa) == 0:
                zongxiafa_text = ""
            else:
                zongxiafa_text = f"\n总下发：{zong_xiafa}"
            for i in add_data[-3:]:
                add_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>   **{format_number(i['amount'])}**\n"
            for i in out_data[-3:]:
                if i['text'].find("U") != -1:
                    part = f"{format_number(i['rmb'])}"
                else:
                    part = f"{format_number(i['rmb'])}"
                out_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>    {part}\n"
            text = f"入款（{add_count}笔）：\n{add_part}\n下发（{out_count}笔）：\n{out_part}\n总入款：{total_add}\n费率：{format_number(rate * 100)}%\n\n应下发：{ying_xiafa}{zongxiafa_text}\n未下发：{wei_xiafa}"
            url_jump = True if add_count >= 5 else False
            return text, url_jump
    elif display_id == 5:  # 只显示入款简洁模式
        if u_display and usd_rate > 0:
            add_count = len(add_data)
            add_part = ""
            total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
            ying_xiafa = format_number(round(sum([i['amount'] * (1 - rate) / (i['usd_rate'] if i['usd_rate'] != 0 else 1) for i in add_data]), 2))
            for i in add_data[-5:]:
                add_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>   **{format_number(i['amount'])}** / {format_number(i['usd_rate'])} ={format_number(round(i['amount'] / (i['usd_rate'] if i['usd_rate'] != 0 else 1), 2))}U\n"
            text = f"入款（{add_count}笔）：\n{add_part}\n\nUSD汇率：{usd_rate}\n总入款：{total_add} | {ying_xiafa} USD"
            url_jump = True if add_count >= 5 else False
            return text, url_jump
        else:
            add_count = len(add_data)
            add_part = ""
            total_add = format_number(round(sum([i['amount'] for i in add_data]), 2))
            for i in add_data[-5:]:
                add_part += f"  <code>{unix_to_datetime(i['timestamp'])}</code>   **{format_number(i['amount'])}** \n"
            text = f"入款（{add_count}笔）：\n{add_part}\n\n总入款：{total_add}"
            url_jump = True if add_count >= 5 else False
            return text, url_jump
