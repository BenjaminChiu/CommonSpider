#!/usr/bin/env python
# coding=utf-8
import random
import threading
import time

from util.my_request import MyRequest
from proxy_host.proxy_json import proxy_false

'''
多线程作用：
请求 param:queue中的url
return response.text or None
'''


class ThreadOne(threading.Thread):

    def __init__(self, id, queue, session, *proxy_flag):
        threading.Thread.__init__(self)
        self.id = id
        self.queue = queue
        self.session = session
        self.proxy_flag = proxy_flag

    def run(self):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                request = MyRequest(self.session, url, self.proxy_flag)
                response = request.my_get()
                print('线程1代 子线程 ' + str(self.id) + ' 请求【 ' + url + ' 】的结果： ' + str(response.status_code))

                if response.status_code == 200:
                    return response.text
                # 请求失败(404 500 503)
                else:
                    self.queue.put(url)  # 将URL重新加入队列
                    # 如果开启了代理、且请求失败，将修改代理
                    if self.proxy_flag:
                        proxy_false(request.proxy)
                    return None

            except Exception as e:
                print('1代子线程出现问题：' + str(e))
                return None
            finally:
                # 干完活，返回一个标记。使得queue.join()能执行，而不是无限挂起
                self.queue.task_done()  # 仅仅表示get成功后，执行的一个标记。不能用在queue.put()上
                time.sleep(random.randint(5, 20))  # 子线程 随机休眠
