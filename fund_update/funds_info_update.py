# -*- encoding: utf-8 -*-
import urllib
import urllib2
import time
import MySQLdb
import sys
sys.path.append('D:/Users/030031/PycharmProjects/Funds/dbConn')
import dbUtils
# 打开数据库连接
conn = dbUtils.get_conn()
cursor =  dbUtils.get_cursor(conn)
fundurl = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=**&page=1&per=1'
f = open("../files/second_fundsid.txt")
line = f.readline()
sql_id = 'select max(f.id) from fund_daily_nav f'
cursor.execute(sql_id)
max_id = cursor.fetchone()[0]
row=1
count = 1
while line:
        count +=1
        if(count>550):#中断后继续
            try:

                    sql_info = 'select * from fund_daily_nav where fund_code = \''+line.strip()+'\' and dt = DATE_SUB(curdate(),INTERVAL 0 DAY) '
                    cursor.execute(sql_info)
                    info = cursor.fetchone()
                    if info == None:
                        tempUrl = fundurl.replace('**', line.strip())
                        request = urllib2.Request(tempUrl)
                        response = urllib2.urlopen(request)
                        content = response.read()
                        content = content[content.index('<tbody>'):content.index('</tbody>')]
                        hisArrayData = content.split('</tr>')
                        for hisData in hisArrayData:
                            hisData = hisData.replace('</td><td class=\'tor bold bck\'>', ','). \
                                replace('</td><td class=\'tor bold\'>', ','). \
                                replace('</td><td class=\'tor bold grn\'>', ',').replace('</td><td class=\'tor bold red\'>',
                                                                                         ',')
                            if hisData == '':
                                break;
                            hisData = hisData[hisData.index('<tr><td>') + 8:hisData.index('</td>')]
                            # 770001,2017-05-02,0.8883,1.6883,-0.07%
                            tmData = hisData.split(',')
                            max_id += 1
                            # 检查是否已经同步
                            print time.strftime('%Y-%m-%d')
                        if tmData[0] == '2017-09-26':
                            if tmData[3] == '':
                                tmData[3] = '0.0%'
                            sql = 'INSERT INTO fund_daily_nav(id,fund_code, dt, nav, acc_nav,rate,update_dt)'
                            sql += ' VALUES (' + bytes(max_id) + ',\'' + line.strip() + '\',DATE_FORMAT(\'' + tmData[
                                0] + '\', \'%Y-%m-%d\'),' + tmData[1] + ',' + tmData[2] + ',' + tmData[3].replace('%', '0') + ',now())'
                            row+=1
                            print line.strip(), tmData
                            cursor.execute(sql)
                            if(row == 5):
                                conn.commit()
                                row=1


            except urllib2.URLError, e:
                    if hasattr(e, "code"):
                       print e.code
                    if hasattr(e, "reason"):
                       print e.reason
        line = f.readline()
conn.commit()
f.close()
dbUtils.close(cursor,conn)
