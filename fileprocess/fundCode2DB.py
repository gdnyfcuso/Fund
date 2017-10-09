# -*- encoding: utf-8 -*-
import sys
sys.path.append('D:/Users/030031/PycharmProjects/Funds/dbConn')
import dbUtils
conn = dbUtils.get_conn()
cursor =  dbUtils.get_cursor(conn)
fund_id = open('../files/second_fundsid.txt')

line = fund_id.readline()
count = 1
while line:
    sql = 'INSERT INTO basic_info(fund_code)'
        # SQL 插入语句
    sql += ' VALUES ('+line.strip()+')'
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        print (sql)
        count+=1
        if count == 500:
            conn.commit()
            count = 1
    except:
        # Rollback in case there is any error
        conn.rollback()
    line = fund_id.readline()
conn.commit()
# 关闭数据库连接
dbUtils.close(cursor,conn)
#关闭文件
fund_id.close()


