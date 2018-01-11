import urllib.request
import http.cookiejar
import time
import sys
import random
sys.path.append('D:/Users/030031/PycharmProjects/Funds/dbConn')
import dbUtils
# head: dict of header
def makeMyOpener(head={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
if __name__=="__main__":
    #将每只基金最近5天的记录存入数据库中
    # 打开数据库连接
    conn = dbUtils.get_conn()
    cursor = dbUtils.get_cursor(conn)
    netValUrl = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=**&page=1&per=5'
    fundList = open("../files/second_fundsid.txt")
    line = fundList.readline()
    sleep_download_time = 0
    # dict  用来存放每只基金 最近5天的记录
    fundDicts = {}
    while line:
        tempUrl = netValUrl.replace('**', line.strip())
        oper = makeMyOpener()
        try:
            uop = oper.open(tempUrl, timeout=5)
            data = uop.read()
        except:
            continue
        # print(data.decode())
        content = data.decode()
        #data.close()
        sleep_download_time = random.randint(0,3)
        time.sleep(sleep_download_time)  # 这里时间自己设定
        content = content[content.index('<tbody>'):content.index('</tbody>')]
        hisArrayData = content.split('</tr>')
        fundNetList = []
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
            print('---------读取基金数据',line.strip())
            sql = 'INSERT INTO fund_daily_nav(fund_code, dt, nav, acc_nav,rate)'
            sql += ' VALUES (\'' + line.strip() + '\',DATE_FORMAT(\'' + tmData[0] + '\', \'%Y-%m-%d\'),'
            sql += tmData[1] + ','
            sql += tmData[2] + ','
            sql += tmData[3].replace('%', '0') + ')'
            try:
                cursor.execute(sql)
            except:
                continue
            print('插入')
        conn.commit()
        #    fundNetList.append(tmData)
        #fundDicts[line.strip()] = fundNetList
        #print(fundDicts)
        line = fundList.readline()

    #print(line.strip(), tmData)
    fundList.close()
    dbUtils.close(cursor, conn)