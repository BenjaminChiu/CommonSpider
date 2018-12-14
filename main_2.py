#!/usr/bin/env python
#coding=utf-8


#import sqlite3
import pymysql
import re

from dao.EntityDao import EntityDao
from movieHome.dytt8Moive import dytt_Lastest
from model.TaskQueue import TaskQueue
from service.EntityService import EntityService
from thread.FloorWorkThread import FloorWorkThread
from thread.TopWorkThread import TopWorkThread
from model.Entity import Entity

'''
    程序主入口
@Author monkey
@Date 2017-08-08
'''

# 截止到2017-08-08, 最新电影一共才有 164 个页面
#LASTEST_MOIVE_TOTAL_SUM = 6 #164

# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
THREAD_SUM = 2


def startSpider():
    # 实例化对象

    # 电视剧 http://www.idyjy.com/w.asp?p=1&f=2&l=t

    #确定起始页面 ，终止页面

    #dytt_Lastest.getMaxsize()
    LASTEST_MOIVE_TOTAL_SUM = dytt_Lastest.getMaxsize('http://www.idyjy.com/w.asp?p=1&f=3&l=t')
    dyttlastest = dytt_Lastest('http://www.idyjy.com/w.asp?p=1&f=3&l=t', 'p=', '&f', 3)



    floorlist = dyttlastest.getPageUrlList()

    floorQueue = TaskQueue.getFloorQueue()
    for item in floorlist:
        floorQueue.put(item, 3)

    # print(floorQueue.qsize())

    for i in range(THREAD_SUM):
        workthread = FloorWorkThread(floorQueue, i)
        workthread.start()

    while True:
        if TaskQueue.isFloorQueueEmpty():
            break
        else:
            pass

    count = 1
    for i in range(THREAD_SUM):
        workthread = TopWorkThread(TaskQueue.getMiddleQueue(), i)
        workthread.start()


    while True:
        if TaskQueue.isMiddleQueueEmpty():
            break
        else:
            pass

    #调用业务方法，插入数据
    EntityService('table_1214').finalSpider()



#主函数 入口？什么几把原理？
if __name__ == '__main__':
    startSpider()