#!/usr/bin/env python
#coding=utf-8

import threading
import time

import requests

from movieHome.dytt8Moive import dytt_Lastest
from model.RequestModel import RequestModel
from model.TaskQueue import TaskQueue

'''
    1)从电影详细信息页面【http://www.dytt8.net/html/gndy/dyzz/20170806/54695.html】中抓取目标内容
    2)将数据存储到数据库中
'''
class TopWorkThread(threading.Thread):

    NOT_EXIST = 0

    def __init__(self, queue, id):
        threading.Thread.__init__(self)
        self.queue = queue
        self.id = id



    def run(self):
        while not self.NOT_EXIST:
            # 队列为空, 结束
            if self.queue.empty():
                NOT_EXIST = 1
                self.queue.task_done()
                break

            url = self.queue.get()
            try:
                response = requests.get(url, headers=RequestModel.getHeaders(), proxies=RequestModel.getProxies(), timeout=3)
                print('Top 子线程 ' + str(self.id) + ' 请求【 ' + url + ' 】的结果： ' + str(response.status_code))

                # 需将电影天堂的页面的编码改为 GBK, 不然会出现乱码的情况
                response.encoding = 'GBK'

                if response.status_code != 200:
                    self.queue.put(url)
                    time.sleep(20)
                else :
                    #分析 页面，将内容加入队列。一个队列就是一部完整的电影
                    temp = dytt_Lastest.getMoiveInforms(url, response.text)
                    #空项 不添加进队列，避免数据库产生空项
                    if len(temp):
                        TaskQueue.getContentQueue().put(temp)
                #线程沉睡5 s/ ms???
                time.sleep(5)

            except Exception as e:
                # self.queue.put(url)
                print(e)
