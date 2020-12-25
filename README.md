# 用 Python + SMTP 写一个爬虫脚本每天定时给邮箱发送问候邮件

## 项目介绍：

开发环境：Python >= 3.6

### 灵感来源
想每天可以定时收到一些消息，那作为程序员，这点小case还是很简单的
一开始想用 itchat 发送微信消息，后来发现不可行了，因为腾讯全部封掉了微信机器人
所以就打算发送邮箱啦！

### 项目地址：
Github:

### 使用库
- [requests][1] - 网络请求库
- [pyyaml][2] - 解析配置文件
- 定时任务 - 没有使用代码进行任务定时，而是打算通过 Ubuntu 的 cron 定时来运行本文件，然后发送消息

### 功能
定时发送早安，附带每日天气的提醒
定时发送晚安，附带土味情话

### 数据来源
天行数据 API：www.tianapi.com
短信发送 API：www.binstd.com

## 代码说明

### 目录结构
- config.yaml ：配置
- GFEverydayEmail.py：核心代码
- requirements.txt：需要安装的库
- run.py：项目运行类

## 项目配置 

### 安装依赖

使用 pip install -r requirements.txt 安装所有依赖

## 项目运行

### 1.直接运行
```
# 早安
python run.py 0
# 晚安
python run.py 1
```

### 2.定时运行
