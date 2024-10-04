import json
import traceback
from copy import deepcopy
from khl import Message, PrivateMessage, Bot,requester
from khl.card import Card, CardMessage, Element, Module, Types
from PIL import Image, ImageDraw, ImageFont

# 用户数量的记录文件
from .Logging import _log
from ..file.Files import bot, BotUserDict,FileManage
from ..Gtime import get_time,get_date,time
from ..KookApi import guild_list, guild_view, upd_card, get_card_msg, icon_cm

# 记录频道/服务器信息的底图
font_color = '#000000'  # 黑色字体
log_base_img = Image.open("../screenshot/log_base.png")  # 文件路径

def log_bot_cmd(key='cmd',value:str=""):
    """记录命令的使用情况，，命令总数多少
    - key: 可以为cmd/user/guild
        - user/guild: 每日有多少服务器/用户使用了命令
        - cmd: 每日命令总数
    - value: 如果传入的是user/guild，value为服务器/用户id
    """
    global BotUserDict
    date = get_date() # 获取当日日期的str
    if key == 'cmd':
        BotUserDict['cmd_total'] += 1 # 命令执行总数+1
        key = 'data' # 需要更新为data
        # 判断（新建键值）
        if date not in BotUserDict['cmd'][key]:
            BotUserDict['cmd'][key][date] = 0
        # 当天命令使用次数+1
        BotUserDict['cmd'][key][date] += 1
    # 用户或者服务器
    else:
        assert(value) # value不能为空
        # 判断日期（新建键值）
        if date not in BotUserDict['cmd'][key]:
            BotUserDict['cmd'][key][date] = {}
        # 初始化为dict，插入的是kv键值对
        elif value not in BotUserDict['cmd'][key][date]:
            BotUserDict['cmd'][key][date][value] = 1
        else:
            BotUserDict['cmd'][key][date][value]+=1 # 使用命令数+1


def log_bot_user(user_id: str,cur_time:str) -> None:
    """记录使用命令的用户，更新用户使用命令的次数和最新使用的时间
    - user_id: kook user id
    - cur_time: time str as 23-03-01 23:04:58
    """
    global BotUserDict
    # 判断用户是否存在于总用户列表中
    if user_id in BotUserDict['user']['data']:
        BotUserDict['user']['data'][user_id]['cmd'] += 1
        BotUserDict['user']['data'][user_id]['used_time'] = cur_time
    else: # 不在，进行初始化
        BotUserDict['user']['data'][user_id] = {
            'cmd':1,
            'init_time':cur_time,
            'used_time':cur_time
        }
    # 再记录当日的用户使用命令
    log_bot_cmd('user',user_id)


# 记录服务器中的用户信息
def log_bot_guild(user_id: str, guild_id: str,guild_name:str) -> str:
    """Return:
    - GNAu: new user in new guild
    - NAu:  new user in old guild
    - Au:   old user
    """
    global BotUserDict
    # 获取当前时间的str
    cur_time = get_time()
    cur_time_stamp = time.time()
    # 先记录用户
    log_bot_user(user_id,cur_time)
    # 再记录当日的服务器使用命令
    log_bot_cmd('guild',guild_id)
    # 服务器不存在，新的用户/服务器
    if guild_id not in BotUserDict['guild']['data']:
        BotUserDict['guild']['data'][guild_id] = {}
        BotUserDict['guild']['data'][guild_id]['init_time'] = cur_time_stamp # 服务器的初始化时间
        BotUserDict['guild']['data'][guild_id]['used_time'] = cur_time_stamp # 服务器上次用命令的时间
        BotUserDict['guild']['data'][guild_id]['name'] = guild_name  # 服务器的名字
        BotUserDict['guild']['data'][guild_id]['cmd'] = 1      # 服务器的命令使用次数
        BotUserDict['guild']['data'][guild_id]['user'] = {} 
        # 用户在该服务器内的初始化时间（第一次使用命令的时间）
        BotUserDict['guild']['data'][guild_id]['user'][user_id] = cur_time 
        return "GNAu"
    # 服务器存在，新用户
    elif user_id not in BotUserDict['guild']['data'][guild_id]['user']:
        BotUserDict['guild']['data'][guild_id]['used_time'] = cur_time_stamp
        BotUserDict['guild']['data'][guild_id]['user'][user_id] = cur_time
        BotUserDict['guild']['data'][guild_id]['cmd'] += 1
        return "NAu"
    # 旧服务器，旧用户
    else:
        # 更新服务器的上次使用命令的时间
        BotUserDict['guild']['data'][guild_id]['used_time'] = cur_time_stamp
        BotUserDict['guild']['data'][guild_id]['cmd'] += 1
        return "Au"

# 在控制台打印msg内容，用作日志
def log_msg(msg: Message) -> None:
    try:
        log_bot_cmd()# 记录命令使用次数
        # 系统消息id，直接退出，不记录
        if msg.author_id == "3900775823":return
        # 私聊用户没有频道和服务器id
        if isinstance(msg, PrivateMessage):
            log_bot_user(msg.author_id,get_time())  # 记录用户
            _log.info(
                f"PrivateMsg | Au:{msg.author_id} {msg.author.username}#{msg.author.identify_num} | {msg.content}")
        else:
            Ustr = log_bot_guild(msg.author_id, msg.ctx.guild.id,msg.ctx.guild.name)  # 记录服务器和用户
            _log.info(
                f"G:{msg.ctx.guild.id} | C:{msg.ctx.channel.id} | {Ustr}:{msg.author_id} {msg.author.username}#{msg.author.identify_num} = {msg.content}"
            )
    except:
        _log.exception("Exception occurred")


# 画图，把当前加入的服务器总数等等信息以图片形式显示在README中
async def log_bot_img() -> None:
    bg = deepcopy(log_base_img)  # 新建一个画布
    draw = ImageDraw.Draw(bg)  # 让bg这个图层能被写字
    # 第一个参数 standard_text_position 是固定参数坐标 ， 第二个是文字内容 ， 第三个是字体 ， 第四个是字体颜色
    text_pos = [(185, 10), (378, 10), (185, 55), (378, 55)]  #左上/右上/左下/右下
    text_info = [
        str(BotUserDict['guild']['guild_total']),
        str(BotUserDict['guild']['guild_active']),
        str(BotUserDict['user']['user_total']),
        str(BotUserDict['cmd_total'])
    ]
    i = 0
    for pos in text_pos:
        draw.text(pos, text_info[i], font=ImageFont.truetype('./config/MISTRAL.TTF', 22), fill=font_color)
        i += 1
    # 保存图片
    bg.save(f'../screenshot/log.png')
    _log.info("log.png draw finished")


# bot用户记录dict处理
async def log_bot_list(log_img_draw=True) -> FileManage:
    global BotUserDict
    # 加入的服务器数量，api获取
    Glist = await guild_list()
    Glist = Glist['data']['meta']['total']
    # api正常返回结果，赋值给全局变量
    BotUserDict['guild']['guild_total'] = Glist
    # dict里面保存的服务器，有用户活跃的服务器数量
    BotUserDict['guild']['guild_active'] = len(BotUserDict['guild']['data'])
    # 计算用户总数
    BotUserDict['user']['user_total'] = len(BotUserDict['user']['data'])
    # 遍历列表，获取服务器名称
    tempDict = deepcopy(BotUserDict)
    for gu in tempDict['guild']['data']:
        # 服务器名称的键值不在，才进行赋值
        if 'name' not in tempDict['guild']['data'][gu]:
            Gret = await guild_view(gu)
            if Gret['code'] != 0:  # 没有正常返回，可能是服务器被删除，或者机器人不在服务器内
                del BotUserDict['guild']['data'][gu]  # 删除键值
                _log.info(f"G:{gu} | guild-view: {Gret}")
                continue
            # 正常返回，赋值
            BotUserDict['guild']['data'][gu]['name'] = Gret['data']['name']
        else:
            continue
    # 画新图片
    if log_img_draw:
        await log_bot_img()
    _log.info("file handling finish, return BotUserDict")
    return BotUserDict

async def log_bot_list_text(LogDict: dict|FileManage,bot:Bot) -> str:
    """从LogDict中分选出两列服务器名和服务器用户数
    - 如果服务器没有名字，则用bot获取
    - 只会返回字数限制为5k之前的服务器
    """
    i = 0
    text = ""
    LogDictTemp = deepcopy(LogDict)
    for gu, ginfo in LogDictTemp['guild']['data'].items():
        i+=1
        try:
            guild_name = ginfo['name'] if ginfo['name'] else (await bot.client.fetch_guild(gu)).name
            # 截取一部分名字
            if (len(guild_name) > 12):
                guild_name = guild_name[:11]
                guild_name+='…'
            # 追加text
            text+=f"[{i}] {guild_name}   = {len(ginfo['user'])}\n"
            # 字数限制为5k字，超过就跳出
            if len(text) >= 4900:
                text+= f"字数限制，省略后续 {len(LogDictTemp['guild']['data']) - i} 个服务器"
                break
        except Exception as result:
            # api调用错误，403是机器人不在服务器，4000是服务器不存在
            if "guild/view' failed with" in str(result):
                _log.warning(f"err ouccur | g:{gu} | {str(result)}")
                continue
            # 其他错误
            _log.exception(f"err ouccur | g:{gu}")
            continue
    
    return text


# 出现kook api异常的通用处理
async def api_request_failed_handler(def_name: str,
                                   excp: str,
                                   msg: Message,
                                   bot: Bot,
                                   cm = CardMessage(),
                                   send_msg: dict[str, str] = {}) -> None:
    """Args:
    - def_name: name of def to print in log
    - excp: taraceback.fromat_exc()
    - msg: khl.Message
    - bot: khl.Bot
    - cm: khl.card.CardMessage, for json.dumps / resend
    - send_msg: return value of msg.reply or bot.send
    """
    _log.exception(f"APIRequestFailed in {def_name} | Au:{msg.author_id}")
    err_str = f"ERR! [{get_time()}] {def_name} Au:{msg.author_id} APIRequestFailed\n```\n{excp}\n```"
    text = f"啊哦，出现了一些问题\n" + err_str
    text_sub = 'e'
    # 引用不存在的时候，直接向频道或者用户私聊重新发送消息
    if "引用不存在" in excp:
        if isinstance(msg, PrivateMessage):
            cur_user = await bot.client.fetch_user(msg.author_id)
            await cur_user.send(cm)
        else:
            cur_ch = await bot.client.fetch_public_channel(msg.ctx.channel.id)
            await bot.send(cur_ch, cm)
        _log.error(f"Au:{msg.author_id} | 引用不存在, 直接发送cm")
        return
    elif "json没有通过验证" in excp or "json格式不正确" in excp:
        _log.error(f"Au:{msg.author_id} | json.dumps: {json.dumps(cm)}")
        text_sub = f"卡片消息json没有通过验证或格式不正确"
    elif "屏蔽" in excp:
        _log.error(f"Au:{msg.author_id} | 用户屏蔽或权限不足")
        text_sub = f"阿狸无法向您发出私信，请检查你的隐私设置"

    cm = await get_card_msg(text, text_sub)
    if send_msg:  # 非none则执行更新消息，而不是直接发送
        await upd_card(send_msg['msg_id'], cm, channel_type=msg.channel_type)
    else:
        await msg.reply(cm)


# 基础错误的处理，带login提示(部分命令不需要这个提示)
async def base_exception_handler(def_name: str,
                                excp: str,
                                msg: Message,
                                send_msg: dict[str, str] = {},
                                debug_send=None,
                                help="建议加入帮助频道找我康康到底是啥问题") -> None:  # type: ignore
    """Args:
    - def_name: name of def to print in log
    - excp: taraceback.fromat_exc()
    - msg: khl.Message
    - send_msg: return value of msg.reply or bot.send
    - debug_send: Channel obj for sending err_str, send if not None
    - help: str for help_info, replyed in msg.reply
    """
    err_str = f"ERR! [{get_time()}] {def_name} Au:{msg.author_id}\n```\n{excp}\n```"
    _log.exception(f"Exception in {def_name} | Au:{msg.author_id}")
    cm0 = CardMessage()
    c = Card(color='#fb4b57')
    c.append(Module.Header(f"很抱歉，发生了一些错误"))
    c.append(Module.Divider())
    c.append(Module.Section(Element.Text(f"{err_str}\n\n{help}", Types.Text.KMD)))
    c.append(Module.Divider())
    c.append(Module.Section('有任何问题，请加入帮助服务器与我联系', Element.Button('帮助', 'https://kook.top/gpbTwZ', Types.Click.LINK)))
    cm0.append(c)
    if send_msg:  # 非{}则执行更新消息，而不是直接发送
        await upd_card(send_msg['msg_id'], cm0, channel_type=msg.channel_type)
    else:
        await msg.reply(cm0)
    # 如果debug_send不是None，则发送信息到报错频道
    if debug_send:
        await bot.client.send(debug_send, err_str)


#############################################################################################

import psutil, os


# 获取进程信息
async def get_proc_info(start_time=get_time()) -> CardMessage:
    """start_time: bot start time as 23-01-01 00:00:00"""
    p = psutil.Process(os.getpid())
    text = f"霸占的CPU百分比：{p.cpu_percent()} %\n"
    text += f"占用的MEM百分比：{format(p.memory_percent(), '.3f')} %\n"
    text += f"吃下的物理内存：{format((p.memory_info().rss / 1024 / 1024), '.4f')} MB\n"
    text += f"开辟的虚拟内存：{format((p.memory_info().vms / 1024 / 1024), '.4f')} MB\n"
    text += f"IO信息：\n{p.io_counters()}"
    cm = CardMessage()
    c = Card(Module.Header(f"来看看阿狸当前的负载吧！"), Module.Context(f"开机于 {start_time} | 记录于 {get_time()}"), Module.Divider(),
             Module.Section(Element.Text(text, Types.Text.KMD)))
    cm.append(c)
    return cm