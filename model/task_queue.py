#!/usr/bin/env python
# coding=utf-8

"""
@Desc
    队列只是一个容纳List的容器，这个容器是线程安全的。故多此一举

    维护三个队列：
    queue_1     所有页的链接，有规律的话，一般逻辑生成。每个元素-->某一页的链接
    Queue_2    存储内容：每页上有很多具体内容。每个元素-->request上面队列中某一页，服务器返回的response
    Queue_3   根据上一个response，获取每个具体内容的链接；请求这个链接，进行内容分析。每个具体内容，定义一个有上限的队列，存储信息复杂的item；大大减少内存的开销。
    存放获取电影信息(名称、导演、主角、下载地址等)的队列, 方便后续持久化

    存放未爬取 url 的队列
    存放
"""
from queue import Queue


class TaskQueue(object):
    # 将三层队列初始化
    Queue_1 = Queue()
    Queue_2 = Queue()
    Queue_3 = Queue(200)

    def __init__(self):
        pass

    # get queue
    @classmethod
    def getQueue_1(cls):
        return cls.Queue_1

    @classmethod
    def getQueue_2(cls):
        return cls.Queue_2

    @classmethod
    def getQueue_3(cls):
        return cls.Queue_3

    # Put an item into the queue.
    @classmethod
    def putToQueue_1(cls, item):
        cls.Queue_1.put(item)

    @classmethod
    def putToQueue_2(cls, item):
        cls.Queue_2.put(item)

    @classmethod
    def putToQueue_3(cls, item):
        cls.Queue_3.put(item)

    # Return True if the queue is empty, False otherwise (not reliable!).
    @classmethod
    def isQueue_1Empty(cls):
        return cls.Queue_1.empty()

    @classmethod
    def isQueue_2Empty(cls):
        return cls.Queue_2.empty()

    @classmethod
    def isQueue_3Empty(cls):
        return cls.Queue_3.empty()

    @classmethod
    def isQueue_2Full(cls):
        return cls.Queue_2.full()

    @classmethod
    def isQueue_3Full(cls):
        return cls.Queue_3.full()
