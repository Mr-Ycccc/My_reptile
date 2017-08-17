# -*- coding:utf-8 -*-

from pymysql import connect
from dingdian import settings
import sys
import importlib

importlib.reload(sys)

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, port=MYSQL_PORT, database=MYSQL_DB)
cur = cnx.cursor()


class sql:
	@classmethod
	def insert_dd_name(cls, xs_name, xs_author, category, name_id, novelurl, serialstatus, serialnumber):
		insert_sql = 'INSERT INTO dd_xiaoshuo(`xs_name`,`xs_author`,`category`,`name_id`,`novelurl`,`serialstatus`,`serialnumber`) VALUES (%(xs_name)s,%(xs_author)s,%(category)s,%(name_id)s,%(novelurl)s,%(serialstatus)s,%(serialnumber)s)'
		value = {
			'xs_name': xs_name,
			'xs_author': xs_author,
			'category': category,
			'name_id': name_id,
			'novelurl': novelurl,
			'serialstatus': serialstatus,
			'serialnumber': serialnumber
		}
		cur.execute(insert_sql, value)
		cnx.commit()

	@classmethod
	def select_name(cls, name_id):
		select_sql = "select exists(select 1 from dd_xiaoshuo where name_id=%(name_id)s)"
		value = {
			'name_id': name_id
		}
		cur.execute(select_sql, value)
		return cur.fetchall()[0]
