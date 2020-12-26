#!/usr/bin/env python

import logging
import time
import os
from pathlib import Path

'''
week01作业：
编写一个函数, 当函数被调用时，将调用的时间记录在日志中, 日志文件的保存位置建议为：/var/log/python- 当前日期 /xxxx.log
'''


def init():
    current_date = time.strftime('%Y%m%d', time.localtime())
    py_file_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = py_file_dir + f'/var/log/Python-{current_date}/test.log'
    log_dir = os.path.dirname(log_path)

    if not os.path.exists(log_dir):
        print(f'日志目录[{log_dir}]不存在，创建中...')
        os.makedirs(log_dir)
        print(f'目录已创建')

    logging.basicConfig(filename=log_path,
                        level=logging.DEBUG,
                        datefmt='%H:%m:%d %x',
                        format='%(asctime)s %(name)-8s %(levelname)-8s [line: %(lineno)d] %(message)s'
                        )


def test():
    print('日志写入中，请按Contrl + C 结束...')
    while True:
        logging.debug('debug msg')
        time.sleep(1)
        logging.info('info msg')
        time.sleep(1)
        logging.warning('warning msg')
        time.sleep(1)
        logging.error('error msg')
        time.sleep(1)
        logging.critical('critical msg')
        time.sleep(1)


if __name__ == '__main__':
    init()
    test()
