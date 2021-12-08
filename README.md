# chat-dingding

Open-Falcon Alarm api im to dingding

## 介绍

本项目采用 [fastapi](https://fastapi.tiangolo.com/) 作为框架

### 使用

#### 接口参数

##### 1. http://0.0.0.0:8082/im?corp=true&chat_id=<chatid1|chatid2>&robot_token=<robot_access_token>

> 用在 alarm/config/cfg.json > "api" > "im" 配置地址

+ `corp=true` 只有为true时，才会通过工作通知发送到用户
+ `chat_id` 群聊id，支持多个
+ `robot_token` 群机器人，Webhook地址中的access_token「注意 安全设置中不支持 加签」

⚠️ 注意：在采用 群聊或群机器人 发送时，告警模版中报警接收组的用户留一个用户即可，要不然可能会出现多次发送的情况

##### 2. http://0.0.0.0:8082/callback?corp=true&tos=<user1|user2>&chat_id=<chatid1|chatid2>&robot_token=<robot_access_token>

> 用在 模版配置 内的 callback地址（只支持http get方式回调）

+ `chat_id` & `robot_token` 同上
+ `tos` 钉钉用户ID

#### falcon端设置

+ 用户信息里的 IM 更换成 钉钉用户ID

## 安装

### 1. Clone

```shell
git clone https://github.com/oaixnah/chat-dingding.git
```

### 2. 环境配置

```shell
$ cd chat-dingding
$ python3 -m virtualenv ./venv
$ ./venv/bin/pip install -r requirements.txt
```

### 3. 钉钉应用配置

```text
修改 config.py
将其中 `AppId`，`AppKey`，`AppSecret` 换成 应用信息 里的 有效凭证
```

## 运行

### Debug

```shell
$ ./venv/bin/uvicorn main:app --reload --host 0.0.0.0:8082
```

### Run with gunicorn

```shell
$ bash control start

open http://127.0.0.1:8082 in your browser.
```

### Stop with gunicorn

```shell
$ bash control stop
```

### Log

```shell
$ bash control tail
```

## Contributing

README.md 文件编写参考: [open-falcon/dashboard](https://github.com/open-falcon/dashboard)

