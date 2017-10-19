#-*-coding:utf-8-*-
import sys
sys.path.append('D:/Users/030031/PycharmProjects/Funds/dbConn')
import dbUtils
import codecs
'''
连续增长天数小于8天，连续跌小于4天的基金
'''
def getAvailableFuds(sql,cursor,file5_8):
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
       fundsDic = {}
       for row in results:
           tm_sql = 'select rate from fund_daily_nav where fund_code = \''+row[0]+'\' order by dt'
           # 执行SQL语句
           cursor.execute(tm_sql)
           # 获取所有记录列表
           tm_results = cursor.fetchall()
           max_positive = 0
           positive = 0
           #positive_rate_add = 0
           max_negative = 0
           negative = 0
           #negative_rate_add = 0
           last_rate_flag = 0
           for tm_data in tm_results:
               rate = tm_data[0]
               if last_rate_flag == 0:
                   if rate < 0:
                       negative = 1
                       #negative_rate_add = rate
                       last_rate_flag = -1
                       if negative > max_negative:
                           max_negative = negative
                   else:
                       positive = 1
                       last_rate_flag = 1
                       #positive_rate_add = rate
                       if positive > max_positive:
                           max_positive = positive
                   continue
               if last_rate_flag < 0:
                   if rate < 0:
                       last_rate_flag = -1
                       negative += 1
                       #negative_rate_add +=rate
                   else:
                       last_rate_flag = 1
                       if negative > max_negative:
                           max_negative = negative
                       negative = 0
                       positive = 1
               else:
                   if rate > 0:
                       last_rate_flag = 1
                       positive += 1
                   else:
                       last_rate_flag = -1
                       if positive > max_positive:
                           max_positive = positive
                       positive = 0
                       negative = 1
           #连续涨小于8天 连续跌小于5天
           if max_negative < 5 and max_positive < 8:
               tmStr = str(row[0])+'--max_positive'+str(max_positive)+'--max_negative'+str(max_negative)+'\n'
               file5_8.write(tmStr)
    except:
       print ("Error: unable to fecth data")


if __name__=="__main__":
    conn = dbUtils.get_conn()
    cursor = dbUtils.get_cursor(conn)
    file5_8 = codecs.open('../files/连续跌小于5天（涨小于8天）.txt', 'a', 'utf-8')
    # 词条sql 可以查询出 历史最大涨幅大于最大跌幅的基金 并且最大涨幅大于2个百分点
    sql = 'select DISTINCT(fund_code) from (select fund_code from fund_daily_nav group by fund_code HAVING MAX(rate)-ABS(MIN(rate)) >= 0 and MAX(rate) >2 and ABS(MIN(rate)) <3) a'
    getAvailableFuds(sql, cursor,file5_8)
    file5_8.close()
    # 关闭数据库连接
    dbUtils.close(cursor, conn)