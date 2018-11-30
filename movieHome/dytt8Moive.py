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

    # 初始页面即抓取入口，即找到可以大量翻页的地方

    #相当于构造函数，初始化起始页面 ，页面总数；后两个参数是页面变换时 以迭代变换的数字为中心，左右的关键定位字
    def __init__(self, breakoutUrl, prefixKey, suffixKey, sum):
        self.breakoutUrl = breakoutUrl
        self.prefixKey = prefixKey
        self.suffixKey = suffixKey
        self.sum = sum



    # 获取【最新电影】有多少个页面
    # 截止到2017-08-08, 最新电影一共才有 164 个页面，返回一个页面总数（int）
    @classmethod
    def getMaxsize(self, breakoutUrl):
        response = requests.get(breakoutUrl, headers=RequestModel.getHeaders(), proxies=RequestModel.getProxies(), timeout=300)
        # 需将电影天堂的页面的编码改为 GBK, 不然会出现乱码的情况
        response.encoding = 'GBK'

        selector = etree.HTML(response.text)
        # 提取信息
        page = selector.xpath("//div[@id='pages']/text()")
        pageNum = str(page).split('/')[1].split('页')[0]
        return pageNum


    # 获取 所有页面的 的URL，返回一个URL的集合（list）
    def getPageUrlList(self):
        '''
        主要功能：目录页url取出，比如：http://www.idyjy.com/w.asp?p=1&f=3&l=t，目标变换就仅仅只是p变量发生变化
        '''
        #定义并初始化 一个list集合
        templist = []

        # 定义前缀与后缀
        # 'http://www.idyjy.com/w.asp?'
        request_url_prefix = str(self.breakoutUrl).split(str(self.prefixKey))[0]

        request_url_suffix = str(self.breakoutUrl).split(str(self.suffixKey))[1]

        #起始页
        startPage = str(self.breakoutUrl).split(str(self.prefixKey))[1].split(str(self.suffixKey))[0]

        print("测试startPage="+str(startPage))

        for i in range(int(startPage), int(self.sum)+1):
            templist.append(request_url_prefix + str(self.prefixKey) + str(i) + str(self.suffixKey) + request_url_suffix)


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
            'mName': '',
            'transName': '',
            'altName': '',
            'mDesc': '',
            'mType': '',
            'decade': '',
            'conutry': '',
            'imdbId': '',
            'doubanScore': '',
            'director': '',
            'actor': '',
            'placard': '',
            'updateTo': '',
            'thunderUrl': ''
        }

        selector = etree.HTML(html)

        #语法介绍：infoList[0][1:5]  这个列表的第0个元素的内容，从1开始，5结束的内容
        #xpath得到的是一个列表，我们默认使用这个列表的第一个元素

        #应该先判断 如果存在，再操作，否则下一部电影（这个功能如何实现），这样可以避免插入空电影
        #影片名

        tmpName = selector.xpath("//span[@id='name']/text()")
        if len(tmpName):
            contentDir['mName'] = tmpName[0]

            tmpTrName = selector.xpath("//span[@id='name']/../text()")
            if len(tmpTrName):
                contentDir['transName'] = tmpTrName[0]



            #兼容 电视剧页面

            liNum = 1

            # 判断 页面类型：电视剧？电影？。约定 1表示电影， 2表示电视剧
            pageType = 1

            upKeyList = selector.xpath("//div[@class='info']/ul/li[" + str(liNum) + "]/span/text()")
            if len(upKeyList) and "更新" == upKeyList[0][0:2]:
                pageType = 2    #标注页面，虽然也可以用liNum 判断。但耦合过高
                upList = selector.xpath("//div[@class='info']/ul/li[" + str(liNum) + "]/text()")
                if len(upList):
                    contentDir['updateTo'] = upList[0]
                #为什么是这个位置，因为能进来，肯定是电视剧页面；故 分析完这栏 加 1
                liNum = liNum + 1


            #影片图片，插入这个位置不得已。因为必须用到pageType 来判断页面
            tmpPCard= selector.xpath("//div[@class='pic']/img/@src")
            tmpPCardOrg = selector.xpath("//div[@class='pic']/img/@original")
            if len(tmpPCard) and pageType == 1:
                contentDir['placard'] = tmpPCard[0]
            elif len(tmpPCardOrg) and pageType == 2:
                contentDir['placard'] = tmpPCardOrg[0]



            #获取info div中 第一个li内容，存在列表中
            infoList = selector.xpath("//div[@class='info']/ul/li["+ str(liNum) +"]/text()")
            print("整个infoList是"+ str(infoList))
            if len(infoList):
                if 1 == pageType:
                    contentDir['decade'] = infoList[0][1:5]
                    contentDir['conutry'] = infoList[1]
                elif 2 == pageType:
                    contentDir['decade'] = infoList[0][0:4]
                    contentDir['conutry'] = infoList[1]



            liNum = liNum + 1
            #可以同时是多种类型
            typeList = selector.xpath("//div[@class='info']/ul/li["+ str(liNum) +"]/a/text()")
            if len(typeList):
                for each in typeList:
                    contentDir['mType'] = contentDir['mType'] + str(each)+"/"


            liNum = liNum + 1
            tmpDire = selector.xpath("//div[@class='info']/ul/li["+ str(liNum) +"]/a/text()")
            if len(tmpDire):
                contentDir['director'] = tmpDire[0]


            liNum = liNum + 1
            #一个集合
            actorList = selector.xpath("//div[@class='info']/ul/li["+ str(liNum) +"]/a/text()")
            if len(actorList):
                for each in actorList:
                    contentDir['actor'] = contentDir['actor'] + str(each)+"/"



            liNum = liNum + 1
            tmpTranName = selector.xpath("//div[@class='info']/ul/li["+ str(liNum) +"]/text()")
            if len(tmpTranName):
                contentDir['altName'] = tmpTranName[0]



            tmpIMDBID= selector.xpath("//span[@id='imdb']/text()")
            if len(tmpIMDBID):
                contentDir['imdbId'] = tmpIMDBID[0]



            #豆瓣分数，并四舍五入1位小数
            tempList = selector.xpath("//div[@class='star']/script/text()")
            if len(tempList):
                people = str(tempList[0]).split(',')[1]
                score = str(tempList[0]).split(',')[3]
                contentDir['doubanScore'] = str(round(int(score)/int(people), 1))


            #电影简介   可能存在反爬虫，可能是页面版本混乱。总之，进行判断，兼容
            DescList = selector.xpath("//div[@class='endtext']/text()")
            DescInPList = selector.xpath("//div[@class='endtext']/p/text()")
            if len(DescList) and '\r\n' != DescList[0]:
                contentDir['mDesc'] = DescList[0]
            elif len(DescInPList):
                for each in DescInPList:
                    contentDir['mDesc'] = contentDir['mDesc'] + each + "$$"


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

                        if len(sizeList):
                            for i in range(len(sizeList)):
                                item = item+downURL[i]+"&&"+nameList[i]+"&&"+sizeList[i]+"##"
                        else:
                            for i in range(len(downURL)):
                                item = item+downURL[i]+"&&"+nameList[i]+"##"

                        thunderURL=thunderURL+item+"$$"

                    #新样式
                    else:
                        title = selector.xpath("//input[@name='down_url_list_" + str(count) + "']/../../../../div[@class='title']/span/h3/text()")[0]
                        downURL = selector.xpath("//input[@name='down_url_list_" + str(count) + "']/@value")
                        sizeList = selector.xpath("//input[@name='down_url_list_" + str(count) + "']/../p/strong/a/em/text()")
                        print("页面中存在的sizeList="+str(sizeList))
                        nameList = selector.xpath("//input[@name='down_url_list_" + str(count) + "']/../p/strong/a/text()")
                        newNameList = []


                        beStatus = None
                        #=默认不存在=======判断是否有[12.6G] 这类特殊的字符存在，如果存在才处理；不存在就绕行。====
                        if len(nameList) and '[' == nameList[0]:
                            beStatus = 1
                            # 拿到偶数项， 相关奇数项为[::2]
                            nameList = nameList[1::2]
                            # 删除字符串中 ]
                            for each in nameList:
                                newNameList.append(str(each).lstrip("]"))
                            # 为下面的循环语句 减负，将新容器newNameList 赋给 nameList
                            nameList = newNameList
                        #============判断结束=============================================


                        # 一个下载DIV 拼串
                        item = title+"@@"
                        if len(sizeList):
                            for i in range(len(sizeList)):
                                item = item+downURL[i]+"&&"+nameList[i]+"&&"+sizeList[i]+"##"
                        else:
                            for i in range(len(downURL)):
                                item = item+downURL[i]+"&&"+nameList[i]+"##"


                        thunderURL = thunderURL + item + "$$"

                    #进入下一个 下载框
                    count = count+1


            # 处理完成，开始赋值
            contentDir['thunderUrl'] = thunderURL

            print(contentDir)
            return contentDir

        #获取不到 页面电影名称，避免产生空项，故返回None
        else:
            return None