#!/usr/bin/env python
# coding=utf-8
import random
import threading
import time

import requests

from movieHome.dytt8Moive import dytt_Lastest
from model.request_model import RequestModel
from model.TaskQueue import TaskQueue
import cfg

'''
    1)自己封装抓取二级网页多线程
    2)由一级链接 抓取 电影目录
    例如：由 http://www.dytt8.net/html/gndy/dyzz/list_23_2.html 获取
           "2017年动画喜剧《宝贝老板》英国粤三语.BD中英双字幕" 和 "页面 url 地址"等若干条电影的信息
@Author monkey
@Date 2017-08-08
'''


class ThreadOne(threading.Thread):
    NOT_EXIST = 0

    # host = 'http://www.idyjy.com'

    def __init__(self, queue, id):
        threading.Thread.__init__(self)
        self.queue = queue
        self.id = id

    def run(self):
        while not self.NOT_EXIST:
            # 队列为空, 结束。为什么先判断？因为如果先做业务的话，绝对会出错
            if self.queue.empty():
                NOT_EXIST = 1
                self.queue.task_done()
                break

            url = self.queue.get()
            request_model = RequestModel()
            try:
                response = request_model.new_request(url)
                print('线程1代 子线程 ' + str(self.id) + ' 请求【 ' + url + ' 】的结果： ' + str(response.status_code))

                # 需将电影天堂的页面的编码改为 GBK, 不然会出现乱码的情况
                response.encoding = 'GBK'

                # 请求失败
                if response.status_code != 200:
                    # 将URL 重新加入队列，并休眠20ms
                    self.queue.put(url)
                    time.sleep(20)
                # 请求成功
                else:
                    # 获取一页上所有的 电影的链接，并存入容器，返回一个List
                    moivePageUrlList = dytt_Lastest.getMoivePageUrlList(response.text)
                    for item in moivePageUrlList:
                        each = cfg.WEBSITE + item   # 拼接每一部电影的链接
                        # print("在FloorWorkThread中，每部具体电影的URL："+each)
                        TaskQueue.putToQueue_2(each)    # 将页面上许多电影的链接 存入queue2
                # 支线程 随机休眠
                time.sleep(random.randint(5, 20))

            except Exception as e:
                # print('catsh  Exception ==== ')
                # self.queue.put(url)
                print(e)
