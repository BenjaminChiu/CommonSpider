"""
@Desc   : 爬取翻墙链接
@Time   : 2021-05-10 10:55
@Author : tank boy
@File   : vmess_main.py
@coding : utf-8
"""
import re

from lxml import etree

import cfg
from model.request_model import MyRequest, MySession

# 正则表达式匹配vmess
pattern = re.compile(r'^(vmess://|ss://)\w')


def init():
    session = MySession()
    response = MyRequest(session, cfg.vmess_web).my_get()
    print("监测点1：链接成功")
    selector = etree.HTML(response.text)
    day = selector.xpath("//div[@class='post-outer']/div[@class='post']/article/font/h2/a/@href")  # day是一个list  div[@class='post-outer' and position()=1]

    data = []
    for i in range(len(day)):
        response_2 = MyRequest(session, day[i]).my_get()
        print("监测点2：链接成功")
        selector_2 = etree.HTML(response_2.text)
        data = selector_2.xpath("//div[@style='-webkit-text-stroke-width: 0px;']/div[3]/div/text()")  # 注意脚标是1开始，而非0
        # 做兼容
        if len(data) == 0:
            data = selector_2.xpath("//div[@style='-webkit-text-stroke-width: 0px;']/div[4]/div/text()")
        if len(data) == 0:
            data = selector_2.xpath("//div[@style='-webkit-text-stroke-width: 0px;']/div[5]/div/text()")
        # 能拿到信息，即结束
        if len(data) != 0:
            print("今日链接为：%s" % day[i])
            print("当前链接的顺位是 %s" % i)
            break

    print("爬取到的节点数量为：%s" % len(data))
    # 使用print写文件，不会有引号问题。三引号可以保留换行格式
    with open('C:/Users/Administrator/Desktop/vmess.json', 'w') as f:
        for i in range(len(data)):
            print(data[i], file=f)
        f.close()


if __name__ == '__main__':
    # init()

    match = pattern.match(
        'vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogImh0dHBzOi8vd3d3Lm1hdHRrYXlkaWFyeS5jb21844CQ55u06L+e44CRSEtHL+mmmea4ryBBIC0gOCIsDQogICJhZGQiOiA'
        'iMDA4LkhLLkFQLlBPUC5CSUdBSVJQT1JULk5FVCIsDQogICJwb3J0IjogIjgwIiwNCiAgImlkIjogImJiNTExMzQ3LTZlZDUtNDc1Yy05ZmZlLWFjNzI2OGZkZjM1MSIsDQogICJ'
        'haWQiOiAiMSIsDQogICJzY3kiOiAiYXV0byIsDQogICJuZXQiOiAid3MiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAiIiwNCiAgInBhdGgiOiAiIiwNCiAgInRscyI'
        '6ICIiLA0KICAic25pIjogIiINCn0=')
    match_2 = pattern.match('ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpaRUNTbGFUWmVhNWpGTzczNkZBM1J5M0RhWFJBMnFOeDBwY2VZRHpLQ3VZUzhnbDNCNHA4SW53eURDT1N4OUAxNT'
                            'QuMTcuMi4yMTE6MTgzMzI=#https%3a%2f%2fwww.mattkaydiary.com%7c%e7%be%8e%e5%9b%bd%e3%8a%b4%e7%9b%b4%e8%bf%9e')
    print("%s" % match_2.string)
