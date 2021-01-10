#!/usr/bin/env python

import pymysql


db= pymysql.connect(host="localhost",user="testuser", password="testpassword",db="testdb",port=3306)

try:
    with db.cursor() as cursor:
        sql = '''SELECT * FROM userinfo'''
        cursor.execute(sql)
        users = cursor.fetchall()
        for user in users:
            print(user)
    db.commit()

except Exception as e:
    print(f"fetch_error: {e}")

finally:
    # 关闭数据库连接
    db.close()
    print(cursor.rowcount)