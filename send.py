import requests
import time

from config import AppId, AppKey, AppSecret


def get_access_token():
    """
    获取企业内部应用的access_token
    https://developers.dingtalk.com/document/app/obtain-orgapp-token
    :return:
    """

    def get_token():
        r = requests.get(
            f'https://oapi.dingtalk.com/gettoken?appkey={AppKey}&appsecret={AppSecret}',
        )
        return r.json().get('access_token')

    with open(AppKey, 'r') as f:
        t = f.read()
        if t:
            c, token = t.split()
            if (int(time.time()) - int(c)) < 7200:
                return token
        token = get_token()
        with open(AppKey, 'w') as f1:
            f1.write(' '.join((str(int(time.time())), token)))
        return token


def robot(access_token, content):
    """
    群机器人
    https://developers.dingtalk.com/document/robots/custom-robot-access
    :param str access_token:
    :param str content:
    :return:
    """
    r = requests.post(
        f'https://oapi.dingtalk.com/robot/send?access_token={access_token}',
        json={
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }
    )
    return r.json()


def conversation(access_token, chat_id, content):
    """
    发送消息到企业群
    https://developers.dingtalk.com/document/app/send-group-messages
    :param str access_token:
    :param str chat_id:
    :param str content:
    :return:
    """
    r = requests.post(
        f'https://oapi.dingtalk.com/chat/send?access_token={access_token}',
        json={
            "chatid": chat_id,
            "msg": {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
        }
    )
    return r.json()


def corp_conversation(access_token, content, userid_list, agent_id=AppId, dept_id_list=None, to_all_user='false'):
    """
    发送工作通知
    https://developers.dingtalk.com/document/app/asynchronous-sending-of-enterprise-session-messages
    :param str access_token:
    :param str agent_id:
    :param str content:
    :param str userid_list:
    :param str dept_id_list:
    :param str to_all_user:
    :return:
    """
    r = requests.post(
        f'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token={access_token}',
        json={
            "msg": {
                "text": {
                    "content": content
                },
                "msgtype": "text"
            },
            "to_all_user": to_all_user,
            "agent_id": agent_id,
            "dept_id_list": dept_id_list,
            "userid_list": userid_list
        }
    )
    return r.json()
