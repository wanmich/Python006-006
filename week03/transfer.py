#!/usr/bin/env python

'''
6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：

一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

请合理设计三张表的字段类型和表结构；
请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。
'''

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, create_engine, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
class User_table(Base):
    __tablename__ = 'user'
    uid = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(15), nullable=True, unique=True)

class Asset_table(Base):
    __tablename__ = 'asset'
    uid = Column(Integer(), primary_key=True, nullable=True)
    asset = Column(DECIMAL(19, 4), nullable=True)

class Transaction_table(Base):
    __tablename__ = 'transactions'
    one_id = Column(Integer(), primary_key=True)
    other_id = Column(Integer(), primary_key=True)
    deal = Column(DECIMAL(19, 4), nullable=True)
    create_date = Column(DateTime(), nullable=True)


def deal(one, other, deal, session):
    one_id = session.query(User_table.uid).filter(User_table.name == one).one()[0]
    other_id = session.query(User_table.uid).filter(User_table.name == other).one()[0]
    one_mon = session.query(Asset_table.asset).filter(Asset_table.uid==one_id, Asset_table.asset>deal).one()[0]
    other_mon = session.query(Asset_table.asset).filter(Asset_table.uid==other_id).one()[0]

    one_mon -= deal
    other_mon += deal
    session.query(Asset_table.asset).filter(Asset_table.uid==one_id).update({Asset_table.asset: one_mon})
    session.query(Asset_table.asset).filter(Asset_table.uid == other_id).update({Asset_table.asset: other_mon})

    transaction = Transaction_table(one_id=one_id,
                         other_id=other_id,
                         create_date=datetime.now(),
                         deal=deal)
    session.add(transaction)

if __name__ == '__main__':
    db_url = "mysql+pymysql://testuser:testpassword@localhost:3306/testdb?charset=utf8mb4"
    engine = create_engine(db_url, echo=True, encoding='utf-8')
    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()
    Base.metadata.create_all(engine)

    try:
        deal('张三','李四', 100, session)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()