#!/usr/bin/env python
# coding=utf-8
import random
import threading
import time

from util.my_request import new_request

'''
request queue2，put response to Queue3
'''


class ThreadTwo(threading.Thread):
    def __init__(self, id, queue):
        threading.Thread.__init__(self)
        self.id = id
        self.queue = queue

    def run(self):
        # 循环取出 电影链接队列，分析页面了
        while not self.queue.empty():
            url = self.queue.get()
            try:
                response = new_request(url)
                print('线程2代 子线程 ' + str(self.id) + ' 请求【 ' + url + ' 】的结果： ' + str(response.status_code))
                response.close()  # 为什么加这个？？？？  原因：出现了 远程主机强迫关闭了一个现有的连接

                # 需将电影天堂的页面的编码改为 GBK, 不然会出现乱码的情况
                response.encoding = 'GBK'

                if response.status_code != 200:
                    self.queue.put(url)
                else:
                    # 分析 页面，将内容加入队列。一个队列中的元素就是一部完整的电影
                    # temp = dytt_Lastest.getMoiveInforms(response.text)
                    #
                    # # 空项 不添加进队列，避免数据库产生空项
                    # if len(temp) and temp is not None:
                    #     # 队列put满后，等队列中数据被存入mysql后，在继续往队列中put
                    #     TaskQueue.getQueue_3().put(temp)
                    #     # TaskQueue.getContentQueue().join()
                    #     print("当前队列数量=" + str(TaskQueue.getQueue_3().qsize()))
                    return response.text

            except Exception as e:
                print('子线程2代出现问题' + str(e))
            finally:
                self.queue.task_done()
                time.sleep(random.randint(5, 20))  # 线程沉睡5秒
