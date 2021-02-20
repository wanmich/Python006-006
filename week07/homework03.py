import time
from functools import wraps
from loguru import logger
'''
作业三：
实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
'''


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f'duration: {end - start}')
        return result

    return wrapper


@timer
def test(*args, **kwargs):
    logger.info(f'test is called.')
    logger.info(f'*args: {args}, type: {type(args)}')
    logger.info(f'**kwargs: {kwargs}, type: {type(kwargs)}')
    time.sleep(2)
    logger.info(f'end')


if __name__ == '__main__':
    test(1, 2, 3, a=1, b=2, c=3)