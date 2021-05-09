#!/usr/bin/env python
# coding=utf-8
import random
import threading
import time

import model.request_model as my_request
from model.request_model import new_request

'''
request queue1，put response to Queue2
'''


class ThreadOne(threading.Thread):

    def __init__(self, id, queue):
        threading.Thread.__init__(self)
        self.id = id
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                response = new_request(url, my_request.header_1, False)
                print('线程1代 子线程 ' + str(self.id) + ' 请求【 ' + url + ' 】的结果： ' + str(response.status_code))

                # 需将电影天堂的页面的编码改为 GBK, 不然会出现乱码的情况
                response.encoding = 'GBK'

                if response.status_code != 200:  # 请求失败
                    self.queue.put(url)  # 将URL重新加入队列，并休眠20ms
                    return None
                else:  # 请求成功
                    # 获取一页上所有的 电影的链接，并存入容器，返回一个List
                    # moivePageUrlList = dytt_Lastest.getMoivePageUrlList(response.text)
                    # for item in moivePageUrlList:
                    #     each = cfg.WEBSITE + item  # 拼接每一部电影的链接
                    #     # print("在FloorWorkThread中，每部具体电影的URL："+each)
                    #     TaskQueue.putToQueue_2(each)  # 将页面上许多电影的链接 存入queue2

                    return response.text
            except Exception as e:
                print('1代子线程出现问题：' + str(e))
                return None
            finally:
                # 干完活，返回一个标记。使得queue.join()能执行，而不是无限挂起
                self.queue.task_done()  # 仅仅表示get成功后，执行的一个标记。不能用在queue.put()上
                time.sleep(random.randint(5, 20))  # 子线程 随机休眠
