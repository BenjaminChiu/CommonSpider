"""
@Desc   : 获取代理，存放到ip代理池。1.从json文件中获取，2.从数据库中获取（暂时不用数据库，太重）
@Time   : 2021-01-28 19:10
@Author : tank boy
@File   : get_proxy.py
@coding : utf-8
"""

import json
import random
import threading
import time
from queue import Queue

from util.my_request import MySession
from proxy_host.proxy_json import info_proxy_dict, verify_proxy, request_to_json


def clean_json():
    """
    清空json文件
    """
    with open('proxy.json', 'w') as f:
        f.seek(0)
        f.truncate()
        f.close()
    print("json已清空数据")


def write_proxy(pass_proxy):
    """
    将测试通过的代理写入json文件
    """
    temp_json = json.dumps(pass_proxy)
    with open('proxy.json', 'a+') as f:
        f.write(temp_json + '\n')
        f.close()
    print("已写入：%s" % pass_proxy)
    # 不使用下面这种方法，是因为pass_proxy是一个Python对象，无法与一个字符串相加
    # with open('proxy.json', 'w') as f:
    #     json.dump(pass_proxy + '\n', f)


# 为每个代理添加一个生命值，并初始化赋值如100，（磁盘 持久化）
# 没请求失败一次就-1，直至为0，从文件中删除（内存 内存中删除）
def get_proxy_from_list():
    """
    从.list文件中读取代理信息，获取ip，port ，type
    未用request请求.list文件的原因：需要翻墙才能下载。只能手动翻墙，手动下载
    """
    proxy_queue = Queue()
    with open("C:/Users/Administrator/Desktop/proxy.list", "r") as f:
        data = f.read()
        proxies_list = data.split('\n')  # 拆分开返回的数据
        clean_json()  # 手动清空json文件

        # 总数-1的目的是，读文件的时候，总会多读1行
        for i in range(len(proxies_list) - 1):
            proxy_json = json.loads(proxies_list[i])  # print(str(i) + proxies_list[i])
            type, host, port = info_proxy_dict(proxy_json)  # 提取字典信息，重新赋值
            proxy = {type: type + '://' + host + ':' + str(port)}  # 封装为一个request形式的proxy
            proxy_queue.put(proxy)  # 加入队列

        f.close()  # 关闭文件
    return proxy_queue


class ThreadVerify(threading.Thread):
    def __init__(self, id, session, in_queue, out_queue):
        super().__init__()
        self.id = id
        self.session = session
        self.in_queue = in_queue  # 未测试的代理
        self.out_queue = out_queue  # 测试合格的代理

    def run(self):
        while not self.in_queue.empty():
            proxy = self.in_queue.get()
            if verify_proxy(self.session, proxy, self.id):
                proxy_pass = request_to_json(proxy)
                proxy_pass['hp'] = 9  # 新增一个hp键，0开始计数
                # id键在这里无法确定，只有在写文件时赋值
                self.out_queue.put(proxy_pass)
            self.in_queue.task_done()
            time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    session = MySession()
    proxy_queue = get_proxy_from_list()  # 读.list代理，存入队列
    out_queue = Queue()

    for i in range(1):
        thread = ThreadVerify(i, session, proxy_queue, out_queue)
        thread.start()

    proxy_queue.join()
    print("%s" % out_queue)
    # write_proxy(proxy)
