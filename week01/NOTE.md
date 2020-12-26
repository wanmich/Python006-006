# week01 学习笔记

## 01 区分Python版本
使用```python -V```和```pip -V```查看当前python和pip的版本
``` bash
$ python -V
Python 3.7.3

$ pip -V
pip 20.3.3 from /home/wan/.local/lib/python3.7/site-packages/pip (python 3.7)
```

## 02 Python基本数据类型
- None 空值  
- Bool 布尔值  
- 数值  整数、浮点数、复数  
- 序列 字符串、列表、元组  
- 集合 字典  
- 可调用 函数  

## 03 高级数据类型
- collections 容器数据类型
- nametuple() 命名元组
- deque 双端队列
- Counter 计数器
- OrderedDict 有序字典

## 04 Python常用的标准库

### time

```python
import time
time.asctime()
# 'Sat Dec 26 22:06:18 2020'

time.localtime()
# time.struct_time(tm_year=2020, tm_mon=12, tm_mday=26, tm_hour=22, tm_min=6, tm_sec=24, tm_wday=5, tm_yday=361, tm_isdst=0)

time.time()
# 1608991590.257505

time.sleep(1)

time.strftime('%Y-%m-%d %X', time.localtime())
# '2020-12-26 22:08:23'

time.strptime('2020-12-26 22:08:23', '%Y-%m-%d %X')
# time.struct_time(tm_year=2020, tm_mon=12, tm_mday=26, tm_hour=22, tm_min=8, tm_sec=23, tm_wday=5, tm_yday=361, tm_isdst=-1)

```

### datetime
```python
from datetime import datetime, timedelta

# 获取当前时间
datetime.today()
# datetime.datetime(2020, 12, 26, 22, 13, 41, 801763)
datetime.now()
# datetime.datetime(2020, 12, 26, 22, 13, 46, 700991)

# 时间偏移
datetime.now() + timedelta(days=1)
# datetime.datetime(2020, 12, 27, 22, 14, 26, 568321)

datetime.now() - timedelta(days=-1)
# datetime.datetime(2020, 12, 27, 22, 14, 41, 128373)

```


### random
```python
from random import random, randrange, choice, sample
random()
# 0.9163223880100664

randrange(0,101,2)
# 88

choice([1,2,3])
# 3

sample([1,2,3,4,5], k=4)
# [3, 2, 5, 4]

```


### logging
```python
import logging
logging.basicConfig(filename='test.log',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(name)-8s %(levelname)-8s [line: %(lineno)d] %(message)s')
logging.debug('debug msg')
logging.info('info msg')
logging.warning('warning msg')
logging.error('error msg')
logging.critical('critical msg')
# test.log
# 2020-12-26 22:30:39 root     DEBUG    [line: 1] debug msg
# 2020-12-26 22:30:49 root     INFO     [line: 1] info msg
# 2020-12-26 22:31:00 root     WARNING  [line: 1] warning msg
# 2020-12-26 22:31:09 root     ERROR    [line: 1] error msg
# 2020-12-26 22:31:19 root     CRITICAL [line: 1] critical msg

```

### json
```python
import json
json.loads('{"name":"testname","test":["python","java"]}')
# {'name': 'testname', 'test': ['python', 'java']}

json.dumps({'name': 'testname', 'test': ['python', 'java']})
# '{"name": "testname", "test": ["python", "java"]}'

```


### pathlib
```python
from pathlib import Path
p=Path()
p.resolve()
# PosixPath('/home/wan/workspace/Python006-006')

p1=Path('/usr/local/a.txt.py')
p1.name
# 'a.txt.py'
p1.stem
# 'a.txt'
p1.suffix
# '.py'
p1.suffixes
# ['.txt', '.py']
p1.parents
# <PosixPath.parents>
for tmp in p1.parents:
     print(tmp)
 
# /usr/local
# /usr
# /

p1.parent
# PosixPath('/usr/local')

p1.parts
# ('/', 'usr', 'local', 'a.txt.py')
```


## re
```python
import re
re.match('.{11}', '13123456789')
# <re.Match object; span=(0, 11), match='13123456789'>
re.match('.{11}', '13123456789').group()
# '13123456789'

re.match('.{11}', '13123456789').span()
# (0, 11)

re.match('.*@.*', '123@123.com')
# <re.Match object; span=(0, 11), match='123@123.com'>
re.match('(.*)@(.*)', '123@123.com').group()
# '123@123.com'
re.match('(.*)@(.*)', '123@123.com').group(1)
# '123'
re.match('(.*)@(.*)', '123@123.com').group(2)
# '123.com'
re.match('(.*)@(.*)', '123@123.com').group(0)
# '123@123.com'

re.search('@', '123@123.com')
# <re.Match object; span=(3, 4), match='@'>

re.findall('123', '123@123.com')
# ['123', '123']

re.sub('123', 'test', '123@123.com')
# 'test@test.com'

re.split('@', '123@123.com')
# ['123', '123.com']

re.split('(@)', '123@123.com')
# ['123', '@', '123.com']
```