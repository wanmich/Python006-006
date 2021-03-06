# 学习笔记

## 1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。

将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交

将增加远程用户的 SQL 语句作为作业内容提交


### 1.1.1 修改字符集的配置项

```
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html
[client]
default_character_set = utf8mb4

[mysql]
default_character_set = utf8mb4

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

interactive_timeout = 28800 #针对交互连接时间
wait_timeout = 28800 # 非交互连接时间
max_connections=1000 # MySql的最大连接数
character_set_server = utf8mb4 # 默认内部运行字符集，也是mysql字符集设置 
init_connect = 'SET NAMES utf8mb4' # 服务器为每个连接的客户端执行的字符串
character_set_client_handshake = FALSE
collation_server = utf8mb4_unicode_ci
```

### 1.1.2 验证字符集的 SQL 语句

```
show variables like '%character%';
```

### 1.2 将增加远程用户的 SQL 语句
```
CREATE USER 'testroot'@'%' IDENTIFIED BY 'testpass';
GRANT ALL PRIVILEGES ON testdb.* TO 'root' @'%';
```


## 2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:

用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间

[完整代码](https://github.com/wanmich/Python006-006/blob/main/week03/create_table_sqlalchemy.py)

将 ORM、插入、查询语句作为作业内容提交

[完整代码(ORM)](https://github.com/wanmich/Python006-006/blob/main/week03/create_table_sqlalchemy.py.py)

[完整代码(插入)](https://github.com/wanmich/Python006-006/blob/main/week03/insert_pymysql.py)

[完整代码(查询)](https://github.com/wanmich/Python006-006/blob/main/week03/query_pymysql.py)

## 3. 为以下 sql 语句标注执行顺序：

```
SELECT DISTINCT player_id, player_name, count(*) as num   # 5
FROM player JOIN team ON player.team_id = team.team_id    # 1
WHERE height > 1.80                                       # 2
GROUP BY player.team_id                                   # 3
HAVING num > 2                                            # 4
ORDER BY num DESC                                         # 6
LIMIT 2                                                   # 7
```
- Step1：FROM JOIN ON：player + team通过筛选生成新的虚拟表；
- Step2：WHERE ： 进一步筛选形成虚拟表；
- Step3：GROUP BY 执行分组操作
- Step4：HAVING 进行筛选，生成虚拟表
- Step5：SELECT 从上一个虚拟表中进行不重复字段查询
- Step6：ORDER 对查询结果进行降序排序
- Step7：LIMIT 取2条查询结果


## 4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?

Table1

id name

1 table1_table2

2 table1

Table2

id name

1 table1_table2

3 table2

举例: INNER JOIN
```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
INNER JOIN Table2
ON Table1.id = Table2.id;
```
查询结果：  
取交集，即满足`Table1.id = Table2.id`的所有值。

LEFT JOIN
```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
LEFT JOIN Table2
ON Table1.id = Table2.id;
```
查询结果：  
返回左表`Table1`所有记录+右表`Table2`满足`on`条件的记录，不满足的，如`Table2.id`，`Table2.name` 列会显示为`NULL`。

RIGHT JOIN
```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
RIGHT JOIN Table2
ON Table1.id = Table2.id;
```
查询结果：  
返回右表`Table1`所有记录+左表`Table2`满足`on`条件的记录，不满足的，如`Table1.id`，`Table1.name` 列会显示为`NULL`。


## 5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。

会增加。

参考：https://mp.weixin.qq.com/s/xe8jcTyZPMOmooO2TBweOw

## 6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：

一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

- 请合理设计三张表的字段类型和表结构；
- 请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。

[完整代码](https://github.com/wanmich/Python006-006/blob/main/week03/transfer.py)