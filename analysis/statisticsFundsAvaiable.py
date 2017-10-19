# -*- coding: UTF-8 -*-
import sys
sys.path.append('D:/Users/030031/PycharmProjects/Funds/dbConn')
import dbUtils

conn = dbUtils.get_conn()
cursor =  dbUtils.get_cursor(conn)

# SQL 查询语句
sql = 'select f.id,f.fund_code,f.dt,f.nav,f.acc_nav,f.rate from fund_daily_nav f where f.fund_code in (select fdn.fund_code from fund_daily_nav fdn   group by fdn.fund_code having max(fdn.rate) > 2 and max(fdn.rate) > ABS(min(fdn.rate))) order by f.dt asc'
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   fundsDic = {}
   for row in results:
      fundsAttr = [];
      fundsAttr.append(1)
      fundsAttr.append(0)
      id = row[0]
      fundCode = row[1]
      dt = row[2]
      nav = row[3]
      acc_nav = row[4]
      rate = row[5]
      if fundsDic.has_key(fundCode):
         tmData = fundsDic[fundCode]
         if(tmData[1]<6):
            #连续跌5天 以上
            if tmData[0] == 1 and rate < 0:
               tmData[1] += 1
            else:
               if rate < 0:
                  tmData[0] = 1
                  tmData[1] = 1
               if rate > 0:
                  tmData[0] = -1
                  tmData[1] = 0
      else:
         if rate < 0:
            fundsAttr[0] = 1
            fundsAttr[1] = 1
            fundsDic[fundCode] = fundsAttr
         else:
            fundsAttr[0] = -1
   print ('add log---')
   for key in fundsDic.keys():
      tmp = fundsDic[key]
      if tmp[1] >= 4:
         continue
      else:
         print ('available fund:'+key)
except:
   print ("Error: unable to fecth data")

# 关闭数据库连接
dbUtils.close(cursor,conn)