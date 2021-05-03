#!/usr/bin/env python
# coding=utf-8

"""
    实体类，用于Dao层 将队列中1个又一个的item解析成一个列表，后批量插入
"""


class Entity(object):
    """
    将字典转化为列表，返回一个list集合
    """

    @staticmethod
    def dir2list(item):
        item_list = [item['mName'], item['transName'], item['altName'], item['mDesc'], item['mType'], item['decade'],
                     item['conutry'], item['imdbId'], item['doubanScore'], item['director'], item['actor'],
                     item['placard'], item['updateTo'], item['thunderUrl'], item['dyjyUrl']]
        return item_list
