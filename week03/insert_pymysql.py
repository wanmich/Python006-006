#!/usr/bin/env python

import pymysql
from datetime import datetime
from my_enum import GenderEnum, DegreeEnum


db= pymysql.connect(host="localhost",user="testuser", password="testpassword",db="testdb",port=3306)

try:
    with db.cursor() as cursor:
        sql = '''INSERT INTO userinfo (user_name, user_age,\
            user_birthday, user_gender, user_degree, created_on)\
                VALUES (%s, %s, %s, %s, %s, %s)'''
        value = (
            ('张三', 11, datetime(2010, 10, 1),
             GenderEnum.male.name, DegreeEnum.middle_school.name, datetime.now()),
            ('李四', 20, datetime(2001, 8, 10),
             GenderEnum.female.name, DegreeEnum.bachelor.name, datetime.now()),
            ('王五', 35, datetime(1985, 1, 10),
             GenderEnum.male.name, DegreeEnum.phd.name, datetime.now())
        )
        cursor.executemany(sql, value)
    db.commit()

except Exception as e:
    print(f"fetch_error: {e}")

finally:
    # 关闭数据库连接
    db.close()
    print(cursor.rowcount)
