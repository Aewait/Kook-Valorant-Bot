


<h1 align="center">Kook-Valorant--bot</h1>


<h4 align="center">这是一个KOOK的「Valorant」小机器人</h4>



<div align="center">

[English](./README_EN.md) | 简体中文


![python](https://img.shields.io/badge/Python-3.8%2B-green) ![commit](https://img.shields.io/github/last-commit/Aewait/Valorant-kaiheila-bot) ![release](https://img.shields.io/github/v/release/Aewait/Valorant-kaiheila-bot)
[![khl server](https://www.kaiheila.cn/api/v3/badge/guild?guild_id=3566823018281801&style=3)](https://kaihei.co/oqz7Xg) ![githubstars](https://img.shields.io/github/stars/Aewait/Valorant-kaiheila-bot?style=social)
</div>

## 功能
当前机器人处于早期版本，目前支持回复valorant游戏错误码，查询valorant每日商店，和一些简单功能



下面是目前支持的功能列表：

| 帮助命令      | 功能                                       |
| ------------- | ------------------------------------------ |
| `/Ahri`           | 回复使用帮助（因`/help`和其他机器人冲突，故用阿狸的英文名`Ahri`替代） |
| `/vhelp` | Valorant相关查询功能的帮助命令                     |


| 游戏相关      | 功能                                       |
| ------------- | ------------------------------------------ |
| `/val 错误码` | 回复游戏错误码解决方法                     |
| `/saveid`     | 保存（修改）用户的游戏id                   |
| `/myid`       | 显示用户的游戏id                           |
| `/bundle 皮肤名`  | 搜索已有皮肤系列包含什么枪械               |
| `/lead 30 20` | 显示出亚服(ap)排行榜前30名胜场超过20的玩家 |
| `/login 账户 密码` | 私聊bot进行登录riot账户的操作(获取token) |
| `/logout` | 退出riot账户登录 |
| `/shop` | 获取每日商店的4个皮肤 |
| `/point` | 获取用户剩余的vp和r点 |

关于商店查询的初步功能已经添加，但是其`稳定性/是否封号`未知，建议谨慎使用。

| 其他命令    | 功能                                                         |
| ----------------- | ------------------------------------------------------------ |
| `/hello`          | 打个招呼 (一般用来测试bot在不在线)                                                 |
| `/roll 1 100`     | 掷色子1-100，范围可自行调节                                  |
| `/countdown 秒数` | 倒计时，默认60秒                                             |
| `/TL 内容` | 翻译内容。其他语言翻译为中文，中文默认翻译成en |
| `/TLON` | 在本文字频道`打开`实时翻译功能 |
| `/TLOFF` | 在本文字频道`关闭`实时翻译功能 |
| `/we 城市` | 查询`城市`未来3天的天气情况 |
| `/hs` | 历史上的今天（因为kook审核原因被删除） |
|         `无`         | 自动给新用户上对应角色（可自主修改）                           |
| `无` | 当有人助力服务器的时候，在通知频道发送感谢信息 |

你可以在[screenshot](./screenshot)文件夹中找到对应的截图示例

----

## 如何使用？

保证你的Linux中`Python`版本高于`3.8`，执行下面的安装库命令

~~~
pip install -r requirements.txt
~~~

> Q：为何`khl.py`只需要3.6.8以上版本，而本仓库需要3.8+？
>
> A：因为valorant的第三方`Python Api`需要3.8+版本

建议根据[khl.py](https://github.com/TWT233/khl.py)的`example`教程，学习KOOK机器人的基本搭建（很简单的，相信我）

如果你想直接使用本机器人，可以转到本仓库[WIKI](https://github.com/Aewait/Valorant-kaiheila-bot/wiki)查看更多引导内容

----

## To Do

下面是一些未来的计划

- [x] 增加保存用户游戏id的功能
- [x] 添加自动给新用户上色功能
- [ ] 学习python
- [x] 学习接入官方的`valorant api`库
- [ ] 实现查询游戏战绩（需要roit授权）
- [x] 实现玩家商店刷枪的查询
- [ ] 实现当商店刷新某一把枪的时候提醒玩家
- [ ] 查看玩家的夜市

由于很多人在使用类似商店查询软件后被ban，我决定正式停止相关功能的开发
>咳咳，虽然初步的商店查询功能已经上线，但是其是否`封号`依旧未知！建议使用小号测试，或者不要用相关功能

<img src="https://s1.ax1x.com/2022/07/07/jwNGMF.png" width="510px" height="360px"/>

----

## 依赖

由于本人压根没有系统的学过Python，所以本仓库的很多代码都是根据他人教程修改后使用的
* 基本框架参考[khl.py](https://github.com/TWT233/khl.py)提供的KOOK-Api库以及使用教程
* Valorant游戏部分代码基于 [frissyn/valorant.py](https://github.com/frissyn/valorant.py/) 项目
* Valorant游戏`主要`代码基于 [ValorantClientAPI](https://github.com/HeyM1ke/ValorantClientAPI) 项目
* 通过账户密码获取 `riot_auth_token` 基于 [floxay/python-riot-auth](https://github.com/floxay/python-riot-auth) 项目


### 特别鸣谢🎁
* [@DeeChael](https://github.com/DeeChael) for helping me debug
* [@Edint386](https://github.com/Edint386) for adding PIL_code for `/shop` 
* [@staciax](https://github.com/staciax) for [Valorant-DiscordBot/issues/74](https://github.com/staciax/Valorant-DiscordBot/issues/74)


