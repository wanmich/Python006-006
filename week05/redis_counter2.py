#! /usr/bin/env python

import redis
import threading
import time


class VideoCountThread(threading.Thread):
    def __init__(self, conn, thread_id, video_id):
        super().__init__()
        self.conn = conn
        self.thread_id = thread_id
        self.video_id = video_id

    def run(self):
        self.counter()

    def counter(self):
        for i in range(10):
            time.sleep(1)
            cur_count = self.conn.incr(str(self.video_id))
            print(f"thread_id: {self.thread_id}, id: {self.video_id}, views: {cur_count}")


if __name__ == '__main__':
    conn = redis.Redis(host='192.168.50.230', password='zaq1@xsw2')
    video_ids = [(1000 + i) for i in range(10)]
    init_res = [conn.set(str(id), 0) for id in video_ids]
    # [print(conn.get(str(id))) for id in video_ids]
    if init_res:
        [VideoCountThread(conn, f'thread_{(id - 1000)}', str(id)).start() for id in video_ids]