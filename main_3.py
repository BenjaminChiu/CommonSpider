#!/usr/bin/env python
#coding=utf-8


#import sqlite3
import pymysql
import re

from dao.EntityDao import EntityDao
from movieHome.dytt8Moive import dytt_Lastest
from model.TaskQueue import TaskQueue
from service.EntityService import EntityService
from MyThread.ThreadOne import FloorWorkThread
from MyThread.ThreadTwo import TopWorkThread
from model.Entity import Entity

'''
    程序主入口
'''

#LASTEST_MOIVE_TOTAL_SUM = 6 #164

# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
THREAD_SUM = 6


def startSpider():
    # 实例化对象 动画片

    # 电视剧 http://www.idyjy.com/w.asp?p=1&f=2&l=t

    #确定起始页面 ，终止页面

    #dytt_Lastest.getMaxsize()
    LASTEST_MOIVE_TOTAL_SUM = dytt_Lastest.getMaxsize('http://www.idyjy.com/w.asp?p=1&f=27&l=t')
    dyttlastest = dytt_Lastest('http://www.idyjy.com/w.asp?p=1&f=27&l=t', 'p=', '&f', LASTEST_MOIVE_TOTAL_SUM)



    pagelist = dyttlastest.getPageUrlList()


    #======将 pageList加入队列，因为队列线程安全=========
    pageQueue = TaskQueue.getFloorQueue()
    for item in pagelist:
        pageQueue.put(item, 3)



    #=====1111==用线程请求pageQueue（pageList）（注意队列枯竭），将请求结果存入pageInfoList中=========
    for i in range(THREAD_SUM):
        workthread = FloorWorkThread(pageQueue, i)
        workthread.start()

    while True:
        if TaskQueue.isFloorQueueEmpty():
            break
        else:
            pass
    #=====================================请求 pageList 结束=====================================





    #33333-取出itemQueue 存入数据库
    service = EntityService('cartoon_home_1218')





    #===222222===请求 pageInfoList（MidQueue） 中的信息，存入itemQueue中
    for i in range(THREAD_SUM):
        workthread = TopWorkThread(TaskQueue.getMiddleQueue(), i)
        workthread.start()

    while True:
        if TaskQueue.isMiddleQueueEmpty():
            service.finalSpider()
            #队列枯竭，关闭数据库连接
            service.shutDownDB()
            break
        elif TaskQueue.isContentQueueFull():
            service.finalSpider()
        else:
            pass
    # ====================请求 pageInfoList 结束======================







#主函数 入口？什么几把原理？
if __name__ == '__main__':
    startSpider()