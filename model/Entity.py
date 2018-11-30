#!/usr/bin/env python
#coding=utf-8

'''
    实体类
'''

class Entity(object):

    '''
    将字典转化为列表，返回一个list集合
    '''
    @staticmethod
    def dirToList(item):
        itemlist = []
        itemlist.append(item['mName'])
        itemlist.append(item['transName'])
        itemlist.append(item['altName'])
        itemlist.append(item['mDesc'])
        itemlist.append(item['mType'])
        itemlist.append(item['decade'])
        itemlist.append(item['conutry'])
        itemlist.append(item['imdbId'])
        itemlist.append(item['doubanScore'])
        itemlist.append(item['director'])
        itemlist.append(item['actor'])
        itemlist.append(item['placard'])
        itemlist.append(item['updateTo'])
        itemlist.append(item['thunderUrl'])
        return itemlist