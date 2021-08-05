# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
# THREAD_SUM = 5
from util import cfg
from util.my_request import MySession
from util.my_request import MyRequest
from proxy_host.proxy_json import read_proxy_json

if __name__ == '__main__':
    # DB = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='fish_movie', port=3306,charset='utf8')
    # CONN = DB.cursor()
    # dao = EntityDao('table_1214')
    # dataList = dao.findModelByName('宝贝儿','刘杰')
    # thunder = dataList[0][1]
    # name = dataList[0][0]
    # dao.updateModel('我你妈改了1','宝贝儿','刘杰')
    read_proxy_json()
    session = MySession()
    request = MyRequest(session, "https://www.baidu.com", True)
    response = request.my_get()
    var = request.proxy
    pool = cfg.Proxy_Pool
    print(request.proxy)

    # 要想在代理池中修改用过的代理
    # 1. 拿着自己的信息，到池中比对，找到后再修改池中代理的hp值
