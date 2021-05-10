# import sqlite3

import cfg
from dao.EntityService import EntityService
from do_main.dytt import dytt_Lastest
from model.task_queue import TaskQueue
from my_thread.ThreadOne import ThreadOne
from my_thread.ThreadTwo import ThreadTwo

# cfg.py为自定义的项目总配置文件
'''
    使用子线程请求，拿到response.text
    借助适配规则，在本文件中的逻辑控制，完成任务
    
    这样只需要修改适配规则，与逻辑控制就能完成任务，达到通用爬虫的目的
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
        pageQueue.put(item, 3)  # 3代表？

    # =======用线程请求pageQueue（pageList）（注意队列枯竭），将请求结果存入pageInfoList中=========
    for i in range(cfg.THREAD_SUM):
        thread_one = ThreadOne(i, pageQueue)
        # thread_one.run()  # thread.run()只能启动一个主线程
        thread_one.start()

    pageQueue.join()  # 使用新api，这个队列完事了。搭配Queue.task_done()
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


# 主函数 入口
if __name__ == '__main__':
    # read_proxy_json()   读取代理
    start_spider()
    # start_spider() 队列1
    # start_spider() 队列2       这样当队列1中有内容时，就开始请求。不用等队列1完事了才开始第二阶段。队列1中的用完后，即释放内存
