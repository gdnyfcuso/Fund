# -*- coding: utf-8 -*-
#python operate mysql database
import MySQLdb

#数据库名称
DATABASE_NAME = ''
#host = 'localhost' or '172.0.0.1'
HOST = ''
#端口号
PORT = ''
#用户名称
USER_NAME = ''
#数据库密码
PASSWORD = ''
#数据库编码
CHAR_SET = ''
#初始化参数
def init():
  global DATABASE_NAME
  DATABASE_NAME = 'funds'
  global HOST
  HOST = 'localhost'
  global PORT
  PORT = '3306'
  global USER_NAME
  USER_NAME = 'xgs'
  global PASSWORD
  PASSWORD = 'x307706'
  global CHAR_SET
  CHAR_SET = 'utf8'
 #获取数据库连接
def get_conn():
   init()
   return MySQLdb.connect(host = HOST, user = USER_NAME, passwd = PASSWORD, db = DATABASE_NAME, charset = CHAR_SET)
#获取cursor
def get_cursor(conn):
       return conn.cursor()
 #关闭连接
def conn_close(conn):
    if conn != None:
     conn.close()
 #关闭cursor
def cursor_close(cursor):
     if cursor != None:
      cursor.close()
 #关闭所有
def close(cursor, conn):
     cursor_close(cursor)
     conn_close(conn)