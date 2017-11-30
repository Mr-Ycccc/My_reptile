import sqlite3

#连接sqlite
conn=sqlite3.connect('test.db')
#创建cursor
cursor=conn.cursor()
#创建表
cursor.execute('create table if not exists user(id varchar(20) primary key,name varchar(20))')
#执行语句
cursor.execute('delete from user')
cursor.execute("insert into user (id,name) values ('1','Y')")
cursor.execute("insert into user (id,name) values ('2','C')")
#通过rowcount获得插入的行数
print(cursor.rowcount)
#执行查询语句:
cursor.execute('select * from user')
#获取查询结果集
values=cursor.fetchall()
print(values)
#关闭Cursor
cursor.close()
#提交事务
conn.commit()
#关闭连接
conn.close()