from urllib.parse import parse_qsl

from fastapi import FastAPI, Request

from send import get_access_token, robot, conversation, corp_conversation

app = FastAPI()


@app.post("/im")
async def im(request: Request):
    """
    im 接口发送到 钉钉
    :param request:
    :return:         [10_10_10_10][load.1min 0.05>=0]
                     状态：PROBLEM
                     等级：P3
                     标签：-
                     持续：O3
                     始于：2021-12-08 13:20:00
    """
    _post = request_body_to_dict(await request.body())
    tos = _post.get('tos')
    content = format_content(_post.get('content'))
    robot_token = request.query_params.get('robot_token')
    corp = request.query_params.get('corp')
    chat_id = request.query_params.get('chat_id') or ''
    return send(content, tos, corp, robot_token, chat_id)


@app.get('/callback')
async def callback(request: Request):
    """
    告警模版内 callback接口
    :param request:
    :return:        [10_10_10_10][disk.io.msec_total=6.26667]
                    状态：PROBLEM
                    标签：device:sda
                    持续：3
                    始于：2021-12-08 13:21:00
    """
    content = '[{hostname}][{metric}={value}]\n' \
              '状态：{status}\n' \
              '标签：{tag}\n' \
              '持续：{step}\n' \
              '始于：{_time}'.format(hostname=request.query_params.get('endpoint'),
                                  metric=request.query_params.get('metric'),
                                  value=request.query_params.get('left_value'),
                                  status=request.query_params.get('status'),
                                  tag=request.query_params.get('tags'),
                                  step=request.query_params.get('step'),
                                  _time=request.query_params.get('time'),
                                  )
    # 群机器人
    robot_token = request.query_params.get('robot_token')
    corp = request.query_params.get('corp')
    tos = request.query_params.get('tos')
    chat_id = request.query_params.get('chat_id') or ''
    return send(content, tos, corp, robot_token, chat_id)


def send(content, tos, corp, robot_token, chat_id):
    """
    执行发送
    :param content:
    :param tos:
    :param corp:
    :param robot_token:
    :param chat_id:
    :return:
    """
    # 群机器人
    if robot_token:
        robot(robot_token, content)
    access_token = get_access_token()
    # 工作通知
    if corp == 'true':
        corp_conversation(access_token, content, tos)
    # 企业群
    for c_id in chat_id.split('|'):
        conversation(access_token, c_id, content)
    return {"msg": "ok"}


def request_body_to_dict(body):
    r = {}
    for k, v in parse_qsl(body.decode()):
        r[k] = v
    return r


def format_content(content):
    """
    规定信息格式
    :param str content: [P0][PROBLEM][10_10_10_51][][note all(#1) disk.io.msec_total device=sda 23.08333>=0][O2 2021-12-08 11:04:00]
    :return:
    """
    level, status, hostname, _, i, j = content[1:-1].split('][')
    note, func, metric, tag, cond = i.split(' ')
    step, _date, _time = j.split(' ')
    return f'[{hostname}][{metric} {cond}]\n' \
           f'状态：{status}\n' \
           f'等级：{level}\n' \
           f'标签：{tag or "-"}\n' \
           f'持续：{step}\n' \
           f'始于：{_date} {_time}'
