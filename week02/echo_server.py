#!/usr/bin/env python

import socket
import sys
from pathlib import Path
'''
week02作业：
不使用开源框架，基于 TCP 协议改造 echo 服务端和客户端代码，实现服务端和客户端可以传输单个文件的功能。

server端代码
'''

HOST = "localhost"
PORT = 10000


def echo_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
    except socket.error as e:
        print(e)
        sys.exit(1)

    print("等待连接...")
    while True:
        path = Path(__file__)
        parent_path = path.resolve().parent
        uploadfile_path = parent_path.joinpath("NOTE_upload.md")
        conn, addr = s.accept()
        print(f"收到来自{addr}的连接。")

        while True:
            data = conn.recv(1024)
            if data:
                with open(uploadfile_path, 'wb') as pipeline_f:
                    pipeline_f.write(data)
            else:
                break
        conn.close()
    s.close()


if __name__ == "__main__":
    echo_server()