#!/usr/bin/env python
'''
2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:

用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
将 ORM、插入、查询语句作为作业内容提交
'''

import pymysql
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from my_enum import GenderEnum, DegreeEnum

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'userinfo'
    user_id = Column(Integer(), primary_key=True, autoincrement=True)
    user_name = Column(String(128), nullable=False, unique=True)
    age = Column(Integer(), default=18)
    birthday = Column(DateTime(), nullable=True)
    gender = Column(Enum(GenderEnum), default=GenderEnum.male)
    degree = Column(Enum(DegreeEnum), default=DegreeEnum.bachelor)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


db_url = "mysql+pymysql://testuser:testpassword@localhost:3306/testdb"
engine = create_engine(db_url, echo=True, encoding='utf-8')

Base.metadata.create_all(engine)