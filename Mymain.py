# import sqlite3

import json
import os

import cfg
from my_thread.ThreadOne import ThreadOne
from my_thread.ThreadTwo import ThreadTwo
from dao.EntityService import EntityService
from model.TaskQueue import TaskQueue
from do_main.dytt8Moive import dytt_Lastest
from model.proxy_model import ProxyModel

# cfg.py为自定义的项目总配置文件
'''
    程序主入口
'''


def start_spider():
    # 确定起始页面 ，终止页面

    # dytt_Lastest.getMaxsize()
    LASTEST_MOIVE_TOTAL_SUM = dytt_Lastest.getMaxsize(cfg.WEBSITE + 'w.asp?p=1&f=3&l=t')
    # dyttlastest = dytt_Lastest('http://www.idyjy.com/w.asp?p=1&f=3&l=t', 'p=', '&f', LASTEST_MOIVE_TOTAL_SUM)
    dyttlastest = dytt_Lastest(cfg.WEBSITE + 'w.asp?p=1&f=3&l=t', 'p=', '&f', LASTEST_MOIVE_TOTAL_SUM)

    pagelist = dyttlastest.getPageUrlList()

    # ======将 pageList加入队列1，因为队列线程安全=========
    pageQueue = TaskQueue.getQueue_1()
    for item in pagelist:
        pageQueue.put(item, 3)

    # =======用线程请求pageQueue（pageList）（注意队列枯竭），将请求结果存入pageInfoList中=========
    for i in range(cfg.THREAD_SUM):
        thread_one = ThreadOne(pageQueue, i)
        # thread_one.run()  # thread.run()只能启动一个主线程
        thread_one.start()

    # 监听thread_one是否干完活
    while True:
        # 逻辑生成的主页链接 枯竭（queue1枯竭）
        if TaskQueue.isQueue_1Empty():
            break
        # # 队列2满，10页满
        # elif TaskQueue.isQueue_2Full():
        #     break
        else:
            pass
    # =====================================请求 pageList 结束=====================================

    # 33333-取出itemQueue 存入数据库
    service = EntityService('movie_home_210212')

    # ===222222===请求 pageInfoList（MidQueue） 中的信息，存入itemQueue中
    for i in range(cfg.THREAD_SUM):
        thread_two = ThreadTwo(TaskQueue.getQueue_2(), i)  # 为什么会从queue_2中提取数据，因为在thread_one中已将数据加入到了queue_2
        thread_two.start()

    # 爬取计数
    count = 1

    while True:
        # 队列2为空，即爬取完成，将剩余数据添加到数据库，并关闭数据库连接
        if TaskQueue.isQueue_2Empty():
            service.finalSpider()
            # 队列枯竭，关闭数据库连接
            service.shutDownDB()
            break
        # 队列3满了，为避免内存溢出，立即将队列中的数据添加到数据库
        elif TaskQueue.isQueue_3Full():
            service.doTable()
            service.finalSpider()
            print("当前分析页面的叠加数：" + str(count * 200))  # 200：因为设置了队列3的上限个数为200
            count = count + 1

        else:
            pass
    # ====================请求 pageInfoList 结束======================


def init_requestmodel():
    """
    初始化的目的：将json文件转移到proxy_poll_http等两个私有变量中
    """
    dataPath = os.path.abspath(cfg.RootPath + '\\proxy_host\\proxy_ip.json')  # 获取tran.csv文件的路径
    with open(dataPath, 'r', encoding='utf8') as f:
        # dict_ip = json.load(f)
        content = f.readlines()
        for line in content:
            data = json.loads(line)
            proxy_model = ProxyModel(data['type'], data['host'], data['port'])  # 使用一个实体类来接收代理的各种参数

            # 根据http类型，加入到相应的列表中
            if proxy_model.proxy_type == 'http':
                cfg.Proxy_Pool_http.append(proxy_model)
            elif proxy_model.proxy_type == 'https':
                cfg.Proxy_Pool_https.append(proxy_model)
            else:
                continue


# 主函数 入口
if __name__ == '__main__':
    init_requestmodel()
    start_spider()
