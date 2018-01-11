#获取最近3天 涨幅都小于0的数据
import codecs
import sys
sys.path.append('D:/Users/030031/PycharmProjects/Funds/dbConn')
import dbUtils

def getAvaiableFundsBydays(fund_code,days):
    # sql = 'select f.rate from fund_daily_nav f where f.fund_code = \''+fund_code+'\' and f.dt >= DATE_FORMAT(date_sub(now() ,interval ' +str(days)+ ' day) , \'%Y-%m-%d\')'
    sql = 'select f.rate from fund_daily_nav f where f.fund_code = \'' + fund_code + '\' order by f.dt desc'
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    fundRateList = []
    for row in results:
        fundRateList.append(row[0])
    if len(fundRateList)>=days and max(fundRateList[0:days]) < 0:
        print('----该基金连续跌',days,'天------',fund_code)
if __name__=="__main__":
    conn = dbUtils.get_conn()
    cursor = dbUtils.get_cursor(conn)
    #读文件
    fund_code_file = codecs.open('../files/second_fundsid.txt','r','utf-8')
    line = fund_code_file.readline()
    #读取连续5天
    days = 5
    while line:
        row = line.strip()
        getAvaiableFundsBydays(row, days)
        line = fund_code_file.readline()
    dbUtils.close(cursor, conn)
    fund_code_file.close()