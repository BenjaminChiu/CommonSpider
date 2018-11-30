from dao.EntityDao import EntityDao
from model.TaskQueue import TaskQueue
from movieHome.dytt8Moive import dytt_Lastest

import requests


from thread.FloorWorkThread import FloorWorkThread

from model.RequestModel import RequestModel




# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
THREAD_SUM = 5



if __name__ == '__main__':

    # 测试获取最大 页面数
    # LASTEST_MOIVE_TOTAL_SUM = dytt_Lastest.getMaxsize()
    # print('【最新电影】一共  ' + str(LASTEST_MOIVE_TOTAL_SUM) + '  有个页面')
    # dyttlastest = dytt_Lastest(LASTEST_MOIVE_TOTAL_SUM)

    #获取所有页面的URL，floorList为容纳这些URL的容器（List）
    # floorList = dyttlastest.getPageUrlList()


    #将容器中的url集合 放入 队列（线程安全），方便使用多线程请求（效率更高）
    # floorQueue = TaskQueue.getFloorQueue()
    #
    # for item in floorList:
    #     floorQueue.put(item, 3)



    #使用多线程 从队列中请求页面
    # for i in range(THREAD_SUM):
    #     workThread = FloorWorkThread(floorQueue, i)
    #     workThread.start()

    #确保URL队列，还有数据
    # while True:
    #     if TaskQueue.isFloorQueueEmpty():
    #         break
    #     else:
    #         pass


    #第二阶段测试，页面内容的抓取
    # 'http://www.idyjy.com/sub/27365.html'
    # "http://www.idyjy.com/sub/19994.html"
    #
    # 'http://www.idyjy.com/sub/27366.html'
    url = 'http://www.idyjy.com/sub/26840.html'

    response = requests.get(url, headers=RequestModel.getHeaders(), proxies=RequestModel.getProxies(), timeout=3)

    print(' 请求【 ' + url + ' 】的结果： ' + str(response.status_code))

    # 需将电影天堂的页面的编码改为 GBK, 不然会出现乱码的情况
    response.encoding = 'GBK'


    # 分析 页面，将内容加入队列。一个队列就是一部完整的电影
    temp = dytt_Lastest.getMoiveInforms(url, response.text)


    # movieDao = EntityDao('testtable')
    # movieDao.NAME = 'testtable'
    # movieDao.insertData(temp)