#!/usr/bin/env python
#coding=utf-8

'''
    实体类
'''

class Utils(object):

    '''
    将字典转化为列表，返回一个list集合
    '''
    @staticmethod
    def dirToList(item):
        itemlist = []
        itemlist.append(item['name'])
        itemlist.append(item['transName'])
        itemlist.append(item['desc'])
        itemlist.append(item['type'])
        itemlist.append(item['decade'])
        itemlist.append(item['conutry'])
        itemlist.append(item['IMDB_id'])
        itemlist.append(item['douban_score'])
        itemlist.append(item['director'])
        itemlist.append(item['actor'])
        itemlist.append(item['placard'])
        itemlist.append(item['ftpUrl'])
        itemlist.append(item['thunderUrl'])
        return itemlist