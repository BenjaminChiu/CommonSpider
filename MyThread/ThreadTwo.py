#!/usr/bin/env python
# coding=utf-8
import random
import threading
import time

import requests

from movieHome.dytt8Moive import dytt_Lastest
from model.request_model import RequestModel
from model.TaskQueue import TaskQueue

'''
    1)从电影详细信息页面【http://www.dytt8.net/html/gndy/dyzz/20170806/54695.html】中抓取目标内容
    2)将数据存储到数据库中
'''


class ThreadTwo(threading.Thread):
    NOT_EXIST = 0

    def __init__(self, queue, id):
        threading.Thread.__init__(self)
        self.queue = queue
        self.id = id

    def run(self):
        # 循环取出 电影链接队列，分析页面了
        while not self.NOT_EXIST:
            # 队列为空, 结束
            if self.queue.empty():
                NOT_EXIST = 1
                self.queue.task_done()
                break

            url = self.queue.get()
            requests_model = RequestModel()
            try:
                response = requests_model.new_request(url)
                print('线程2代 子线程 ' + str(self.id) + ' 请求【 ' + url + ' 】的结果： ' + str(response.status_code))
                response.close()  # 为什么加这个？？？？  原因：出现了 远程主机强迫关闭了一个现有的连接

                # 需将电影天堂的页面的编码改为 GBK, 不然会出现乱码的情况
                response.encoding = 'GBK'

                if response.status_code != 200:
                    self.queue.put(url)
                    time.sleep(20)
                else:
                    # 分析 页面，将内容加入队列。一个队列中的元素就是一部完整的电影
                    temp = dytt_Lastest.getMoiveInforms(response.text)

                    # 空项 不添加进队列，避免数据库产生空项
                    if len(temp) and temp is not None:
                        # 队列put满后，等队列中数据被存入mysql后，在继续往队列中put
                        TaskQueue.getQueue_3().put(temp)
                        # TaskQueue.getContentQueue().join()
                        print("当前队列数量=" + str(TaskQueue.getQueue_3().qsize()))

                # 线程沉睡5秒
                time.sleep(random.randint(5, 20))

            except Exception as e:
                # self.queue.put(url)
                print(e)
