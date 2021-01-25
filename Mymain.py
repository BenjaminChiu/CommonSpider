#!/usr/bin/env python
# coding=utf-8


# import sqlite3

from MyThread.FloorWorkThread import FloorWorkThread
from MyThread.TopWorkThread import TopWorkThread
from model.TaskQueue import TaskQueue
from movieHome.dytt8Moive import dytt_Lastest
from service.EntityService import EntityService

'''
    程序主入口
'''

# LASTEST_MOIVE_TOTAL_SUM = 6 #164

# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
THREAD_SUM = 5


def startSpider():
    # 实例化对象

    # 电视剧 http://www.idyjy.com/w.asp?p=1&f=2&l=t

    # 确定起始页面 ，终止页面

    # dytt_Lastest.getMaxsize()
    LASTEST_MOIVE_TOTAL_SUM = dytt_Lastest.getMaxsize('http://www.idyjy.com/w.asp?p=1&f=3&l=t')
    # dyttlastest = dytt_Lastest('http://www.idyjy.com/w.asp?p=1&f=3&l=t', 'p=', '&f', LASTEST_MOIVE_TOTAL_SUM)
    dyttlastest = dytt_Lastest('http://www.idyjy.com/w.asp?p=885&f=3&l=t', 'p=', '&f', 898)

    pagelist = dyttlastest.getPageUrlList()

    # ======将 pageList加入队列，因为队列线程安全=========
    pageQueue = TaskQueue.getFloorQueue()
    for item in pagelist:
        pageQueue.put(item, 3)

    # =====1111==用线程请求pageQueue（pageList）（注意队列枯竭），将请求结果存入pageInfoList中=========
    for i in range(THREAD_SUM):
        workthread = FloorWorkThread(pageQueue, i)
        # workthread.run()   #原版是workthread.start()，无法进行多线程调试，所以换成前面的样式
        workthread.start()

    while True:
        if TaskQueue.isFloorQueueEmpty():
            break
        else:
            pass
    # =====================================请求 pageList 结束=====================================

    # 33333-取出itemQueue 存入数据库
    service = EntityService('movie_home_200201')

    # ===222222===请求 pageInfoList（MidQueue） 中的信息，存入itemQueue中
    for i in range(THREAD_SUM):
        workthread = TopWorkThread(TaskQueue.getMiddleQueue(), i)
        # workthread.run()   #原版是workthread.start()，无法进行多线程调试，所以换成前面的样式
        workthread.start()

    # 爬取计数
    count = 1

    while True:
        if TaskQueue.isMiddleQueueEmpty():
            service.finalSpider()
            # 队列枯竭，关闭数据库连接
            service.shutDownDB()
            break
        elif TaskQueue.isContentQueueFull():
            service.finalSpider()
            print("当前分析页面的叠加数：" + str(count * 200))
            count = count + 1

        else:
            pass
    # ====================请求 pageInfoList 结束======================


# 主函数 入口？什么几把原理？
if __name__ == '__main__':
    startSpider()
