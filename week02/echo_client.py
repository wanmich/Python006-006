#!/usr/bin/env python

import socket
import sys
from pathlib import Path
'''
week02作业：
不使用开源框架，基于 TCP 协议改造 echo 服务端和客户端代码，实现服务端和客户端可以传输单个文件的功能。

client端代码
'''

HOST = "localhost"
PORT = 10000


def echo_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    except socket.error as se:
        print(se)
        sys.exit(1)

    path = Path(__file__)
    parent_path = path.resolve().parent
    file_path = parent_path.joinpath("NOTE.md")
    with open(file_path, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                print(f"文件【{file_path}】内容读取且发送完毕。")
                break
            s.send(data)
        s.close()


if __name__ == "__main__":
    echo_client()