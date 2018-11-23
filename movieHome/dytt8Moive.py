#!/usr/bin/env python
#coding=utf-8

'''
@Desc
    主要用来抓取电影天堂（www.dytt8.net）的电影信息(包括电影名、导演、主角、下载地址)
    爬取入口【最新电影】(http://www.dytt8.net/html/gndy/dyzz/index.html)

'''
import requests
from lxml import etree

from model.RequestModel import RequestModel


class dytt_Lastest(object):

    # 获取爬虫程序抓取入口，即找到可以大量翻页的地方
    breakoutUrl = 'http://www.idyjy.com/w.asp?p=1&f=3&l=t'

    def __init__(self, sum):
        self.sum = sum


    # 获取【最新电影】有多少个页面
    # 截止到2017-08-08, 最新电影一共才有 164 个页面，返回一个页面总数（int）
    @classmethod
    def getMaxsize(cls):
        response = requests.get(cls.breakoutUrl, headers=RequestModel.getHeaders(), proxies=RequestModel.getProxies(), timeout=300)
        # 需将电影天堂的页面的编码改为 GBK, 不然会出现乱码的情况
        response.encoding = 'GBK'

        # print("请求地址为1："+cls.breakoutUrl)
        # print("请求地址为2："+str(RequestModel.getHeaders()))
        # print("请求地址为3："+str(RequestModel.getProxies()))
        #
        #print("页面信息为："+response.text)

        selector = etree.HTML(response.text)
        # 提取信息
        page = selector.xpath("//div[@id='pages']/text()")
        print(page)
        #['页次:1/715页']

        pageNum = str(page).split('/')[1].split('页')[0]
        print(pageNum)
        #715
        return pageNum


    # 获取 所有页面的 的URL，返回一个URL的集合（list）
    def getPageUrlList(self):
        '''
        主要功能：目录页url取出，比如：http://www.idyjy.com/w.asp?p=1&f=3&l=t，目标变换就仅仅只是p变量发生变化
        '''
        #定义并初始化 一个list集合
        templist = []
        request_url_prefix = 'http://www.idyjy.com/w.asp?'

        #templist = [request_url_prefix + 'index.html']

        for i in range(1, int(self.sum)+1):
            templist.append(request_url_prefix + 'p=' + str(i) + '&f=3&l=t')

        for t in templist:
            print('request url is ###   ' + t + '    ###')

        return templist



    #获取 一个页面上的 所有电影的链接，返回一个所有电影的URL的集合（list）
    @classmethod
    def getMoivePageUrlList(cls, html):
        '''
        获取电影信息的网页链接
        '''
        selector = etree.HTML(html)
        templist = selector.xpath("//ul[@class='img-list clearfix']/li/a/@href")
        # print(len(templist))
        # print(templist)
        return templist



    #请求一个电影链接，进入该电影信息页面，爬取内容。最为复杂的匹配页面函数
    @classmethod
    def getMoiveInforms(cls, url, html):

        #定义并初始化一个 容器，用来存储一个电影对象
        contentDir = {
            'name': '',
            'transName': '',
            'desc': '',
            'type': '',
            'decade': '',
            'conutry': '',
            'IMDB_id': '',
            'douban_score': '',
            'director': '',
            'actor': '',
            'placard': '',
            'ftpUrl': '',
            'thunderUrl': ''
        }

        selector = etree.HTML(html)

        #语法介绍：infoList[0][1:5]  这个列表的第0个元素的内容，从1开始，5结束的内容
        #xpath得到的是一个列表，我们默认使用这个列表的第一个元素

        #应该先判断 如果存在，再操作，否则下一部电影（这个功能如何实现），这样可以避免插入空电影
        #影片名
        if len(selector.xpath("//span[@id='name']/text()")):
            contentDir['name'] = selector.xpath("//span[@id='name']/text()")[0]

            #影片图片
            contentDir['placard'] = selector.xpath("//div[@class='pic']/img/@src")[0]


            #获取info div中 第一个li内容，存在列表中
            infoList = selector.xpath("//div[@class='info']/ul/li[1]/text()")

            contentDir['decade'] = infoList[0][1:5]
            contentDir['conutry'] = infoList[1][1:3]



            #可以同时是多种类型
            typeList = selector.xpath("//div[@class='info']/ul/li[2]/a/text()")
            for each in typeList:
                contentDir['type'] = contentDir['type'] + str(each)+"/"


            contentDir['director'] = selector.xpath("//div[@class='info']/ul/li[3]/a/text()")[0]

            #一个集合
            actorList = selector.xpath("//div[@class='info']/ul/li[4]/a/text()")
            for each in actorList:
                contentDir['actor'] = contentDir['actor'] + str(each)+"/"


            contentDir['transName'] = selector.xpath("//div[@class='info']/ul/li[5]/text()")[0]


            contentDir['IMDB_id'] = selector.xpath("//span[@id='imdb']/text()")[0]

            #豆瓣分数，并四舍五入1位小数
            tempList = selector.xpath("//div[@class='star']/script/text()")[0]
            people = str(tempList).split(',')[1]
            score = str(tempList).split(',')[3]
            contentDir['douban_score'] = str(round(int(score)/int(people), 1))


            contentDir['desc'] = selector.xpath("//div[@class='endtext']/text()")[0]


            #处理下载资源的获取 与 拼串
            #只要有下载框，就进去。没有下载框，跳出。  downDIV可能为空
            thunderURL=""

            count = 0
            while len(selector.xpath("//input[@name='down_url_list_" + str(count) + "']/@value")):
                #旧样式
                if count == 0:
                    title = selector.xpath("//input[@name='down_url_list_0']/../../../../div[@class='title']/span/h3/text()")[0]
                    #1个字符串 3个列表
                    downURL = selector.xpath("//input[@name='down_url_list_0']/@value")
                    nameList = selector.xpath("//input[@name='down_url_list_0']/../p/strong/a/text()")
                    sizeList = selector.xpath("//input[@name='down_url_list_0']/../span/em/text()")
                    #一个下载DIV 拼串
                    title = str(title).rstrip("1")
                    item = title+"@@"
                    for i in range(len(sizeList)):
                        item = item+downURL[i]+"&&"+nameList[i]+"&&"+sizeList[i]+"##"

                    thunderURL=thunderURL+item+"$$"

                #新样式
                else:
                    title = selector.xpath("//input[@name='down_url_list_" + str(count) + "']/../../../../div[@class='title']/span/h3/text()")[0]
                    downURL = selector.xpath("//input[@name='down_url_list_" + str(count) + "']/@value")
                    sizeList = selector.xpath("//input[@name='down_url_list_" + str(count) + "']/../p/strong/a/em/text()")
                    nameList = selector.xpath("//input[@name='down_url_list_" + str(count) + "']/../p/strong/a/text()")
                    # 拿到偶数项， 相关奇数项为[::2]
                    nameList = nameList[1::2]
                    newNameList = []
                    # 删除字符串中 ]
                    for each in nameList:
                        newNameList.append(str(each).lstrip("]"))


                    # 一个下载DIV 拼串
                    item = title+"@@"
                    for i in range(len(sizeList)):
                        item = item+downURL[i]+"&&"+newNameList[i]+"&&"+sizeList[i]+"##"

                    thunderURL = thunderURL + item + "$$"

                #进入下一个 下载框
                count = count+1

            contentDir['thunderUrl'] = thunderURL

            print(contentDir)
            return contentDir

        #获取不到 页面电影名称，避免产生空项，故返回None
        else:
            return None