#!/usr/bin/env python

import requests
from pathlib import Path
from lxml import etree
from queue import Queue
import threading
import json
import time
'''
week02作业：
使用 requests 库抓取知乎任意一个话题下排名前 15 条的答案内容 (如果对前端熟悉请抓取所有答案)，并将内容保存到本地的一个文件。
问题：蚂蚁金服若没有被监管的话，会引起哪些问题？
链接：https://www.zhihu.com/question/429648797
'''


class CrawlThread(threading.Thread):
    '''
    爬虫类
    '''
    def __init__(self, thread_id, queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }

    def run(self):
        # 重写run方法
        print(f'启动线程：{self.thread_id}')
        self.scheduler()
        print(f'结束线程：{self.thread_id}')

    # 模拟任务调度
    def scheduler(self):
        while not self.queue.empty():
            # 队列为空不处理
            offset = self.queue.get()
            print(f'下载线程：{self.thread_id}, offset：{offset}')

            url = f'https://www.zhihu.com/api/v4/questions/429648797/answers?include=content&limit={limit}&offset={offset}&platform=desktop&sort_by=default'

            try:
                # downloader 下载器
                response = requests.get(url, headers=self.headers)
                dataQueue.put(response.text)
            except Exception as e:
                print('下载出现异常', e)


class ParserThread(threading.Thread):
    '''
    页面内容分析
    '''
    def __init__(self, thread_id, queue, file):
        threading.Thread.__init__(self)  # 上面使用了super()
        self.thread_id = thread_id
        self.queue = queue
        self.file = file

    def run(self):
        print(f'启动线程：{self.thread_id}')
        while flag or not self.queue.empty():
            try:
                item = self.queue.get(False)  # 参数为false时队列为空，抛出异常
                if not item:
                    continue
                self.parse_data(item)
                self.queue.task_done()  # get之后检测是否会阻塞
            except Exception as e:
                pass
        print(f'结束线程：{self.thread_id}')

    def parse_data(self, item):
        '''
        解析网页内容的函数
        :param item:
        :return:
        '''
        try:

            res_dict = json.loads(item)
            # print(f"res_dict:\n{res_dict}")
            answers = res_dict['data']
            # print(f"answers:\n{answers}")
            contents = []
            for answer in answers:
                content = answer['content']
                # print(f"content:\n{content}")
                contents.append(content)

            answer_text = ''
            for content in contents:
                html = etree.HTML(content)
                answer = html.xpath('//p/text()')
                # print(f"answer len: {len(answer)}")
                answer_text += ''.join(answer) + '\r\n\r\n'
                print(f"answer: \n{answer_text}")

            self.file.write(answer_text)

        except Exception as e:
            print('answer error', e)


if __name__ == '__main__':
    limit = 5  # 保持默认limit
    num_of_answers = 15  #获取前15个答案
    data_len = int(
        num_of_answers / limit) + (1 if num_of_answers % limit > 0 else 0)

    # 定义存放offset的任务队列
    offsetQueue = Queue(data_len)
    for offset in range(0, data_len):
        offsetQueue.put(offset)

    # 定义存放解析数据的任务队列
    dataQueue = Queue()

    # 爬虫线程
    crawl_threads = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, offsetQueue)
        thread.start()
        crawl_threads.append(thread)

    # 将结果保存到文件中
    path = Path(__file__)
    parent_path = path.resolve().parent
    file_path = parent_path.joinpath(f'answers_top{num_of_answers}.txt')
    with open(file_path, 'a', encoding='utf-8') as pipeline_f:
        pipeline_f.write('问题：蚂蚁金服若没有被监管的话，会引起哪些问题？\r\n\r\n')

        # 解析线程
        parse_thread = []
        parser_name_list = ['parse_1', 'parse_2', 'parse_3']
        flag = True
        for thread_id in parser_name_list:
            thread = ParserThread(thread_id, dataQueue, pipeline_f)
            thread.start()
            parse_thread.append(thread)

        # 结束crawl线程
        for t in crawl_threads:
            t.join()

        print(f"len dataQueue: {dataQueue.qsize()}")
        print(f"mark1")
        # 结束parse线程
        flag = False
        for t in parse_thread:
            t.join()

    print('退出主线程')
