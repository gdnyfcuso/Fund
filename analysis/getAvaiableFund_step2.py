#-*-coding:utf-8-*-
import sys
sys.path.append('D:/Users/030031/PycharmProjects/Funds/dbConn')
import dbUtils
import codecs
'''
分析所有净值天数内，涨幅大于1.5个百分点的，2个百分点的天数比例，
分析最近4天连续跌的情况
'''
def rate_greater_than_2(fund_code,cursor):
    sql = 'select f.rate from fund_daily_nav f where f.fund_code = \''+fund_code+'\''
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    key_rate = 1.5
    key_rate_count = 0
    all_recodes = 0
    for row in results:
        rate = row[0]
        all_recodes += 1
        if(rate>=key_rate):
            key_rate_count+=1
    print (key_rate_count/all_recodes,'----大于阈值个数：',key_rate_count,'-------总个数：',all_recodes)
if __name__=="__main__":
    conn = dbUtils.get_conn()
    cursor = dbUtils.get_cursor(conn)
    #读文件 读取连续跌小于4天 连续涨小于8天的基金 code
    fund_code_file = codecs.open('../files/连续跌小于5天（涨小于8天）.txt','r','utf-8')
    line = fund_code_file.readline()
    while line:
        row = line.strip().split('--')
        rate_greater_than_2(row[0], cursor)
        line = fund_code_file.readline()
    dbUtils.close(cursor, conn)
    fund_code_file.close()