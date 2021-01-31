#! /usr/bin/env python

import redis
import time


def sendsms(telephone_number: int, content='', key=None):
    slot = 6
    time.sleep(1)
    print('\n--------------------------START----------------------------')
    t1 = conn.hget(str(telephone_number), 't1').decode()
    if float(t1) == 0:
        t1 = time.time()
        conn.hset(str(telephone_number), 't1', t1)
        conn.hset(str(telephone_number), 'send_at', t1)
        conn.hincrby(str(telephone_number), 'count')
    else:
        t2 = time.time()
        count = conn.hget(str(telephone_number), 'count').decode()
        duration = (t2 - float(t1))
        if duration <= slot and int(count) == 5:
            conn.hmset(str(telephone_number), {'send_at': 0, 'count': 0, 't1': 0})
            print(f"1 分钟内发送次数超过 5 次, 请等待 1 分钟")
            time.sleep(5)
            # print(f"msg: 信息未发送\nto: {telephone_number}\ncontent: {content}")
            # print('--------------------------END----------------------------')
            # return 0
        elif duration > slot:
            conn.hmset(str(telephone_number), {'send_at': 0, 'count': 0, 't1': 0})
        conn.hset(str(telephone_number), 'send_at', time.time())
        conn.hincrby(str(telephone_number), 'count')
    count = conn.hget(str(telephone_number), 'count').decode()
    print(f"msg: 发送成功\nto: {telephone_number}\ncontent: {content}\ncount: {count}")
    print('--------------------------END----------------------------')


if __name__ == '__main__':
    conn = redis.Redis(host='192.168.50.231', password='zaq1@xsw2')
    telephone_numbers = [12345654321, 88887777666]
    [conn.hmset(str(t_num), {'send_at': 0, 'count': 0, 't1': 0}) for t_num in telephone_numbers]
    sendsms(12345654321, 'hello')
    sendsms(12345654321, 'hi')
    sendsms(12345654321, 'idiot')
    sendsms(12345654321, 'Are you Trump Donald')
    sendsms(12345654321, 'I am Biden, thank you brother')
    sendsms(12345654321, '今天天气很好，万里无云，蓝蓝的天空上飘着洁白的云彩')
    sendsms(88887777666, 'How are you?')
    sendsms(88887777666, ''.join([str(i) for i in range(203)]))
    sendsms(88887777666, '1'*140)
    sendsms(88887777666, '1'*139)