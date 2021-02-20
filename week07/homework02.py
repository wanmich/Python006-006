from loguru import logger
from collections import Iterator
'''
作业二：
自定义一个 python 函数，实现 map() 函数的功能。
'''


def my_map(func, *args):
    logger.info(f'args: {args}')
    for arg in zip(*args):
        logger.info(f'arg: {arg}')
        yield func(*arg)


def square(x):
    return x**2


def sum(x, y, z):
    return x + y + z


if __name__ == '__main__':
    g = my_map(square, (1, 2, 3, 4))
    logger.info(
        f'g: {g}, type: {type(g)}, is_iterator: {isinstance(g, Iterator)}')
    logger.info(f'next(g): {next(g)}')
    for i in g:
        logger.info(f'i: {i}')

    g = my_map(sum, (1, 2, 3, 4), (5, 6), (7, 8))
    logger.info(
        f'g: {g}, type: {type(g)}, is_iterator: {isinstance(g, Iterator)}')
    logger.info(f'next(g): {next(g)}')
    for i in g:
        logger.info(f'i: {i}')