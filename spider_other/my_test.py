import os
import re

from util.my_request import MySession, MyRequest

if __name__ == '__main__':
    # DB = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='fish_movie', port=3306,charset='utf8')
    # CONN = DB.cursor()
    # dao = EntityDao('table_1214')
    # dataList = dao.findModelByName('宝贝儿','刘杰')
    # thunder = dataList[0][1]
    # name = dataList[0][0]
    # dao.updateModel('我你妈改了1','宝贝儿','刘杰')

    # session = MySession()
    # for i in range(100):
    #     response = MyRequest(session, "https://www.baidu.com", True).get()
    #     print("%s" % response)

    # var = request.proxy
    # pool = cfg.Proxy_Pool
    # print(request.proxy)

    # with open('C:/Users/Administrator/Desktop/store_s.json', 'w') as f:
    #     print('fuck you!', file=f)
    # f.close()

    pattern_ssr = re.compile(r'/www.mattkaydiary.com')
    test = 'ss://YWVzLTI1Ni1nY206WXlDQmVEZFlYNGNhZEhwQ2trbWRKTHE4QDg0LjE3LjUzLjIyNzo0Mzg5Mw==#https%3a%2f%2fwww.mattkaydiary.com%7c%e7%91%9e%e5%a3%ab(CH)Switzerland%2fZ%c3%bcrich'
    test = test.replace('https%3a%2f%2fwww.mattkaydiary.com%7c', '')
    # s = pattern_ssr.match(test)

    print('%s' % test)
